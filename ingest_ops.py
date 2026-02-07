import os
import requests
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datasets import load_dataset

# --- CONFIGURATION ---
DB_DIR = "sec_ops_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- TARGET DATASETS (The "Best" for SecOps) ---
# We use specific security datasets from HF + Official Frameworks
HF_DATASETS = [
    # (Dataset ID, Column containing the text)
    ("daloza/security-vulnerabilities", "description"),  # Huge CVE list
    ("midas/sec-data", "text"),                          # General security text
]

URL_SOURCES = {
    "MITRE_ENTERPRISE": "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json",
    "OWASP_TOP10": "https://raw.githubusercontent.com/OWASP/Top10/master/2021/docs/index.md"
}

def setup_db():
    print(">> INITIALIZING VECTOR DATABASE...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return embeddings

def ingest_hf_datasets(embeddings):
    print(">> CONTACTING HUGGING FACE NEURAL NET...")
    docs = []

    for ds_name, text_col in HF_DATASETS:
        try:
            print(f"   [+] Downloading Stream: {ds_name}...")
            # We stream it to avoid crashing RAM, taking first 2000 entries per set
            dataset = load_dataset(ds_name, split="train", streaming=True)

            count = 0
            for row in dataset:
                if count > 2000: break # Limit for laptop performance
                text = row.get(text_col, "")
                if len(text) > 50:
                    docs.append(Document(page_content=text, metadata={"source": f"HF::{ds_name}"}))
                    count += 1
            print(f"   [+] Ingested {count} records from {ds_name}")
        except Exception as e:
            print(f"   [!] Failed to load {ds_name}: {e}")

    return docs

def ingest_url_sources():
    print(">> DOWNLOADING OFFICIAL FRAMEWORKS...")
    docs = []

    # MITRE
    try:
        resp = requests.get(URL_SOURCES["MITRE_ENTERPRISE"])
        data = json.loads(resp.text)
        objects = data.get('objects', [])
        mitre_text = "\n".join([f"{obj.get('name', 'UNK')}: {obj.get('description', '')}" for obj in objects if 'description' in obj])
        docs.append(Document(page_content=mitre_text, metadata={"source": "MITRE_ATTACK"}))
        print("   [+] MITRE ATT&CK Downloaded")
    except Exception as e: print(f"   [!] MITRE Failed: {e}")

    # OWASP
    try:
        resp = requests.get(URL_SOURCES["OWASP_TOP10"])
        docs.append(Document(page_content=resp.text, metadata={"source": "OWASP_TOP_10"}))
        print("   [+] OWASP Downloaded")
    except Exception as e: print(f"   [!] OWASP Failed: {e}")

    return docs

def main():
    embeddings = setup_db()

    # 1. Gather Data
    hf_docs = ingest_hf_datasets(embeddings)
    url_docs = ingest_url_sources(embeddings)
    all_docs = hf_docs + url_docs

    if not all_docs:
        print("[!] No data found. Aborting.")
        return

    # 2. Split & Vectorize
    print(f">> VECTORIZING {len(all_docs)} DOCUMENTS (This will take time)...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)

    # 3. Save to Disk
    if os.path.exists(DB_DIR):
        print("   [i] Appending to existing database...")

    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_DIR)
    print(f"\n>> SUCCESS. KNOWLEDGE BASE UPDATED. ({len(chunks)} chunks stored)")

if __name__ == "__main__":
    main()
