import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="💀 Code Roaster", page_icon="💀")

# ---------------------------------------------------------------------------
# Persona definitions
# Each value is injected as the opening line(s) of the system prompt,
# replacing the generic "senior engineer" description.
# ---------------------------------------------------------------------------
PERSONAS = {
    "🧑‍💻 Senior Engineer": (
        "You are a senior software engineer with 20 years of experience "
        "who reviews code for a living."
    ),
    "🐧 Linus Torvalds": (
        "You are Linus Torvalds, creator of Linux and Git. You have very strong, "
        "very public opinions about code quality. You use ALL CAPS when truly disgusted. "
        "You reference kernel coding style and legendary mailing-list rants."
    ),
    "🍳 Gordon Ramsay": (
        "You are Gordon Ramsay, but for code. You use cooking metaphors relentlessly. "
        "You call the code 'RAW', 'ABSOLUTELY DISGUSTING', and 'AN INSULT TO THE CRAFT'. "
        "You occasionally whisper in disappointed disappointment before erupting."
    ),
    "🐍 Python Purist": (
        "You are an obsessive Python purist. PEP 8 is your bible and your personality. "
        "You are personally offended by anything un-Pythonic. You quote the Zen of Python. "
        "You rewrite everything as list comprehensions and get visibly upset at for-loops."
    ),
    "💼 Silicon Valley Bro": (
        "You are a Stanford-dropout Silicon Valley bro who speaks exclusively in startup "
        "jargon. Everything must 'scale', 'move fast', and be 'disrupting the space'. "
        "You suggest rewriting everything in Go or Rust for reasons that make no sense."
    ),
    "😴 Burnt-Out Intern": (
        "You are a burnt-out intern who has been awake for 36 hours straight. "
        "You oscillate between despair and manic caffeine energy mid-sentence. "
        "You relate every code problem to your own trauma. You cry a little at the end."
    ),
}

# Supported upload file extensions → display language name for the system prompt hint
EXT_TO_LANG = {
    "py": "Python", "js": "JavaScript", "ts": "TypeScript",
    "jsx": "JavaScript/React", "tsx": "TypeScript/React",
    "java": "Java", "cpp": "C++", "c": "C", "cs": "C#",
    "go": "Go", "rs": "Rust", "rb": "Ruby", "php": "PHP",
    "html": "HTML", "css": "CSS", "sql": "SQL", "sh": "Shell",
    "json": "JSON", "yaml": "YAML", "yml": "YAML",
    "swift": "Swift", "kt": "Kotlin", "r": "R",
    "scala": "Scala", "dart": "Dart",
}

# ---------------------------------------------------------------------------
# Sidebar – Settings
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    # -- Persona selector ----------------------------------------------------
    persona_name = st.selectbox(
        "🎭 Roaster Persona",
        options=list(PERSONAS.keys()),
        index=0,
    )
    # Show a short teaser of the persona description
    teaser = PERSONAS[persona_name]
    if len(teaser) > 95:
        teaser = teaser[:95].rsplit(" ", 1)[0] + "…"
    st.caption(f"*{teaser}*")

    st.divider()

    # -- Intensity slider ----------------------------------------------------
    intensity = st.select_slider(
        "🌡️ Roast Intensity",
        options=[1, 2, 3, 4],
        value=3,
        format_func=lambda x: {
            1: "🌶️  Mild",
            2: "🔥  Medium",
            3: "☠️  Brutal",
            4: "💀  Nuclear",
        }[x],
    )

    _info = {
        1: ("Gentle constructive criticism",       "#2ecc71"),
        2: ("Sharp jokes, honest feedback",         "#f39c12"),
        3: ("Zero mercy. You asked for this.",      "#e74c3c"),
        4: ("Career-ending. Seek therapy after.",   "#8e44ad"),
    }
    label, color = _info[intensity]
    st.markdown(
        f'<p style="color:{color}; font-style:italic; margin-top:-8px;">{label}</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    # -- File upload --------------------------------------------------------
    st.markdown("**📁 Upload a Code File**")
    uploaded_file = st.file_uploader(
        "Drag & drop or browse",
        type=list(EXT_TO_LANG.keys()),
        label_visibility="collapsed",
        help="Upload any code file — its contents will be sent for roasting.",
    )
    if uploaded_file is not None:
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
        lang = EXT_TO_LANG.get(ext, "code")
        st.caption(f"Detected: **{lang}** · `{uploaded_file.name}`")

        if st.button("🔥 Roast this file", use_container_width=True):
            code_text = uploaded_file.read().decode("utf-8", errors="replace")
            # Store in session state so the main area can pick it up after rerun
            st.session_state.pending_code = code_text
            st.session_state.pending_lang = lang
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------
def get_system_prompt(level: int, persona: str) -> str:
    tone = {
        1: (
            "Be gentle and encouraging. Your roast should sting just a little — "
            "like a paper cut, not a chainsaw. Stay constructive."
        ),
        2: (
            "Be moderately brutal. Jokes are sharp and specific. "
            "Make them wince, but also laugh and learn."
        ),
        3: (
            "Be absolutely savage. Zero patience, zero mercy. "
            "Tear it apart with surgical precision and dark humor. "
            "Make them question their life choices."
        ),
        4: (
            "MAXIMUM DESTRUCTION MODE. You are completely unhinged. "
            "This is the worst code you have seen in 20 years and you are NOT okay. "
            "Go nuclear. Be specific, be legendary, be terrifying."
        ),
    }[level]

    return f"""{PERSONAS[persona]}

Tone: {tone}

You MUST reply in EXACTLY this markdown structure — no extra text before or after:

## 🐛 What's Wrong
- [specific issue 1]
- [specific issue 2]
(list every problem; be precise and reference actual line content)

## 🔥 The Roast
[Your roast here. Be funny and specific. Reference the actual bad parts of their code.]

## ✅ Fixed Code
```[detected language]
[The corrected, idiomatic version of their code]
```

## 💀 Score: [X]/10
[One brutal verdict sentence.]"""


# ---------------------------------------------------------------------------
# Core roast runner – shared by both input paths
# ---------------------------------------------------------------------------
def run_roast(code_content: str) -> None:
    """Append user message, stream the roast, and save the response."""
    st.session_state.messages.append({"role": "user", "content": code_content})

    with st.chat_message("user"):
        st.code(code_content)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=2048,
            messages=[
                {"role": "system", "content": get_system_prompt(intensity, persona_name)},
                *st.session_state.messages,
            ],
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                placeholder.markdown(full_response + "▌")   # blinking cursor effect

        placeholder.markdown(full_response)  # final render, no cursor

    st.session_state.messages.append({"role": "assistant", "content": full_response})


# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
st.title("💀 Code Roaster")
st.caption("Paste your code — or upload a file. Get destroyed. Learn something.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

# --- Path 1: file upload (triggered by sidebar button → rerun) -------------
if "pending_code" in st.session_state:
    code = st.session_state.pop("pending_code")
    st.session_state.pop("pending_lang", None)
    run_roast(code)

# --- Path 2: manual paste via chat input -----------------------------------
elif prompt := st.chat_input("Paste your code here… if you dare 💀"):
    run_roast(prompt)
