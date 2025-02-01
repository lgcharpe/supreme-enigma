from fastapi import FastAPI
import logging
from models import PeriodBody, DayBody
from services.api_service import APIService
from services.cache_service import CacheService
from services.olama_service import OlamaService
from typing import List
import json

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/period")
async def get(body: PeriodBody):
    # Check if the response is cached first
    cached_response = CacheService.read_period_object_from_cache(body)
    if cached_response:
        return cached_response
    else:
        season_ids, dates = APIService.get_season_ids(body)
        if not season_ids:
            return {"responses": [], "meta_summary": None}

        final_response = APIService.get_responses_from_ids(season_ids, dates)

        try:
            raw_responses = [response["raw_response"] for response in final_response["responses"]]
            meta_summary = OlamaService.generate_meta_response("\n".join(raw_responses)).strip("```json").strip("```")
            final_response["meta_summary"] = json.loads(meta_summary)
        except Exception as e:
            logger.error(f"Error generating meta summary: {str(e)}")
            final_response["meta_summary"] = None

        CacheService.cache_period_object(final_response, body)

        return final_response


@app.post("/day")
async def day(body: DayBody):
    # Implementation for the day endpoint
    season_ids, dates = APIService.get_ids_from_date(body)
    if not season_ids:
        return {"responses": [], "meta_summary": None}

    response_object = APIService.get_responses_from_ids(season_ids, dates)
    return response_object


@app.get("/topics")
async def topics():
    # Implementation for the topics endpoint
    topics = APIService.get_topics()
    return topics
