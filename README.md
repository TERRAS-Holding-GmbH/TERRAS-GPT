# TERRAS-GPT

TERRAS-GPT ist ein KI-gestütztes System zur Analyse und Beantwortung von Fragen zu Excel-basierten KPI- und Reporting-Dateien. Es nutzt OpenAI-Modelle und speichert Dokumente als Vektoren, um schnelle und präzise Antworten zu ermöglichen.

## Features

- Automatisches Einlesen und Vektorisieren von Excel-Dateien
- Chatbot für Fragen zu den importierten Daten
- Integration mit Microsoft Graph API und SharePoint
- Nutzung von OpenAI GPT-Modellen

## Projektstruktur

```
.
├── .env                  # Umgebungsvariablen (nicht ins Repo pushen!)
├── .gitignore
├── chatbot.py            # Chatbot-Interface für Fragen zu den Excel-Dateien
├── ingest.py             # Importiert und vektorisiert Excel-Dateien
├── listFiles.py          # Listet Dateien aus SharePoint auf
├── openaitest.py         # Testet Retrieval und Antwortgenerierung
├── test.py               # Testet Authentifizierung und API-Zugriff
├── excel_dateien/        # Ablage für Excel-Dateien
└── vectorstore/          # Persistenter Vektorstore (FAISS)
```

## Voraussetzungen

- Python 3.8+
- OpenAI API Key
- Microsoft Azure App-Registrierung (Client ID, Tenant ID, Secret)
- Abhängigkeiten aus `requirements.txt` (z.B. langchain, openai, msal, pandas, python-dotenv, requests, openpyxl)

## Installation

1. Repository klonen:
   ```sh
   git clone https://github.com/TERRAS-Holding-GmbH/TERRAS-GPT.git
   cd TERRAS-GPT
   ```

2. Python-Umgebung einrichten und Abhängigkeiten installieren:
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. `.env`-Datei mit Zugangsdaten anlegen (siehe Beispiel in der Datei).

4. Excel-Dateien in den Ordner `excel_dateien/` legen.

## Nutzung

### 1. Excel-Dateien einlesen und Vektorstore erstellen

```sh
python ingest.py
```

### 2. Chatbot starten

```sh
python chatbot.py
```

### 3. SharePoint-Dateien auflisten

```sh
python listFiles.py
```

### 4. Testskripte

- `test.py`: Testet Authentifizierung und API-Zugriff.
- `openaitest.py`: Testet Retrieval und Antwortgenerierung.

## Hinweise

- Die `.env`-Datei ist durch `.gitignore` geschützt und wird nicht ins Repository gepusht.
- Sensible Daten wie API-Keys niemals öffentlich teilen!

## Lizenz

MIT License

