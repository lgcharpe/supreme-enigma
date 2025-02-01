# config.py
import os

class Settings:
    SEASON_LIST_URL = "https://data.stortinget.no/eksport/publikasjoner?publikasjontype=referat&sesjonid=2024-2025"
    PUBLICATION_URL = "https://data.stortinget.no/eksport/publikasjon?publikasjonid="
    CACHE_FOLDER = "../cache"
    REQUEST_TIMEOUT = 30
    USER_AGENT = "PublicationFetcher/1.0"

settings = Settings()
