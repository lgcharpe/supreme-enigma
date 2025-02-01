class Settings:
    SEASON_LIST_URL = "https://data.stortinget.no/eksport/publikasjoner?publikasjontype=referat&sesjonid=2024-2025"
    PUBLICATION_URL = "https://data.stortinget.no/eksport/publikasjon?publikasjonid="
    TOPICS_URL = "https://data.stortinget.no/eksport/emner"
    CACHE_FOLDER = "../cache"
    REQUEST_TIMEOUT = 30
    USER_AGENT = "PublicationFetcher/1.0"

settings = Settings()
