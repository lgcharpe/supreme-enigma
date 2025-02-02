import logging
import requests

class OlamaService:
    @staticmethod
    def generate_response(text_to_summarize: str, language: str) -> str:
        prompt = f"""
        You are an expert parliamentary analyst. Given a transcription of parliamentary proceedings, create a summary in {language}. Format the response as JSON with these exact fields:

        ```json
        {
          "summary": "",          // 100-word overview of the proceedings
          "keyPoliticians": [{
            "name": "",           // Politician's full name
            "party": "",          // Political party
            "mainArguments": []   // List of their main points/arguments
          }],
          "disputes": [{
            "topic": "",          // Subject of disagreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of the dispute
          }],
          "agreements": [{
            "topic": "",          // Subject of agreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of what was agreed
          }],
          "votingResults": [{
            "motion": "",         // What was voted on
            "result": "",         // Outcome of the vote
            "forCount": 0,        // Number of votes in favor
            "againstCount": 0     // Number of votes against
          }],
          "funnyMoments": [{
            "description": "",    // Description of the humorous event
            "politicians": []     // Politicians involved
          }],
          "specialEvents": [{
            "type": "",          // Type of special event
            "description": "",   // What happened
            "impact": ""         // Why it matters
          }]
        }
        ```

        Focus on the most significant events and discussions. Make the summary engaging but factual. Include any memorable exchanges or notable moments.

        Here is the transcription:
            {text_to_summarize}
        """

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
    def generate_meta_response(text_to_summarize: str, language: str) -> str:
        prompt: str = f"""
        You are an expert parliamentary analyst. Given multiple daily summaries, create a comprehensive period overview in {language}. Synthesize the information and highlight the most important developments. Format the response as JSON with these exact fields:

        ```json
        {
          "summary": "",          // 250-word overview of the entire period
          "keyPoliticians": [{
            "name": "",           // Politician's full name
            "party": "",          // Political party
            "mainArguments": []   // List of their main points/arguments across the period
          }],
          "disputes": [{
            "topic": "",          // Major subject of disagreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of the ongoing dispute
          }],
          "agreements": [{
            "topic": "",          // Major subject of agreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of significant agreements reached
          }],
          "votingResults": [{
            "motion": "",         // Major items voted on
            "result": "",         // Outcome of the vote
            "forCount": 0,        // Number of votes in favor
            "againstCount": 0     // Number of votes against
          }],
          "funnyMoments": [{
            "description": "",    // Most memorable humorous events
            "politicians": []     // Politicians involved
          }],
          "specialEvents": [{
            "type": "",           // Type of special event
            "description": "",    // What happened
            "impact": ""          // Why it matters
          }]
        }
        ```

        Combine similar events where appropriate and focus on the most impactful developments across the period.

        Here are the daily summaries:
            {text_to_summarize}

        """

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "ola",
            "prompt": prompt,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}

        raw = requests.post(url, json=payload, headers=headers).json()

        return raw["response"]
