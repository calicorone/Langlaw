from src.legal_reasoner import summarize_case

# ✅ 실제 사건 설명을 이곳에 입력하세요
example_description = "운전 중 실수로 신호를 위반하여 보행자를 치어 사망하게 된 사건입니다."

# 🔍 사건 설명을 기반으로 관련 판례, 법령 검색 후 LLM 분석
summarize_case(example_description)

