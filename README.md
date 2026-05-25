# 💀 Code Roaster

A Streamlit web app that lets you paste your code and get **brutally roasted** by an AI senior developer with 20 years of experience and zero patience for bad code.

## Demo

> 📸 *Replace the placeholders below with your screenshots saved in the `assets/` folder*

<!-- Screenshot 1: e.g. the input screen / landing view -->
[Demo 1](assets/demo1.png) -->

<!-- Screenshot 2: e.g. the roast response in action -->
[Demo 2](assets/demo2.png) -->

## What It Does

- Paste any code snippet into the chat input
- The app sends it to **GPT-4o-mini** with a savage system prompt
- You get a funny, specific roast of your code's errors and bad practices
- Every roast ends with the actual fix, so you learn something too
- Supports multi-turn conversation so you can keep the session going

## Tech Stack

| Tool | Purpose |
|------|---------|
| [Streamlit](https://streamlit.io/) | Web UI / chat interface |
| [OpenAI API](https://platform.openai.com/) | GPT-4o-mini for code review |
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

Type or paste your code into the chat box at the bottom of the page and hit Enter. Brace yourself.

## Project Structure

```
Agent1/
├── app.py            # Main Streamlit app
├── requirements.txt  # Python dependencies
├── .env              # API key (NOT committed — see .gitignore)
├── .gitignore        # Ignores .env and __pycache__
└── README.md         # This file
```
