from src.keyword_extractor import extract_keywords_from_case
from src.case_search_api import fetch_case_laws
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(temperature=0)

def load_laws():
    with open("data/\uD615\uBC95.json", "r", encoding="utf-8") as f:
        return json.load(f)

def find_laws_by_keywords(keywords, law_data, max_results=5):
    result = []
    for keyword in keywords:
        for article in law_data:
            if keyword in article["내용"] or keyword in article["제목"]:
                result.append(article)
                if len(result) >= max_results:
                    return result
    return result

def summarize_case(case_description: str):
    print("▶ 사건 설명:", case_description)

    # 1. 키워드 추출
    keywords = extract_keywords_from_case(case_description)
    print("🔍 추출된 키워드:", keywords)

    # 2. 관련 판례 검색
    all_cases = []
    for kw in keywords:
        all_cases += fetch_case_laws(kw, max_results=1)

    # 3. 관련 법령 검색 (제한된 수로 필터링)
    law_data = load_laws()
    matched_laws = find_laws_by_keywords(keywords, law_data, max_results=5)

    # 4. LLM에 전달할 템플릿
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
        "case": case_description,
        "cases": case_text,
        "laws": law_text
    })

    print("\n🧠 LLM 판단 요약:\n")
    print(result.content)

__all__ = ["summarize_case"]
