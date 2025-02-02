import json
import os
from config import settings
from typing import Optional
from models import PeriodBody


class CacheService:
    @staticmethod
    def cache_object(response_object: dict) -> None:
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        with open(f"{settings.CACHE_FOLDER}/{response_object['ids']}.json", "w") as f:
            json.dump(response_object, f)

    @staticmethod
    def cache_object_by_topic(response_object: dict, topic_id: int) -> None:
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        with open(f"{settings.CACHE_FOLDER}/{response_object['ids']}_{str(topic_id)}.json", "w") as f:
            json.dump(response_object, f)

    @staticmethod
    def cache_period_object(response_object: dict, date_object: PeriodBody) -> None:
        from_date = str(date_object.from_date)
        to_date = str(date_object.to_date)
        full_date = f"{from_date}_{to_date}"
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        with open(f"{settings.CACHE_FOLDER}/{full_date}.json", "w") as f:
            json.dump(response_object, f)

    @staticmethod
    def read_period_object_from_cache(date_object: PeriodBody) -> Optional[dict]:
        from_date = str(date_object.from_date)
        to_date = str(date_object.to_date)
        full_date = f"{from_date}_{to_date}"
        cache_path = f"{settings.CACHE_FOLDER}/{full_date}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    @staticmethod
    def cache_period_object_by_topic_by_topic(response_object: dict, date_object: PeriodBody, topic_id: int) -> None:
        from_date = str(date_object.from_date)
        to_date = str(date_object.to_date)
        full_date = f"{from_date}_{to_date}"
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        with open(f"{settings.CACHE_FOLDER}/{full_date}_{str(topic_id)}.json", "w") as f:
            json.dump(response_object, f)

    @staticmethod
    def read_period_object_from_cache_by_topic(date_object: PeriodBody, topic_id: int) -> Optional[dict]:
        from_date = str(date_object.from_date)
        to_date = str(date_object.to_date)
        full_date = f"{from_date}_{to_date}"
        cache_path = f"{settings.CACHE_FOLDER}/{full_date}_{str(topic_id)}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    @staticmethod
    def read_from_cache(id: str) -> Optional[dict]:
        cache_path = f"{settings.CACHE_FOLDER}/{id}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    @staticmethod
    def read_from_cache_by_topic(id: str, topic_id: int) -> Optional[dict]:
        cache_path = f"{settings.CACHE_FOLDER}/{id}_{str(topic_id)}.json"
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None
