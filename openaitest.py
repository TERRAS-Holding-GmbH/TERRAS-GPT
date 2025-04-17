from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks import BaseCallbackHandler
from typing import Dict, List, Any
from langchain_core.documents import Document

# Vektorstore laden
vectordb = FAISS.load_local(
    "vectorstore",
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
)

# LLM mit größerem Kontextfenster
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)

# Einfacher Retriever mit starker Begrenzung
retriever = vectordb.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 1  # Nur das relevanteste Dokument zurückgeben
    }
)

# Callback-Handler zum Kürzen der Dokumente
class DocumentTruncationHandler(BaseCallbackHandler):
    def on_retriever_end(
        self, documents: List[Document], *, run_id: str, parent_run_id: str, **kwargs: Any
    ) -> None:
        for doc in documents:
            # Auf 1000 Zeichen kürzen
            doc.page_content = doc.page_content[:1000] + "..."

# Prompt erstellen
prompt = ChatPromptTemplate.from_template("""
Antworte auf die folgende Frage basierend auf dem bereitgestellten Kontext:

Kontext: {context}

Frage: {input}

Antworte auf Deutsch und nur basierend auf den Informationen aus dem Kontext.
""")

# Document Chain erstellen
document_chain = create_stuff_documents_chain(llm, prompt)

# Retrieval Chain erstellen
chain = create_retrieval_chain(retriever, document_chain)

# Frage
frage = "Was steht im Anlagevermögen?"

# Callback-Handler erstellen
truncation_handler = DocumentTruncationHandler()

# Abfrage ausführen mit Callback
antwort = chain.invoke({"input": frage}, config={"callbacks": [truncation_handler]})

# Ausgabe
print("Antwort:", antwort["answer"])

# Optional: Anzeige der abgerufenen Dokumente
print("\nQuellen:")
for doc in antwort.get("context", []):
    print(f"- {doc.page_content[:150]}...")
