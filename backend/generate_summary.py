import requests


def generate_response(text_to_summarize: str) -> str:
    prompt: str = f"Kan du oppsummere: \n{text_to_summarize}"

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "ola",
        "prompt": prompt,
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    raw = requests.post(url, json=payload, headers=headers).json()

    return raw["response"]


if __name__ == "__main__":
    print(generate_response("This is a text about everything possible!"))
