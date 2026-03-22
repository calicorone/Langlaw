from pathlib import Path
import json
import re

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.keyword_extractor import extract_keywords_from_case
from src.case_search_api import fetch_case_laws

_REPO_ROOT = Path(__file__).resolve().parent.parent
_LAW_JSON = _REPO_ROOT / "data" / "형법.json"

llm = ChatOpenAI(temperature=0)


def load_laws():
    with open(_LAW_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_keywords(raw):
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    s = str(raw).strip()
    if not s:
        return []
    s = s.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    m = re.search(r"\[[\s\S]*?\]", s)
    if m:
        try:
            arr = json.loads(m.group())
            if isinstance(arr, list):
                return [str(x).strip() for x in arr if str(x).strip()]
        except json.JSONDecodeError:
            pass
    return [s]


def find_laws_by_keywords(keywords, law_data, max_results=5):
    result = []
    for keyword in keywords:
        for article in law_data:
            if keyword in article["내용"] or keyword in article["제목"]:
                result.append(article)
                if len(result) >= max_results:
                    return result
    return result


def analyze_case(case_description: str):
    text = (case_description or "").strip()
    if not text:
        raise ValueError("사건 설명을 입력해 주세요.")

    keywords_raw = extract_keywords_from_case(text)
    keywords = normalize_keywords(keywords_raw)

    all_cases = []
    for kw in keywords:
        all_cases += fetch_case_laws(kw, max_results=1)

    law_data = load_laws()
    matched_laws = find_laws_by_keywords(keywords, law_data, max_results=5)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "너는 법률 상담 전문가야. 사용자 사건 설명, 판례, 관련 법령을 바탕으로 판단을 내려줘."),
        ("human", """
사건 설명:
{case}

관련 판례 요약:
{cases}

적용 가능한 법령:
{laws}

위 내용을 바탕으로 이 사건에 적용될 수 있는 법적 판단 또는 변론 요지를 요약해줘.
        """)
    ])

    case_text = "\n".join([f"- {c['사건명']} ({c['사건번호']}, {c['선고일자']})" for c in all_cases])
    law_text = "\n".join([f"{l['조문번호']} {l['제목']} - {l['내용'][:80]}..." for l in matched_laws])

    chain = prompt | llm
    result = chain.invoke({
        "case": text,
        "cases": case_text,
        "laws": law_text
    })

    return {
        "case_description": text,
        "keywords_raw": keywords_raw,
        "keywords": keywords,
        "cases": all_cases,
        "laws": matched_laws,
        "judgment": result.content,
    }


def summarize_case(case_description: str):
    r = analyze_case(case_description)
    print("▶ 사건 설명:", r["case_description"])
    print("🔍 추출된 키워드:", r["keywords_raw"])
    print("\n🧠 LLM 판단 요약:\n")
    print(r["judgment"])


__all__ = ["summarize_case", "analyze_case", "load_laws", "find_laws_by_keywords"]
