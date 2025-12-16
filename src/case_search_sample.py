import xml.etree.ElementTree as ET

def fetch_case_laws_from_sample(xml_path="sample_prec.xml"):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = []

    for record in root.findall("RECORD"):
        result = {
            "사건명": record.findtext("사건명"),
            "사건번호": record.findtext("사건번호"),
            "선고일자": record.findtext("선고일자"),
            "법원명": record.findtext("법원명"),
            "판례상세링크": record.findtext("판례상세링크"),
        }
        results.append(result)
    return results
