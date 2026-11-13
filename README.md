# PDF Stift

Einfacher PDF-Editor als Web-App: PDF öffnen, freihand zeichnen, gerade Linien ziehen,
krumme Striche begradigen, Text einfügen, als neues PDF speichern.
Läuft im Browser auf iPad, iPhone, Mac und Windows. Alles passiert lokal im Gerät,
das PDF wird nirgends hochgeladen.

**Online:** https://joerg-create.github.io/pdf-stift/

## Dateien
- `index.html` – die App (mit `lib/`, `manifest.webmanifest`, `sw.js`, `icon.svg`)
- `app.html` – Quelltext; `sh build.sh` erzeugt daraus `index.html`

## Benutzen
- **Mac/Windows:** Ordner irgendwo ablegen und `index.html` im Browser öffnen
  (Chrome, Edge, Safari, Firefox). Funktioniert ohne Internet.
- **iPad/iPhone:** Ordner auf einer HTTPS-Adresse bereitstellen (z. B. GitHub Pages),
  in Safari öffnen, „Teilen → Zum Home-Bildschirm“. Danach startet sie wie eine App
  und funktioniert auch offline.

## Bedienung
| Werkzeug | Taste | Funktion |
|---|---|---|
| Hand | H | Scrollen, nichts zeichnen |
| Stift | P | Freihand. Mit „Auto-gerade“ werden fast gerade Striche automatisch gerade |
| Linie | L | Gerade Linie, rastet bei 0°, 45°, 90° ein |
| Text | T | Auf die Seite tippen und schreiben; vorhandenen Text antippen = ändern, ziehen = verschieben |
| Radierer | E | Strich oder Text antippen bzw. darüberwischen |
| Begradigen | G | Macht den zuletzt gezeichneten Strich gerade |
| Zurück / Wiederholen | Strg/Cmd+Z, Strg/Cmd+Umschalt+Z | |
| Speichern | Strg/Cmd+S | Schreibt zurück in die geöffnete Datei (Chrome/Edge). Sonst Download bzw. auf iPad/iPhone Teilen-Menü → „In Dateien sichern“ |
| Speichern unter | Strg/Cmd+Umschalt+S | Als neue Datei speichern (Chrome/Edge) |
| Tabs | Alt+←/→ | Mehrere PDFs gleichzeitig offen; „+“ öffnet weitere, × schließt (bei ungespeicherten Änderungen erst „Verwerfen?“) |

## iCloud
Die PDFs liegen in iCloud Drive und werden von Apple zwischen allen Geräten abgeglichen.
- **Mac/Windows mit Chrome oder Edge:** „Öffnen“ → Datei im iCloud-Drive-Ordner wählen
  (Windows: App „iCloud für Windows“). „Speichern“ schreibt direkt in diese Datei zurück.
- **Mac mit Safari:** Öffnen aus iCloud Drive; Speichern landet im Download-Ordner
  (in Safari-Einstellungen kann man iCloud Drive als Download-Ort wählen).
- **iPhone/iPad:** „Öffnen“ zeigt die Dateien-App mit iCloud Drive. „Speichern“ öffnet das
  Teilen-Menü → „In Dateien sichern“ → gleichen Ordner wählen → „Ersetzen“.

Hinweis: Text nutzt die PDF-Standardschrift Helvetica (Umlaute, ß und € gehen; Emojis nicht).
