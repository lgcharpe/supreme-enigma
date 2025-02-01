import requests
import logging
from typing import Optional, Tuple, List
from datetime import date
from xml.parsers.expat import ExpatError
from requests.exceptions import RequestException
from config import settings
from models import RequestBody
from services.xml_service import XMLService

logger = logging.getLogger(__name__)

class APIService:
    @staticmethod
    def get_publication(publication_id: str) -> Optional[str]:
        if not publication_id or not isinstance(publication_id, str):
            raise ValueError("Publication ID must be a non-empty string")

        try:
            response = requests.get(
                f"{settings.PUBLICATION_URL}{publication_id}",
                timeout=settings.REQUEST_TIMEOUT,
                verify=True,
                headers={'User-Agent': settings.USER_AGENT}
            )
            response.raise_for_status()
            return XMLService.extract_text_from_xml(response.text)

        except Exception as e:
            logger.error(f"Error fetching publication {publication_id}: {str(e)}")
            return None

    @staticmethod
    def get_season_ids(date_range: RequestBody) -> Optional[Tuple[List[str], List[date]]]:
        try:
            response = requests.get(
                settings.SEASON_LIST_URL,
                timeout=settings.REQUEST_TIMEOUT,
                verify=True,
                headers={'User-Agent': settings.USER_AGENT}
            )
            response.raise_for_status()
            return XMLService.parse_season_list(response.text, date_range)

        except Exception as e:
            logger.error(f"Error fetching season IDs: {str(e)}")
            return None
