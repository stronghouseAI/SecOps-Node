# 🛡️ SecOps-Node (Local AI Security Station)

> **A completely offline, specialized AI terminal for Red Team and Blue Team operations.** > *Powered by Ollama, LangChain, and Streamlit.*

![SecOps Terminal](https://via.placeholder.com/800x400.png?text=Upload+Your+Screenshot+Here)
*(Tip: Replace this link with one of your actual screenshots!)*

## 📋 Overview

**SecOps-Node** is a local Deployment Kit that turns any Linux laptop into an air-gapped Security Operations Center. It uses Retrieval-Augmented Generation (RAG) to ground its answers in real security frameworks (MITRE ATT&CK, OWASP) and switches between specialized neural models for offensive and defensive tasks.

It is designed to be **100% private** and **offline-capable**.

## 🚀 Features

* **⚔️ Red Team Mode:**
    * **Engine:** `dolphin-mistral` (Uncensored, high-performance).
    * **Focus:** Exploit generation, payload crafting, penetration testing methodology, TTP analysis.
* **🛡️ Blue Team Mode:**
    * **Engine:** `llama3` (Meta's latest, high reasoning).
    * **Focus:** Log analysis, mitigation strategies, incident response, mapping attacks to MITRE Enterprise.
* **🧠 Local Knowledge Base:**
    * Built-in vector database (`ChromaDB`) that ingests MITRE STIX data and OWASP documentation.
    * No hallucinations—answers are grounded in verified security data.
* **🔌 Offline & Private:**
    * Runs locally on your hardware. No data is sent to the cloud.
    * Perfect for sensitive engagements or air-gapped networks.
* **📟 Retro Terminal UI:**
    * Distraction-free, high-contrast "Hacker" aesthetic.

## 📦 Installation (The Easy Way)

If you just want to **use** the tool, download the "Deployment Kit" from the Releases page.

1.  Go to the **[Releases Page](../../releases/latest)**.
2.  Download `SecOps_Deployment_Kit.zip`.
3.  Unzip it on your Linux machine (or WSL).
4.  Open a terminal in the folder and run:
    ```bash
    chmod +x setup.sh run_app.sh
    ./setup.sh
    ```
    *(This will install Python dependencies and download the necessary Ollama models ~8GB).*

5.  **Launch the App:**
    ```bash
    ./run_app.sh
    ```

## 🛠️ Installation (For Developers)

If you want to modify the code or contribute:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/stronghouseAI/SecOps-Node.git](https://github.com/stronghouseAI/SecOps-Node.git)
    cd SecOps-Node
    ```

2.  **Install Ollama:**
    Follow instructions at [ollama.com](https://ollama.com).

3.  **Pull the Models:**
    ```bash
    ollama pull llama3
    ollama pull dolphin-mistral
    ```

4.  **Setup Virtual Environment:**
    ```bash
    python3 -m venv ai_env
    source ai_env/bin/activate
    pip install -r requirements.txt
    ```

5.  **Build the Database:**
    ```bash
    python3 ingest_ops.py
    ```

6.  **Run:**
    ```bash
    streamlit run sec_ops.py
    ```

## 🎮 Usage

### Switching Modes
Use the sidebar to toggle between **BLUE_TEAM** and **RED_TEAM**.
* **Blue Team:** The AI assumes the persona of a SOC Analyst. It is cautious, factual, and prioritizes defense.
* **Red Team:** The AI assumes the persona of an Offensive Security Researcher. It provides direct technical answers for testing and validation.

### Data Ingestion
To update the knowledge base with new data:
1.  Drop `.txt`, `.md`, or `.json` files into the project folder.
2.  Run `python3 ingest_ops.py`.
3.  Restart the application.

## ⚠️ Disclaimer

**This tool is for educational and authorized security testing purposes only.**
The creators of SecOps-Node are not responsible for any misuse of this software. Ensure you have explicit permission before testing any system.

---

**Repo maintained by [stronghouseAI](https://github.com/stronghouseAI)**
