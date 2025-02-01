from fastapi import FastAPI
import logging
from models import RequestBody, DayBody
from services.api_service import APIService
from services.cache_service import CacheService
from generate_summary import generate_response, generate_meta_response
import json

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/")
async def get(body: RequestBody):
    season_ids, dates = APIService.get_season_ids(body)
    if not season_ids:
        return {"responses": [], "meta_summary": None}

    final_response = {
        "responses": [],
        "meta_summary": None
    }

    for season_id, p_date in zip(season_ids, dates):
        # Check cache first
        cached_response = CacheService.read_from_cache(season_id)
        if cached_response:
            final_response["responses"].append(cached_response)
            continue

        # Get and process publication
        publication = APIService.get_publication(season_id)
        if not publication:
            continue

        length = len(publication.split())
        if length > 5000:
            continue

        try:
            summary = generate_response(publication).strip("```")
            parsed_summary = json.loads(summary)
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

    if body.meta_summary:
        try:
            raw_responses = [response["raw_response"] for response in final_response["responses"]]
            meta_summary = generate_meta_response("\n".join(raw_responses)).strip("```json").strip("```")
            final_response["meta_summary"] = json.loads(meta_summary)
        except Exception as e:
            logger.error(f"Error generating meta summary: {str(e)}")
            final_response["meta_summary"] = None

    return final_response

@app.post("/day")
async def day(body: DayBody):
    # Implementation for the day endpoint
    pass
