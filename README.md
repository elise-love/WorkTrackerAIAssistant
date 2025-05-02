# Elfie ‑ Work‑Tracker AI Assistant 🧚🏻‍♀️
*A 10‑second journal to keep my daily work on track.*

## Elevator Pitch
✨ Elfie is a lightweight desktop AI assistant that can save ur time planning and logging stuff everyday.


##  Project Stage & Roadmap
|     Stage     |                  Goal                   |      Status    |
|---------------|-----------------------------------------|----------------|
| **Stage 1**   | Minimal UI: send prompt ➜ get reply    | ⏳ In progress |
| **Stage 2**   | Add templates (to‑do list, work log)    |       🔜       |
| **Stage 2.5** | Decide log storage (SQLite vs. JSON)    |       🔜       |
| **Stage 3**   | Model persona, command stability tests  |       🔜       |
| **Stage 4**   | History viewer (per day) | 2025‑07‑25   |       🔜       |
| **Stage 5**   | Extras: token meter, UI themes          |       🔜       |


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
cp .env.example .env   # put your OPENAI_API_KEY inside
python -m elfie        # launches the UI
```

##Project Structure
elfie/
├─ src/
│  └─ elfie/
│     ├─ __main__.py      
│     ├─ ui/              
│     ├─ core/            
│     └─ config.py        
├─ tests/
├─ data/               
├─ docs/
│  └─ images/
├─ .env.example
└─ README.md

