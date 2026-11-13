"""Legt für einen CI-Lauf ein Apple-Distribution-Zertifikat und ein App-Store-Profil
über die App Store Connect API an und räumt es danach wieder auf.

  python asc_signing.py create   -> schreibt IOS_CERTIFICATE, IOS_CERTIFICATE_PASSWORD,
                                    IOS_MOBILE_PROVISION, ASC_CERT_ID, ASC_PROFILE_ID nach $GITHUB_ENV
  python asc_signing.py cleanup  -> löscht Profil und Zertifikat dieses Laufs

Benötigt: APPLE_API_ISSUER, APPLE_API_KEY, APPLE_API_KEY_PATH, BUNDLE_ID
"""
import base64, json, os, secrets, sys, time, urllib.error, urllib.request

import jwt
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID

API = "https://api.appstoreconnect.apple.com/v1"


def token():
    key = open(os.environ["APPLE_API_KEY_PATH"]).read()
    now = int(time.time())
    return jwt.encode({"iss": os.environ["APPLE_API_ISSUER"], "iat": now, "exp": now + 1100, "aud": "appstoreconnect-v1"},
                      key, algorithm="ES256", headers={"kid": os.environ["APPLE_API_KEY"], "typ": "JWT"})


def call(method, path, body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body else None,
                                 headers={"Authorization": "Bearer " + token(), "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        sys.exit(f"App Store Connect {method} {path} -> {e.code}: {e.read().decode()[:1500]}")


def setenv(name, value, mask=False):
    if mask:
        print(f"::add-mask::{value}")
    with open(os.environ["GITHUB_ENV"], "a") as f:
        f.write(f"{name}={value}\n")


def create():
    ident = os.environ["BUNDLE_ID"]
    found = [b for b in call("GET", f"/bundleIds?filter[identifier]={ident}&limit=200")["data"]
             if b["attributes"]["identifier"] == ident]
    if found:
        bundle_id = found[0]["id"]
    else:
        bundle_id = call("POST", "/bundleIds", {"data": {"type": "bundleIds", "attributes": {
            "identifier": ident, "name": "PDF Stift", "platform": "IOS"}}})["data"]["id"]
        print("App-ID angelegt:", ident)

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    csr = (x509.CertificateSigningRequestBuilder()
           .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "PDF Stift CI")]))
           .sign(key, hashes.SHA256()))
    cert_data = call("POST", "/certificates", {"data": {"type": "certificates", "attributes": {
        "certificateType": "DISTRIBUTION",
        "csrContent": csr.public_bytes(serialization.Encoding.PEM).decode()}}})["data"]
    cert_id = cert_data["id"]
    setenv("ASC_CERT_ID", cert_id)
    cert = x509.load_der_x509_certificate(base64.b64decode(cert_data["attributes"]["certificateContent"]))
    print("Zertifikat angelegt:", cert.subject.rfc4514_string())

    password = secrets.token_urlsafe(18)
    enc = (serialization.PrivateFormat.PKCS12.encryption_builder()
           .kdf_rounds(50000)
           .key_cert_algorithm(pkcs12.PBES.PBESv1SHA1And3KeyTripleDESCBC)
           .hmac_hash(hashes.SHA1())
           .build(password.encode()))
    p12 = pkcs12.serialize_key_and_certificates(b"PDF Stift CI", key, cert, None, enc)

    prof = call("POST", "/profiles", {"data": {"type": "profiles",
        "attributes": {"name": f"PDF Stift CI {os.environ.get('GITHUB_RUN_ID', int(time.time()))}", "profileType": "IOS_APP_STORE"},
        "relationships": {"bundleId": {"data": {"type": "bundleIds", "id": bundle_id}},
                          "certificates": {"data": [{"type": "certificates", "id": cert_id}]}}}})["data"]
    setenv("ASC_PROFILE_ID", prof["id"])
    print("Profil angelegt:", prof["attributes"]["name"])

    setenv("IOS_CERTIFICATE", base64.b64encode(p12).decode(), mask=False)
    setenv("IOS_CERTIFICATE_PASSWORD", password, mask=True)
    setenv("IOS_MOBILE_PROVISION", prof["attributes"]["profileContent"])


def cleanup():
    if os.environ.get("ASC_PROFILE_ID"):
        call("DELETE", f"/profiles/{os.environ['ASC_PROFILE_ID']}")
        print("Profil gelöscht")
    if os.environ.get("ASC_CERT_ID"):
        call("DELETE", f"/certificates/{os.environ['ASC_CERT_ID']}")
        print("Zertifikat widerrufen")


if __name__ == "__main__":
    {"create": create, "cleanup": cleanup}[sys.argv[1]]()
