# Langlaw

한국어 사건 설명을 입력하면 핵심 법적 키워드를 추출하고, 관련 판례와 형법 조문을 검색한 뒤 GPT가 법적 판단 요약을 생성하는 AI 법률 분석 도구입니다.

---

## 주요 기능

| 기능 | 설명 |
|---|---|
| 키워드 추출 | LLM이 사건 설명에서 핵심 법적 키워드 3–5개 추출 |
| 판례 검색 | law.go.kr Open API로 키워드별 판례 조회 |
| 법령 매칭 | 로컬 형법 JSON에서 조문 검색 |
| 판단 요약 | GPT가 판례·법령을 종합해 법적 판단 요약 생성 |
| Web UI | Flask 기반 브라우저 인터페이스 (탭형 결과 뷰) |
| Desktop UI | Tkinter 기반 네이티브 데스크탑 앱 |
| API 키 설정 | 웹 UI 내 설정 모달 — `.env`에 키 저장 및 즉시 반영 |

---

## 아키텍처

전체 흐름은 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)에서 확인할 수 있습니다.

```
사용자 입력
    │
    ├── Web UI (Flask)          app.py  ──────────────────────────┐
    └── Desktop UI (Tkinter)   langlaw.py                        │
                                                                  ▼
                                              src/legal_reasoner.py  (analyze_case)
                                                    │
                          ┌─────────────────────────┼──────────────────────┐
                          ▼                         ▼                      ▼
              keyword_extractor.py        case_search_api.py         data/형법.json
              (OpenAI → 키워드 목록)      (law.go.kr → 판례 목록)    (조문 키워드 매칭)
                                                                           │
                                          ──────────────────────────────────
                                                    ▼
                                           OpenAI (판단 요약 생성)
                                                    │
                                              분석 결과 반환
```

---

## 프로젝트 구조

```
Langlaw/
├── app.py                     Flask 서버 · REST API · 설정 엔드포인트
├── langlaw.py                 데스크탑(Tkinter) 실행 진입점
├── langlaw.bat                Windows용 실행 스크립트
│
├── src/
│   ├── legal_reasoner.py      핵심 분석 파이프라인 (analyze_case)
│   ├── keyword_extractor.py   LangChain + OpenAI 키워드 추출
│   ├── case_search_api.py     law.go.kr 판례 Open API 클라이언트
│   ├── law_api_downloader.py  형법 XML 다운로드 · JSON 변환 (초기 1회)
│   └── langlaw_gui.py         Tkinter GUI (입력창 + 결과창)
│
├── templates/
│   └── index.html             웹 프론트엔드 (SPA)
│
├── static/
│   ├── favicon.svg            벡터 파비콘 (저울 아이콘)
│   ├── favicon.png            래스터 파비콘
│   └── favicon.ico            멀티해상도 .ico (16/32/48 px)
│
├── data/
│   ├── 형법.xml               형법 원본 XML (law.go.kr 다운로드)
│   └── 형법.json              파싱된 조문 JSON (런타임 사용)
│
├── docs/
│   └── ARCHITECTURE.md        상세 아키텍처 · 데이터 흐름 문서
│
└── test_*.py                  단위 테스트 스크립트
```

---

## 시작하기

### 사전 요구사항

- Python 3.10 이상
- OpenAI API 키 ([platform.openai.com/api-keys](https://platform.openai.com/api-keys))
- law.go.kr OC ID ([law.go.kr/DRF/UserMain.do](https://www.law.go.kr/DRF/UserMain.do) — 무료)

### 설치

```bash
git clone https://github.com/calicorone/Langlaw.git
cd Langlaw
pip install langchain-openai langchain-core python-dotenv requests flask
```

### 환경 변수 설정

`.env` 파일을 프로젝트 루트에 생성하거나, 앱 실행 후 웹 UI의 "⚙ API 키 설정" 버튼으로 설정할 수 있습니다.

```env
OPENAI_API_KEY=sk-...
OC_ID=your_law_go_kr_oc_id
```

### 형법 데이터 초기 다운로드 (최초 1회)

```bash
python -c "
from src.law_api_downloader import download_law_by_id, convert_xml_to_json
download_law_by_id('91')
convert_xml_to_json()
"
```

`data/형법.json`이 생성되면 이후에는 이 파일을 재사용합니다.

---

## 실행

### 웹 UI

```bash
python app.py
```

브라우저에서 [http://localhost:5000](http://localhost:5000)을 엽니다.

### 데스크탑 UI

```bash
python langlaw.py        # macOS / Linux
langlaw.bat              # Windows
```

---

## REST API

### `GET /api/settings`

현재 키 설정 여부를 반환합니다 (값 자체는 노출하지 않음).

```json
{ "OPENAI_API_KEY": true, "OC_ID": false }
```

### `POST /api/settings`

키를 `.env`에 저장하고 서버에 즉시 반영합니다.

```json
{ "OPENAI_API_KEY": "sk-...", "OC_ID": "your_id" }
```

### `POST /api/analyze`

사건을 분석하고 결과를 반환합니다.

**요청**

```json
{ "case_description": "운전 중 신호를 위반하여 보행자를 치어 사망하게 된 사건입니다." }
```

**응답**

```json
{
  "keywords": ["교통사고", "업무상과실치사", "신호위반"],
  "cases": [
    {
      "사건명": "대법원 2012도...",
      "사건번호": "2012도1234",
      "선고일자": "20130101",
      "법원명": "대법원",
      "판례상세링크": "https://www.law.go.kr/..."
    }
  ],
  "laws": [
    {
      "조문번호": "제268조",
      "제목": "업무상과실·중과실 치사상",
      "내용": "..."
    }
  ],
  "judgment": "이 사건은 형법 제268조 업무상 과실치사에 해당할 가능성이 높으며..."
}
```

---

## 테스트

```bash
python test_keyword_extraction.py   # 키워드 추출 확인
python test_case_search.py          # 판례 API 응답 확인
python test_reasoning.py            # 전체 파이프라인 확인
```

---

## 환경 변수

| 변수 | 필수 | 설명 |
|---|---|---|
| `OPENAI_API_KEY` | ✅ | OpenAI API 키 |
| `OC_ID` | ✅ | law.go.kr Open API OC 식별자 |

---

## 라이선스

MIT
