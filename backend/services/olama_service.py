import logging
import requests

class OlamaService:
    @staticmethod
    def generate_response(text_to_summarize: str) -> str:
        prompt: str = f"Kan du oppsummere den følgende stortingsmeldingen: \n{text_to_summarize}"

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "ola",
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        raw = requests.post(url, json=payload, headers=headers).json()

        return raw["response"]

    @staticmethod
    def generate_meta_response(text_to_summarize: str) -> str:
        prompt: str = f"Aggregate the following summaries into a shared json object \n{text_to_summarize}"

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "knut",
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        raw = requests.post(url, json=payload, headers=headers).json()

        return raw["response"]
