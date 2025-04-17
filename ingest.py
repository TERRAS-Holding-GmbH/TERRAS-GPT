# ingest.py

import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

def load_excel_files(directory):
    docs = []
    for filename in os.listdir(directory):
        if filename.endswith(".xlsx"):
            print(f"🔍 Überprüfe Datei: {filename}")
            filepath = os.path.join(directory, filename)
            try:
                df = pd.read_excel(filepath, engine="openpyxl")  # oder andere Engine, falls nötig
                text = df.to_string(index=False)  # Hier wird der gesamte Inhalt der Excel-Datei als Text extrahiert
                
                # Erstelle ein Document-Objekt und füge es zur Liste hinzu
                document = Document(page_content=text, metadata={"source": filename})
                docs.append(document)
                
            except Exception as e:
                print(f"❌ Fehler bei {filename}: {e}")
    return docs


def ingest_documents():
    docs = load_excel_files("excel_dateien")
    splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=10)  # Text aufteilen
    split_docs = splitter.split_documents(docs)  # Teilt die Dokumente in kleinere Abschnitte

    embeddings = OpenAIEmbeddings()  # Erstelle Embeddings
    vectordb = FAISS.from_documents(split_docs, embeddings)  # Vektorstore aus den Dokumenten erstellen
    vectordb.save_local("vectorstore")  # Speichert den Vektorstore lokal
    print("✅ Vektorstore gespeichert.")

if __name__ == "__main__":
    ingest_documents()
