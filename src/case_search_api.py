import requests
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

load_dotenv()
OC_ID = os.getenv("OC_ID")

def fetch_case_laws(keyword, max_results=5):
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": OC_ID,
        "target": "prec",
        "type": "XML",
        "query": keyword,
        "display": max_results
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("❌ API 요청 실패: 상태코드 " + str(response.status_code))

    root = ET.fromstring(response.content)
    results = []

    for record in root.findall("prec"):
        result = {
            # 📌 주의: '판례명' 대신 '사건명'으로 수정
            "사건명": record.findtext("사건명") or record.findtext("판례명") or "제목 없음",
            "사건번호": record.findtext("사건번호"),
            "선고일자": record.findtext("선고일자"),
            "법원명": record.findtext("법원명") or "미상",
            "판례상세링크": "https://www.law.go.kr" + record.findtext("판례상세링크", ""),
        }
        results.append(result)

    return results
