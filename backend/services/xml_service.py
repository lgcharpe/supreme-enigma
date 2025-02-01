import xml.etree.ElementTree as ET
import re
import xmltodict
import logging
from typing import Optional, Tuple, List
from datetime import datetime, date
from models import RequestBody

class XMLService:
    @staticmethod
    def extract_text_from_xml(xml_string: str) -> str:
        root = ET.fromstring(xml_string)
        extracted_text = []
        current_name = ""
        timestamp_pattern = re.compile(r"\[\d{2}:\d{2}:\d{2}\]")

        for a_tag in root.findall(".//A"):
            name_tag = a_tag.find("Navn")
            if name_tag is not None:
                current_name = name_tag.text.strip() if name_tag.text else ""

            text_parts = [elem.tail.strip() if elem.tail else "" for elem in a_tag.iter() if elem.tail]
            text_content = " ".join(text_parts).strip()
            text_content = timestamp_pattern.sub("", text_content)

            if current_name:
                extracted_text.append(f"{current_name}\n{text_content}")
                current_name = ""
            else:
                extracted_text.append(text_content)

        text = "\n".join(filter(None, extracted_text))
        return re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)

    @staticmethod
    def parse_season_list(xml_data: str, date_range: RequestBody) -> Tuple[List[str], List[date]]:
        data = xmltodict.parse(xml_data)
        publication_ids = []
        dates = []

        publikasjoner = data.get('publikasjoner_oversikt', {})
        publications = publikasjoner.get('publikasjoner_liste', {}).get('publikasjon', [])

        if isinstance(publications, dict):
            publications = [publications]

        for pub in publications:
            date_str = pub.get('dato')
            if date_str:
                pub_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
                if date_range.from_date <= pub_date <= date_range.to_date:
                    pub_id = pub.get('id')
                    if pub_id:
                        publication_ids.append(pub_id)
                        dates.append(pub_date)

        return publication_ids, dates
