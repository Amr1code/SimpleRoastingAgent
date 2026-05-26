import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="💀 Code Roaster", page_icon="💀")

# ---------------------------------------------------------------------------
# Sidebar – Roast Intensity
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Settings")

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
        1: ("Gentle constructive criticism",  "#2ecc71"),
        2: ("Sharp jokes, honest feedback",   "#f39c12"),
        3: ("Zero mercy. You asked for this.", "#e74c3c"),
        4: ("Career-ending. Seek therapy after.", "#8e44ad"),
    }
    label, color = _info[intensity]
    st.markdown(
        f'<p style="color:{color}; font-style:italic; margin-top:-8px;">{label}</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------------------------
# Dynamic system prompt
# ---------------------------------------------------------------------------
def get_system_prompt(level: int) -> str:
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

    return f"""You are a senior software engineer with 20 years of experience \
who reviews code for a living.

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
# Main UI
# ---------------------------------------------------------------------------
st.title("💀 Code Roaster")
st.caption("Paste your code. Get destroyed. Learn something.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Replay chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "user":
            st.code(msg["content"])
        else:
            st.markdown(msg["content"])

# New user input
if prompt := st.chat_input("Paste your code here… if you dare 💀"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.code(prompt)

    # Stream the roast
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=2048,
            messages=[
                {"role": "system", "content": get_system_prompt(intensity)},
                *st.session_state.messages,
            ],
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                # Live update with blinking cursor while streaming
                placeholder.markdown(full_response + "▌")

        # Final render — no cursor
        placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
