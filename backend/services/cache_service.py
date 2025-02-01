import json
import os
from config import settings
from typing import Optional

class CacheService:
    @staticmethod
    def cache_object(response_object: dict) -> None:
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        with open(f"{settings.CACHE_FOLDER}/{response_object['ids']}.json", "w") as f:
            json.dump(response_object, f)

    @staticmethod
    def read_from_cache(id: str) -> Optional[dict]:
        cache_path = f"{settings.CACHE_FOLDER}/{id}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None
