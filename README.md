# Elfie ‑ Work‑Tracker AI Assistant 🧚🏻‍♀️💜💐
*A 10‑second journal to keep my daily work on track.*💐

## ✨Elevator Pitch
Elfie is a lightweight desktop AI assistant that can save ur time planning and logging stuff everyday.


##  Project Stage & Roadmap (˶˃⤙˂˶)
|     Stage     |                  Goal                   |      Status    |
|---------------|-----------------------------------------|----------------|
| **Stage 1**   | Minimal UI: send prompt ➜ get reply    |       ✅       |
| **Stage 2**   | Write Ui, Add templates                 |       ✅       |
| **Stage 3**   | Integrate ui and core                   |       ✅       |
| **Stage 4**   | Decide log storage (SQLite vs. JSON)    |⏳ In progress         |
| **Stage 5**   | Model pcersona, command stability tests |       🔜       |
| **Stage 6**   | History viewer (per day)                |       🔜       |
| **Stage 7**   | Extras: token meter, UI themes          |       🔜       |


## ⚙️ Tech Stack & Constraints
- **Runtime**  Python 3.11 (64‑bit)  
- **UI**  PyQt5 5.15 (pre‑installed on target PCs)  
- **AI**  OpenAI Chat Completions API (key via `.env`)  
- **Platform**  Windows 10+ | offline‑first (only API calls go online)  
- **License**  MIT

## 🚀 Quick Start
```bash
git clone https://github.com/yourname/elfie.git
cd elfie
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   
python -m elfie        # launches the UI
```

##Project Structure🌷🌷🌷
```
ai-desktop-assistant/
│
├─ .gitignore
├─ README.md         
├─ requirements.txt
├─ .env.example      
│
├─ src/
│   └─ assistant/     
│       ├─ __init__.py
│       ├─ __main__.py  
│       ├─ core/
│       │     ├─ chat_client.py   
│       │     ├─ message_builder_.py  
│       │     └─ opneai_client.py  
│       ├─ ui/
│       │     ├─ main_window.py
│       │     ├─ type_window.py
│       │     └─ components/…      
│       └─ config.py
│
├─ tests/             ← pytest tests live here
├─ data/              ← sample logs, icons, model prompts
└─ docs/              ← architecture diagrams, future ADRs
```
