import xml.etree.ElementTree as ET
import re
import xmltodict
import logging
from typing import Optional, List, Dict, TypedDict, Tuple
from datetime import datetime, date
from models import RequestBody, DayBody
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class Topic(TypedDict):
    id: str
    name: str
    is_main_subject: bool
    sub_topics: List['Topic']


class XMLService:
    @staticmethod
    def parse_topics(xml_data: str) -> Optional[List[Topic]]:
            try:
                if not xml_data:
                    logger.error("Empty XML data received")
                    return None

                data = xmltodict.parse(xml_data)
                if not data:
                    logger.error("Failed to parse XML data")
                    return None

                # Safely navigate through the nested structure
                emne_oversikt = data.get('emne_oversikt') or {}
                emne_liste = emne_oversikt.get('emne_liste') or {}
                topics = emne_liste.get('emne')

                if not topics:
                    logger.warning("No topics found in XML")
                    return []

                # Ensure topics is always a list
                if isinstance(topics, dict):
                    topics = [topics]

                result = []

                for topic in topics:
                    if not isinstance(topic, dict):
                        continue

                    # Process main topic with safe gets
                    main_topic = {
                        'id': topic.get('id', ''),
                        'name': topic.get('navn', ''),
                        'is_main_subject': topic.get('er_hovedemne') == 'true',
                        'sub_topics': []
                    }

                    # Safely process sub-topics
                    underemne_liste = topic.get('underemne_liste') or {}
                    sub_topics = underemne_liste.get('emne')

                    if sub_topics:
                        # Ensure sub_topics is always a list
                        if isinstance(sub_topics, dict):
                            sub_topics = [sub_topics]

                        for sub_topic in sub_topics:
                            if not isinstance(sub_topic, dict):
                                continue

                            sub_topic_data = {
                                'id': sub_topic.get('id', ''),
                                'name': sub_topic.get('navn', ''),
                                'is_main_subject': sub_topic.get('er_hovedemne') == 'true',
                                'sub_topics': []
                            }
                            main_topic['sub_topics'].append(sub_topic_data)

                    result.append(main_topic)

                return result

            except Exception as e:
                logger.error(f"Error parsing topics: {str(e)}")
                return None

    @staticmethod
    def get_all_topic_names(topics: List[Topic]) -> List[str]:
        """Helper method to get a flat list of all topic names"""
        result = []
        for topic in topics:
            result.append(topic['name'])
            result.extend([sub['name'] for sub in topic['sub_topics']])
        return result

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
    def parse_season_list(xml_data: str, date_object: BaseModel) -> Tuple[List[str], List[date]]:
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
                # If date object is of instance DayBody, we want to extract the publication IDs for a specific date
                # If date object is of instance RequestBody, we want to extract the publication IDs for a date range
                if isinstance(date_object, DayBody):
                    if date_object.date == pub_date:
                        pub_id = pub.get('id')
                        if pub_id:
                            publication_ids.append(pub_id)
                            dates.append(pub_date)
                elif isinstance(date_object, RequestBody):
                    if date_object.from_date <= pub_date <= date_object.to_date:
                        pub_id = pub.get('id')
                        if pub_id:
                            publication_ids.append(pub_id)
                            dates.append(pub_date)
                else:
                    raise ValueError("Date object must be an instance of DayBody or Request")

        return publication_ids, dates
