import logging
import requests

class OlamaService:
    @staticmethod
    def generate_response(text_to_summarize: str, language: str) -> str:
        prompt = f'''
        You are an expert parliamentary analyst. Given a transcription of parliamentary proceedings, create a summary in {language}. Format the response as JSON with these exact fields:

        ```json
        {{
          "summary": "",          // 100-word overview of the proceedings
          "keyPoliticians": [{{
            "name": "",           // Politician's full name
            "party": "",          // Political party
            "mainArguments": []   // List of their main points/arguments
          }}],
          "disputes": [{{
            "topic": "",          // Subject of disagreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of the dispute
          }}],
          "agreements": [{{
            "topic": "",          // Subject of agreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of what was agreed
          }}],
          "votingResults": [{{
            "motion": "",         // What was voted on
            "result": "",         // Outcome of the vote
            "forCount": 0,        // Number of votes in favor
            "againstCount": 0     // Number of votes against
          }}],
          "funnyMoments": [{{
            "description": "",    // Description of the humorous event
            "politicians": []     // Politicians involved
          }}],
          "specialEvents": [{{
            "type": "",          // Type of special event
            "description": "",   // What happened
            "impact": ""         // Why it matters
          }}]
        }}
        ```

        Focus on the most significant events and discussions. Make the summary engaging but factual. Include any memorable exchanges or notable moments.
        You should ONLY reply with the JSON object.

        Here is the transcription:
            {text_to_summarize}
        '''

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
        {{
          "summary": "",          // 250-word overview of the entire period
          "keyPoliticians": [{{
            "name": "",           // Politician's full name
            "party": "",          // Political party
            "mainArguments": []   // List of their main points/arguments across the period
          }}],
          "disputes": [{{
            "topic": "",          // Major subject of disagreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of the ongoing dispute
          }}],
          "agreements": [{{
            "topic": "",          // Major subject of agreement
            "parties": [],        // Parties involved
            "summary": ""         // Brief description of significant agreements reached
          }}],
          "votingResults": [{{
            "motion": "",         // Major items voted on
            "result": "",         // Outcome of the vote
            "forCount": 0,        // Number of votes in favor
            "againstCount": 0     // Number of votes against
          }}],
          "funnyMoments": [{{
            "description": "",    // Most memorable humorous events
            "politicians": []     // Politicians involved
          }}],
          "specialEvents": [{{
            "type": "",           // Type of special event
            "description": "",    // What happened
            "impact": ""          // Why it matters
          }}]
        }}
        ```

        Combine similar events where appropriate and focus on the most impactful developments across the period.
        You should ONLY reply with the JSON object.


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


    @staticmethod
    def generate_meta_response_with_topic(text_to_summarize: str, language: str, topic: str) -> str:
        prompt: str = f"""
        You are an expert parliamentary analyst. Given multiple daily summaries, create a focused analysis of {topic} in {language}. Extract and analyze all relevant information about this topic from the provided transcripts. Format the response as JSON with these exact fields:

        ```json
        {{
        "summary": "",          // Overview of topic developments
        "keyDecisions": [{{
            "date": "",           // Date of decision
            "description": "",    // What was decided
            "impact": ""          // How it affects citizens
        }}],
        "currentStatus": {{
            "state": "",           // Current state of the topic
            "lastUpdated": ""      // When this was last reviewed
        }},
        "nextSteps": [{{
            "description": "",     // What's coming next
            "expectedDate": ""     // When it's expected
        }}],
        "publicFeedback": {{
            "summary": "",         // Overview of public response
            "mainConcerns": []     // List of main public concerns
        }}
        }}
        ```

        Focus on tracking the evolution of this specific topic through the transcripts, highlighting key developments, decisions, and their implications for the public. Synthesize information to provide a clear picture of where this issue stands and where it's headed.
        You should ONLY reply with the JSON object.


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

    @staticmethod
    def generate_response_with_topic(text_to_summarize: str, language: str, topic: str) -> str:
        prompt: str = f"""
        Here's the rewritten prompt:

        You are an expert parliamentary analyst. Given a transcription of parliamentary proceedings, create a focused analysis of {topic} in {language}. Extract and analyze all relevant information about this topic from the provided transcript. Format the response as JSON with these exact fields:

        ```json
        {{
          "summary": "",          // Overview of topic developments
          "keyDecisions": [{{
            "date": "",           // Date of decision
            "description": "",    // What was decided
            "impact": ""          // How it affects citizens
          }}],
          "currentStatus": {{
            "state": "",           // Current state of the topic
            "lastUpdated": ""      // When this was last reviewed
          }},
          "nextSteps": [{{
            "description": "",     // What's coming next
            "expectedDate": ""     // When it's expected
          }}],
          "publicFeedback": {{
            "summary": "",         // Overview of public response
            "mainConcerns": []     // List of main public concerns
          }}
        }}
        ```

        Focus on tracking this specific topic through the proceedings, highlighting key developments, decisions, and their implications for the public. Synthesize information to provide a clear picture of where this issue stands and where it's headed.
        You should ONLY reply with the JSON object.

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
