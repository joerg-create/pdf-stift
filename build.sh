#!/bin/sh
# Erzeugt index.html (eigenständige App) aus app.html
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
  printf '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n'
  printf '<meta name="apple-mobile-web-app-title" content="PDF Stift">\n'
  printf '<link rel="manifest" href="manifest.webmanifest">\n<link rel="apple-touch-icon" href="icon.svg">\n<link rel="icon" href="icon.svg">\n'
  printf '<style>*,*::before,*::after{box-sizing:border-box}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%%}[hidden]{display:none!important}</style>\n'
  printf '</head>\n<body>\n'
  sed "s|https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/|lib/|g; s|https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/|lib/|g" app.html
  printf '\n<script>if("serviceWorker" in navigator&&location.protocol==="https:")navigator.serviceWorker.register("sw.js").catch(()=>{});</script>\n'
  printf '</body>\n</html>\n'
} > index.html
