from src.keyword_extractor import extract_keywords_from_case

case = "운전 중 신호를 위반하여 보행자를 치어 사망하게 한 사건입니다."
result = extract_keywords_from_case(case)

print("🔍 추출된 키워드:")
print(result)
