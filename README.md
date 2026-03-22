# Langlaw

AI-powered Korean legal analysis tool. Enter a case description and Langlaw extracts legal keywords, searches relevant precedents from the Korean Law Information Centre (law.go.kr), matches applicable statutes from the Criminal Act (형법), and produces a concise legal judgment summary via GPT.

---

## Features

- **Keyword extraction** — LLM identifies 3–5 core legal keywords from your case description
- **Precedent search** — queries law.go.kr's Open API for matching case law
- **Statute matching** — searches the downloaded Criminal Act JSON for relevant articles
- **Judgment summary** — GPT synthesises everything into a plain-language legal analysis
- **Web UI** — clean, responsive single-page interface (Flask)
- **Desktop UI** — native Tkinter window (optional)

---

## Project Structure

```
Langlaw/
├── app.py                  # Flask web server + REST API
├── langlaw.py              # Desktop (Tkinter) launcher
├── langlaw.bat             # Windows shortcut for desktop UI
│
├── src/
│   ├── legal_reasoner.py   # Core analysis pipeline (analyze_case / summarize_case)
│   ├── keyword_extractor.py# LLM-based keyword extraction
│   ├── case_search_api.py  # law.go.kr precedent search
│   ├── law_api_downloader.py # Downloads / converts statute XML → JSON
│   └── langlaw_gui.py      # Tkinter GUI
│
├── templates/
│   └── index.html          # Web frontend
│
├── static/
│   ├── favicon.svg         # Vector favicon (balance scale)
│   ├── favicon.png         # Raster favicon
│   └── favicon.ico         # Multi-resolution .ico (16/32/48 px)
│
├── data/
│   ├── 형법.xml             # Criminal Act (raw XML)
│   └── 형법.json            # Criminal Act (parsed JSON, used at runtime)
│
└── test_*.py               # Manual test scripts
```

---

## Prerequisites

- Python 3.10+
- OpenAI API key
- law.go.kr Open API key (OC ID)

---

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/calicorone/Langlaw.git
   cd Langlaw
   ```

2. Install dependencies:

   ```bash
   pip install langchain-openai langchain-core python-dotenv requests flask
   ```

3. Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=sk-...
   OC_ID=your_law_go_kr_oc_id
   ```

   You can obtain an OC ID for free at [www.law.go.kr/DRF/UserMain.do](https://www.law.go.kr/DRF/UserMain.do).

4. Download the Criminal Act data (only needed once):

   ```bash
   python -c "from src.law_api_downloader import *; download_law_by_id('91'); convert_xml_to_json()"
   ```

---

## Running the Web UI

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

### API endpoint

```
POST /api/analyze
Content-Type: application/json

{ "case_description": "운전 중 신호를 위반하여 보행자를 치어 사망하게 된 사건입니다." }
```

Response:

```json
{
  "keywords": ["교통사고", "업무상과실치사", "신호위반"],
  "cases":    [{ "사건명": "...", "사건번호": "...", "선고일자": "...", "법원명": "...", "판례상세링크": "..." }],
  "laws":     [{ "조문번호": "제268조", "제목": "업무상과실·중과실 치사상", "내용": "..." }],
  "judgment": "이 사건은 ..."
}
```

---

## Running the Desktop UI

```bash
python langlaw.py        # macOS / Linux
langlaw.bat              # Windows
```

---

## Running Tests

```bash
python test_keyword_extraction.py
python test_case_search.py
python test_reasoning.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key (required) |
| `OC_ID` | law.go.kr Open API OC identifier (required) |

---

## License

MIT
