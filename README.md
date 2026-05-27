# 💀 Code Roaster

A Streamlit web app that lets you paste **or upload** your code and get **brutally roasted** by an AI reviewer — choose your persona and intensity, then brace yourself.

## Demo

<!-- Screenshot 1: e.g. the input screen / landing view -->
[Demo 1](assets/demo1.png)
<!-- Screenshot 2: e.g. the roast response in action -->
[Demo 2](assets/demo2.png)

## What It Does

- **Paste or upload** any code snippet or file (`.py`, `.js`, `.ts`, `.java`, `.go`, `.rs`, and 20+ more)
- Choose a **Roaster Persona** — each one brings a completely different voice and personality to the roast
- Dial in the **Roast Intensity** from Mild to Nuclear
- The app sends your code to **GPT-4o-mini** with a combined persona + intensity system prompt
- You get a **streaming roast** with a blinking cursor as it generates
- Every roast ends with the actual fix, so you learn something too
- Supports **multi-turn conversation** so you can keep the session going

## Roaster Personas

| Persona | Personality |
|---------|-------------|
| 🧑‍💻 Senior Engineer | The default — 20 years of experience, zero tolerance for bad code |
| 🐧 Linus Torvalds | ALL CAPS rage, kernel coding style references, legendary mailing-list energy |
| 🍳 Gordon Ramsay | Cooking metaphors, "THIS CODE IS RAW", whispering disappointment before erupting |
| 🐍 Python Purist | PEP 8 as religion, Zen of Python quotes, personally offended by for-loops |
| 💼 Silicon Valley Bro | Startup jargon, everything must "scale", suggests rewriting in Rust for no reason |
| 😴 Burnt-Out Intern | 36 hours awake, oscillates between despair and caffeine mania, cries a little |

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Web UI / chat interface, file uploader |
| [OpenAI API](https://platform.openai.com/) | GPT-4o-mini for code review, streaming responses |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Load API key from `.env` |

## Setup

1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd Agent1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key**

   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

   The app will open in your browser at `http://localhost:8501`.

## Usage

### Pasting Code
Type or paste your code into the chat box at the bottom of the page and hit Enter.

### Uploading a File
Use the **📁 Upload a Code File** section in the sidebar — drag & drop or browse for any supported code file, then click **🔥 Roast this file**. The app auto-detects the language from the file extension.

**Supported extensions:** `.py` `.js` `.ts` `.jsx` `.tsx` `.java` `.cpp` `.c` `.cs` `.go` `.rs` `.rb` `.php` `.html` `.css` `.sql` `.sh` `.json` `.yaml` `.swift` `.kt` `.r` `.scala` `.dart`

### Changing Persona / Intensity
Use the sidebar controls before submitting. The persona and intensity apply to the **next** message you send — previous messages in the chat keep their original roast style.

## Project Structure

```
Agent1/
├── app.py            # Main Streamlit app
├── requirements.txt  # Python dependencies
├── .env              # API key (NOT committed — see .gitignore)
├── .gitignore        # Ignores .env and __pycache__
├── assets/           # Demo screenshots
└── README.md         # This file
```
