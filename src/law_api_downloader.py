import requests
import xml.etree.ElementTree as ET
import os
import json
from dotenv import load_dotenv

load_dotenv()
OC_ID = os.getenv("OC_ID")

def get_law_id_by_name(law_name: str) -> str:
    """법령 이름으로 ID 조회"""
    url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": OC_ID,
        "target": "law",
        "type": "XML",
        "query": law_name
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    return root.findtext("law/법령ID")

def download_law_by_id(law_id: str, save_path="data/형법.xml"):
    """법령 ID로 전체 조문 다운로드 및 저장"""
    url = "https://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": OC_ID,
        "target": "law",
        "type": "XML",
        "ID": law_id
    }
    response = requests.get(url, params=params)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(response.content)
    print(f"✅ 저장 완료: {save_path}")

def convert_xml_to_json(xml_path="data/형법.xml", json_path="data/형법.json"):
    """XML을 파싱해서 조문 단위 JSON으로 저장"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    articles = []
    for part in root.findall(".//조문단위"):
        조문번호 = part.findtext("조문번호")
        조문제목 = part.findtext("조문제목") or ""
        조문내용 = part.findtext("조문내용") or ""
        if 조문번호:
            articles.append({
                "조문번호": 조문번호.strip(),
                "제목": 조문제목.strip(),
                "내용": 조문내용.strip().replace("\n", " ")
            })

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 저장 완료: {json_path}")
