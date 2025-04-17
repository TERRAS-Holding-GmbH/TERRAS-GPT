# chatbot.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()

def start_chat():
    vectordb = FAISS.load_local(
        "vectorstore",  # Pfad zum Vektorstore
        OpenAIEmbeddings(),  # Verwende OpenAI-Embeddings
        allow_dangerous_deserialization=True  # Da der Vektorstore von dir erstellt wurde
    )
    retriever = vectordb.as_retriever()  # Vektorstore als Retriever verwenden
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),  # Verwende das OpenAI-Modell für Fragen-Antworten
        retriever=retriever
    )

    print("❓ Frage mich etwas zu den Excel-Dateien:")
    while True:
        query = input(">> ")
        if query.lower() in ["exit", "quit"]:  # Beende die Sitzung, wenn 'exit' oder 'quit' eingegeben wird
            break
        answer = qa_chain.run(query)  # Beantworte die Frage mithilfe des Vektorstores
        print("💬", answer)

if __name__ == "__main__":
    start_chat()
