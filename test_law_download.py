from src.law_api_downloader import get_law_id_by_name, download_law_by_id, convert_xml_to_json

law_name = "형법"
law_id = get_law_id_by_name(law_name)
print(f"📌 '{law_name}'의 법령ID: {law_id}")

download_law_by_id(law_id, save_path=f"data/{law_name}.xml")
convert_xml_to_json(xml_path=f"data/{law_name}.xml", json_path=f"data/{law_name}.json")
