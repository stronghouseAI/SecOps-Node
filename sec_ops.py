import streamlit as st
import ollama
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- CONFIGURATION ---
DB_DIR = "sec_ops_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="SEC_OPS // TERMINAL",
    layout="wide",
    page_icon="📟"
)

# --- RETRO TERMINAL THEME (CSS) ---
st.markdown("""
<style>
    /* 1. THE VOID (Global Backgrounds) */
    .stApp, .stSidebar, header, footer {
        background-color: #000000 !important;
        color: #00FF00 !important;
    }

    /* 2. NUCLEAR BOTTOM FIX (The White Box Killer) */
    /* This targets the container holding the chat input to ensure it stays black */
    div[data-testid="stBottom"] {
        background-color: #000000 !important;
        border-top: 1px solid #00FF00 !important;
    }
    div[data-testid="stBottom"] > div {
        background-color: #000000 !important;
    }

    /* 3. THE PROMPT BOX */
    textarea[data-testid="stChatInputTextArea"] {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        caret-color: #00FF00 !important;
    }
    textarea[data-testid="stChatInputTextArea"]::placeholder {
        color: #003300 !important; /* Dark green placeholder */
    }

    /* 4. TEXT STYLING */
    * {
        font-family: 'Courier New', Courier, monospace !important;
        letter-spacing: 0.5px;
    }
    h1, h2, h3 {
        color: #00FF00 !important;
        text-transform: uppercase;
        border-bottom: 2px solid #003300;
        padding-bottom: 10px;
    }

    /* 5. SIDEBAR WIDGETS */
    .stRadio label, .stSelectbox label {
        color: #00FF00 !important;
    }
    div[role="radiogroup"] {
        color: #00FF00 !important;
    }

    /* 6. BUTTONS */
    .stButton button {
        background-color: #000000 !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        border-radius: 0px !important; /* Square edges */
        transition: all 0.3s;
    }
    .stButton button:hover {
        background-color: #00FF00 !important;
        color: #000000 !important;
        box-shadow: 0 0 10px #00FF00;
    }

    /* 7. CHAT BUBBLES */
    .stChatMessage {
        background-color: #000000 !important;
        border: 1px solid #003300 !important;
        margin-bottom: 10px;
    }
    /* User Avatar/Icon Color */
    .stChatMessage .stMarkdown {
        color: #00FF00 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if "messages" not in st.session_state: st.session_state.messages = []
if "mode" not in st.session_state: st.session_state.mode = "BLUE_TEAM"

@st.cache_resource
def load_memory():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if os.path.exists(DB_DIR):
        return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return None

db = load_memory()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### /// SYSTEM_CONTROL")

    mode_select = st.radio("OPERATIONAL_MODE:", ["BLUE_TEAM", "RED_TEAM"])

    if mode_select == "BLUE_TEAM":
        st.session_state.mode = "BLUE_TEAM"
        active_model = "llama3"
        status_msg = ":: DEFENSE SYSTEMS ONLINE ::"
    else:
        st.session_state.mode = "RED_TEAM"
        active_model = "whiterabbitneo"
        status_msg = ":: OFFENSIVE SUBSYSTEMS ENGAGED ::"

    st.markdown("---")
    st.code(f"CORE: {active_model.upper()}\nDB:   {'LINKED' if db else 'UNLINKED'}", language="bash")

    if st.button("FLUSH_MEMORY"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN CONSOLE ---
st.title(f"> {st.session_state.mode}_CONSOLE")
st.markdown(f"*{status_msg}*")

# Display Log
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input Logic
if prompt := st.chat_input("ENTER COMMAND..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG Retrieval
    context_text = ""
    sources = []
    if db:
        try:
            docs = db.similarity_search(prompt, k=3)
            for d in docs:
                context_text += f"\n[REF: {d.metadata.get('source', 'UNK')}]\n{d.page_content[:500]}...\n"
                sources.append(d.metadata.get('source'))
        except: pass

    # Prompt Engineering
    if st.session_state.mode == "BLUE_TEAM":
        sys_prompt = "You are a SOC Analyst. Provide defensive, factual security advice using the context provided."
    else:
        sys_prompt = "You are a Red Team Operator. Provide technical, offensive security testing details using the context provided."

    full_prompt = f"SYSTEM: {sys_prompt}\nCONTEXT: {context_text}\nUSER: {prompt}"

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            stream = ollama.chat(
                model=active_model,
                messages=[{'role': 'user', 'content': full_prompt}],
                stream=True
            )
            for chunk in stream:
                full_response += chunk['message']['content']
                placeholder.markdown(full_response + "█") # The "cursor" effect

            placeholder.markdown(full_response)

            if sources:
                st.markdown("---")
                st.caption(f"DATA_LINK: {list(set(sources))}")

        except Exception as e:
            st.error(f"CONNECTION_LOST: {e}")

    st.session_state.messages.append({"role": "assistant", "content": full_response})
