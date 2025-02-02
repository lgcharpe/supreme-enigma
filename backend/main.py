from re import S
from fastapi import FastAPI, Path, Query
import logging
from models import PeriodBody, DayBody
from services.api_service import APIService
from services.xml_service import XMLService
from services.cache_service import CacheService
from services.olama_service import OlamaService
import json
from utils import get_language_name

app = FastAPI()
logger = logging.getLogger(__name__)
# Set the logger level to display info
logger.setLevel(logging.INFO)

@app.get("/summary/{country}/period/{startDate}/{endDate}")
async def get_summary_by_period(
    country: str = Path(..., min_length=2, max_length=2),
    startDate: str = Path(...),
    endDate: str = Path(...),
    lang: str = Query("nb", min_length=2, max_length=2)
):
    d_object = PeriodBody(from_date=startDate, to_date=endDate)
    language_name = get_language_name(lang)
    # Check if the response is cached first
    cached_response = CacheService.read_period_object_from_cache(d_object)
    if cached_response:
        return cached_response
    else:
        season_ids, dates = APIService.get_season_ids(d_object)
        if not season_ids:
            return {"responses": [], "meta_summary": None}

        final_response = APIService.get_responses_from_ids(season_ids, dates, language_name)

        try:
            raw_responses = [response["raw_response"] for response in final_response["responses"]]
            meta_summary = OlamaService.generate_meta_response("\n".join(raw_responses), language_name).strip("```json").strip("```")
            final_response["meta_summary"] = json.loads(meta_summary)
        except Exception as e:
            logger.error(f"Error generating meta summary: {str(e)}")
            final_response["meta_summary"] = None

        CacheService.cache_period_object(final_response, d_object)

        return final_response


@app.get("/summary/{country}/date/{date}")
async def get_summary_by_date(
    country: str = Path(..., min_length=2, max_length=2),
    date: str = Path(...),
    lang: str = Query("en", min_length=2, max_length=2)
):
    language_name = get_language_name(lang)
    d_obj = DayBody(country=country, date=date, lang=language_name)
    print(d_obj)

    season_ids, dates = APIService.get_ids_from_date(d_obj)
    print(season_ids, dates)
    if not season_ids:
        return {"responses": [], "meta_summary": None}

    response_object = APIService.get_responses_from_ids(season_ids, dates, d_obj.lang)
    return response_object

@app.get("/summary/{country}/period/{startDate}/{endDate}/{topic}")
async def get_summary_by_period_and_topic(
    country: str = Path(..., min_length=2, max_length=2),
    startDate: str = Path(...),
    endDate: str = Path(...),
    topic: int = Path(...),
    lang: str = Query("en", min_length=2, max_length=2)
):

    # Call the get topics method to get the topics and find the topic name from the topic id

    topics = APIService.get_topics()
    all_topics = XMLService.get_all_topic_names(topics)
    topic_name = all_topics.get(topic, None)

    d_object = PeriodBody(from_date=startDate, to_date=endDate)
    language_name = get_language_name(lang)
    # Check if the response is cached first
    cached_response = CacheService.read_period_object_from_cache(d_object)
    if cached_response:
        return cached_response
    else:
        season_ids, dates = APIService.get_season_ids(d_object)
        if not season_ids:
            return {"responses": [], "meta_summary": None}

        final_response = APIService.get_responses_from_ids(season_ids, dates, language_name)

        try:
            raw_responses = [response["raw_response"] for response in final_response["responses"]]
            meta_summary = OlamaService.generate_meta_response_with_topic("\n".join(raw_responses), language_name, topic_name).strip("```json").strip("```")
            final_response["meta_summary"] = json.loads(meta_summary)
        except Exception as e:
            logger.error(f"Error generating meta summary: {str(e)}")
            final_response["meta_summary"] = None

        CacheService.cache_period_object(final_response, d_object)

        return final_response



@app.get("/topics/{country}")
async def get_topics(
    country: str = Path(..., min_length=2, max_length=2),
    lang: str = Query("en", min_length=2, max_length=2)
):
    # Implementation for the topics endpoint
    topics = APIService.get_topics()
    return topics
