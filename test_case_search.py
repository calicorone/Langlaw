from src.case_search_api import fetch_case_laws

keywords = ["형법", "사기", "배임"]

for keyword in keywords:
    print(f"\n🔎 '{keyword}'에 대한 판례 검색:")
    try:
        cases = fetch_case_laws(keyword)
        if not cases:
            print("❗ 결과 없음")
        for case in cases:
            print(f"📌 {case['사건명']} ({case['사건번호']}) - {case['법원명']} / {case['선고일자']}")
            print(f"👉 상세보기: {case['판례상세링크']}\n")
    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")
