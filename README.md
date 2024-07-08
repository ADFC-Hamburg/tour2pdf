# ADFC Tour2pdf

Ein Script aus dem ADFC Tourenportal ein PDF macht.

# Development


Instalation: Linux mit Python
```
./create-venv.sh

```

Starten mit:
```
./.venv/bin/fastapi dev ./tour2pdf.py
```

Dann einen Browser auf:

http://127.0.0.1:8000/


aufrufen da gibt es eine Doku.

Alternativ:

http://127.0.0.1:8000/api/pdf?unitKey=158&eventType=Radtour&limit=6&beginning=2024-07-07

zeigt gleich eine PDF Datei an.

Wichtige Doku-Seiten:

* https://adfcevents.docs.apiary.io/
* https://weasyprint.org/
* https://fastapi.tiangolo.com/

# Docker Image erstellen / nutzen

```
docker build --progress=plain -t tour2pdf .
docker run --expose 8000 tour2pdf
```

