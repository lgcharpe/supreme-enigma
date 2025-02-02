import requests
import logging
import json
from typing import Optional, Tuple, List
from datetime import date
from config import settings
from models import DayBody, PeriodBody
from services.xml_service import XMLService
from services.cache_service import CacheService
from services.olama_service import OlamaService

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MAX_TOKEN_LIMIT = 15000

class APIService:
    @staticmethod
    def get_topics() -> Optional[List[str]]:
        try:
            response = requests.get(
                settings.TOPICS_URL,
                timeout=settings.REQUEST_TIMEOUT,
                verify=True,
                headers={'User-Agent': settings.USER_AGENT}
            )
            response.raise_for_status()
            return XMLService.parse_topics(response.text)

        except Exception as e:
            logger.error(f"Error fetching topics: {str(e)}")
            return None


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
    def get_season_ids(date_range: PeriodBody) -> Optional[Tuple[List[str], List[date]]]:
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

    @staticmethod
    def get_ids_from_date(specific_date: DayBody) -> Optional[List[str]]:
        try:
            response = requests.get(
                settings.SEASON_LIST_URL,
                timeout=settings.REQUEST_TIMEOUT,
                verify=True,
                headers={'User-Agent': settings.USER_AGENT}
            )
            response.raise_for_status()
            return XMLService.parse_season_list(response.text, specific_date)

        except Exception as e:
            logger.error(f"Error fetching season IDs: {str(e)}")
            return None

    @staticmethod
    def get_responses_from_ids(season_ids: List, dates: List, language: str) -> dict:
        final_response = {
            "responses": [],
        }
        for season_id, p_date in zip(season_ids, dates):
            # Log the season ID and date
            logger.info(f"Processing season ID {season_id} from date {p_date}")
            cached_response = CacheService.read_from_cache(season_id)
            if cached_response:
                final_response["responses"].append(cached_response)
                continue

            # Get and process publication
            publication = APIService.get_publication(season_id)
            if not publication:
                continue

            length = len(publication.split())
            if length > MAX_TOKEN_LIMIT:
                continue

            try:
                summary = OlamaService.generate_response(publication, language).strip("```json").strip("```")
                try:
                    parsed_summary = json.loads(summary)
                except json.JSONDecodeError:
                    logger.error(f"Error parsing JSON: {summary}")
                    continue

                response_object = {
                    "response": parsed_summary,
                    "raw_response": summary,
                    "lengths": length,
                    "ids": season_id,
                    "dates": str(p_date)
                }
                final_response["responses"].append(response_object)
                CacheService.cache_object(response_object)
            except Exception as e:
                logger.error(f"Error processing publication {season_id}: {str(e)}")
                continue
        return final_response
