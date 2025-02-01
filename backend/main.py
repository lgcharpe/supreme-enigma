from fastapi import FastAPI
import logging
from models import RequestBody, DayBody
from services.api_service import APIService
from services.cache_service import CacheService
from services.olama_service import OlamaService
from typing import List
import json

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/")
async def get(body: RequestBody):
    season_ids, dates = APIService.get_season_ids(body)
    if not season_ids:
        return {"responses": [], "meta_summary": None}

    final_response = APIService.get_responses_from_ids(season_ids, dates)

    if body.meta_summary:
        try:
            raw_responses = [response["raw_response"] for response in final_response["responses"]]
            meta_summary = OlamaService.generate_meta_response("\n".join(raw_responses)).strip("```json").strip("```")
            final_response["meta_summary"] = json.loads(meta_summary)
        except Exception as e:
            logger.error(f"Error generating meta summary: {str(e)}")
            final_response["meta_summary"] = None

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
=======
@app.post("/day")
async def day(body: DayBody):
    # Implementation for the day endpoint
    pass
>>>>>>> 53ea9a84572ed821a2acc516dc882b7d31d8d2dd
