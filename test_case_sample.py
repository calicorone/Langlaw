from src.case_search_sample import fetch_case_laws_from_sample

print("🔍 샘플 판례 결과:")
cases = fetch_case_laws_from_sample()

for case in cases:
    print(f"📌 {case['사건명']} ({case['사건번호']}) - {case['법원명']} / {case['선고일자']}")
    print(f"👉 상세보기: {case['판례상세링크']}\n")
