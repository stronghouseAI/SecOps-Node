#!/bin/bash

# --- CONFIGURATION ---
BLUE_TEAM_MODEL="llama3"
RED_TEAM_MODEL="dolphin-mistral" # Changed to the fast one we just fixed
ENV_NAME="ai_env"

echo "/// SECOPS NODE: DEPLOYMENT PROTOCOL ///"

# 1. Check/Install Python3
if ! command -v python3 &> /dev/null; then
    echo "[!] Python3 not detected. Please install (sudo apt install python3)"
    exit 1
fi

# 2. Check/Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "[*] Installing Ollama (The Brain)..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "[+] Ollama detected."
fi

# 3. Pull Neural Models (The Heavy Lifting)
echo "[*] Downloading Neural Models (This requires internet once)..."
ollama pull $BLUE_TEAM_MODEL
ollama pull $RED_TEAM_MODEL

# 4. Create Isolated Environment
if [ ! -d "$ENV_NAME" ]; then
    echo "[*] Creating Virtual Environment..."
    python3 -m venv $ENV_NAME
fi

# 5. Activate & Install Libraries
echo "[*] Installing Python Dependencies..."
source $ENV_NAME/bin/activate
pip install -r requirements.txt

# 6. Build Knowledge Base
echo "[*] Ingesting Security Data..."
python ingest_ops.py

echo "/// DEPLOYMENT COMPLETE ///"
echo "To run the app, type: ./run_app.sh"
