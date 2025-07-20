# Elfie ‑ Work‑Tracker AI Assistant 🧚🏻‍♀💜🌟
<br/>

## Customized AI assistant🤖: knows you THE best!🩶🤍🩶🤍

<br/>

## ✨Elevator Pitch
Elfie is a lightweight desktop AI assistant that can:
- save ur time planning 📃
- vibe logging ur daily routine and stuff 🖋️
- talk heart 2 heart with secretly in any style about literally anything 🥹
<br/><br/>
##  Project Stage & Roadmap (˶˃⤙˂˶)
|     Stage     |                  Goal                   |      Status    |
|---------------|-----------------------------------------|----------------|
| **Stage 1**   | Minimal UI: send prompt ➜ get reply    |       ✅       |
| **Stage 2**   | Write Ui, Add templates                 |       ✅       |
| **Stage 3**   | Integrate ui and core                   |       ✅       |
| **Stage 4**   | Decide log storage (SQLite vs. JSON)    |⏳ In progress  |
| **Stage 5**   | Model pcersona, command stability tests |       🔜       |
| **Stage 6**   | History viewer (per day)                |       🔜       |
| **Stage 7**   | Extras: token meter, UI themes          |       🔜       |

<br/>

## 🚀 Quick Start
```bash
git clone https://github.com/yourname/elfie.git
cd elfie
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   
python -m elfie        # launches the UI
```

<br/>

## 🌷🌷🌷 Project Structure🌷🌷🌷
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

<br/>

## 🤥 Planned Optimization
- DB version control
- handle new thread after creation (automatically)
- CLI 交互建議抽成 Utility
- HTML styling 建議抽出管理
- THREAD_NUM_ID_MAP and THREAD_NAME_ID_MAP crentralize 
- replace QPlainTextEdit with TExtEdit

<br/>

## 🦾Upcoming features (maybe)

- more cli in gui (ehhhh badass coder💀💀):
```
	→輸入：\\elf config
	→something pops out

	輸入：\\debug mode
	→ memory / thread / token 使用率

	> 輸入：\\kill
	→ 「！？嗚嗚我錯了啦別這樣 QAQ」
```
- LLM  ( like there's tim e💀 )
<br/><br/>

## ⚙️ Tech Stack & Constraints
- **Runtime**  Python 3.11 (64‑bit)  
- **UI**  PyQt5 5.15 (pre‑installed on target PCs)  
- **AI**  OpenAI Chat Completions API (key via `.env`)  
- **Platform**  Windows 10+ | offline‑first (only API calls go online)  
- **License**  MIT

<br/><br/><br/>