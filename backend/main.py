from fastapi import FastAPI
import xmltodict
import json
import requests
from typing import List, Optional
import logging
from requests.exceptions import RequestException
from xml.parsers.expat import ExpatError
import re
import os
import xml.etree.ElementTree as ET

from pydantic import BaseModel
from datetime import date, datetime
from generate_summary import generate_response, generate_meta_response

SEASON_LIST_URL = "https://data.stortinget.no/eksport/publikasjoner?publikasjontype=referat&sesjonid=2024-2025"
PUBLICATION_URL = "https://data.stortinget.no/eksport/publikasjon?publikasjonid="
CACHE_FOLDER = "../cache"
app = FastAPI()

class RequestBody(BaseModel):
    from_date: date
    to_date: date
    meta_summary: bool

@app.post("/")
async def get(body: RequestBody):
    # Get season_ids in a list
    season_ids, dates = get_season_ids(body)
    assert len(season_ids) == len(dates), "Wopsi Dopsi, uneven length"
    project_texts = []
    parsed_ids = []
    parsed_dates = []
    if season_ids:
        for season_id, p_date in zip(season_ids, dates):
            # Get publication data for each season_id
            publication = get_publication(season_id)
            project_texts.append(publication)
            parsed_ids.append(season_id)
            parsed_dates.append(p_date)
    else:
        logging.warning("No season_ids found")

    # Generate summary for each publication
    skipped = 0
    final_response = {
        "responses": [],
        "meta_summary": None
    }
    for project_text, pid, p_date in zip(project_texts, parsed_ids, parsed_dates):
        # Tries to read from cache, if it is None it generates a new response
        response_object = read_from_cache(pid)
        if response_object:
            logging.info(f"Found cached object for {pid}")
            final_response["responses"].append(response_object)
            continue

        length = len(project_text.split(" "))
        print(f"Length: {length}")
        if length > 5000:
            skipped += 1
            continue
        else:
            summary = generate_response(project_text)
            try:
                # Remove triple backticks from the start and end of the string
                summary = summary.strip("```")
                parsed_summary = json.loads(summary)
                response_object = {
                    "response": parsed_summary,
                    "raw_response": summary,
                    "lengths": length,
                    "ids": pid,
                    "dates": str(p_date)
                }
                final_response["responses"].append(response_object)
                try:
                    cache_object(response_object)
                except Exception as e:
                    logging.error(f"Failed to cache object: {str(e)}")
                    continue
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse JSON: {str(e)}")
                continue

    logging.warning(f"Skipped {skipped} summaries due to excessive length")

    if body.meta_summary:
        logging.info("Generating meta summary")
        raw_responses = [response["raw_response"] for response in final_response["responses"]]
        meta_summary = generate_meta_response("\n".join(raw_responses))
        try:
            meta_summary = meta_summary.strip("```")
            parsed_m_summary = json.loads(meta_summary)
            final_response["meta_summary"] = parsed_m_summary
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON: {str(e)}")
            final_response["meta_summary"] = None

    return final_response

# A funciton that saves the response object as a local json file in a folder. It also checks if the folder exists, if not it creates it.
def cache_object(response_object: dict):
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)
    with open(f"{CACHE_FOLDER}/{response_object['ids']}.json", "w") as f:
        json.dump(response_object, f)

# A function that reads the response object from the local json file based on pid and returns None if the file does not exist.
def read_from_cache(id: str):
    if os.path.exists(f"{CACHE_FOLDER}/{id}.json"):
        with open(f"{CACHE_FOLDER}/{id}.json", "r") as f:
            return json.load(f)
    else:
        return None


def get_publication(publication_id: str) -> Optional[dict]:
    """
    Safely fetches and extracts publication data from an XML endpoint.

    Args:
        publication_id (str): The ID of the publication to fetch

    Returns:
        Optional[dict]: Publication data if successful, None if an error occurs

    Raises:
        ValueError: If the publication ID is empty or malformed
    """
    # Set up logging
    logger = logging.getLogger(__name__)

    # Validate input
    if not publication_id or not isinstance(publication_id, str):
        logger.error("Invalid publication ID provided")
        raise ValueError("Publication ID must be a non-empty string")

    try:
        # Make request with timeout and verify SSL by default
        response = requests.get(
            f"{PUBLICATION_URL}{publication_id}",
            timeout=30,
            verify=True,
            headers={'User-Agent': 'PublicationFetcher/1.0'}
        )

        # Raise an error for bad status codes
        response.raise_for_status()

        parsed_text = extract_text_from_xml(response.text)

        # Use dict.get() for safe navigation through the data structure
        return parsed_text

    except RequestException as e:
        logger.error(f"Network error occurred: {str(e)}")
        return None
    except ExpatError as e:
        logger.error(f"XML parsing error: {str(e)}")
        return None
    except KeyError as e:
        logger.error(f"Unexpected data structure: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return None

def get_season_ids(date_range: RequestBody):
    """
    Safely fetches and extracts publication IDs from an XML endpoint.

    Args:
        url (str): The URL to fetch XML data from

    Returns:
        Optional[List[str]]: List of publication IDs if successful, None if an error occurs

    Raises:
        ValueError: If the URL is empty or malformed
    """
    # Set up logging
    logger = logging.getLogger(__name__)

    # Validate input
    if not SEASON_LIST_URL or not isinstance(SEASON_LIST_URL, str):
        logger.error("Invalid URL provided")
        raise ValueError("URL must be a non-empty string")

    try:
        # Make request with timeout and verify SSL by default
        response = requests.get(
            SEASON_LIST_URL,
            timeout=30,
            verify=True,
            headers={'User-Agent': 'SeasonIDFetcher/1.0'}
        )

        # Raise an error for bad status codes
        response.raise_for_status()

        # Parse XML safely
        data = xmltodict.parse(response.text)

        # Use dict.get() for safe navigation through the data structure
        publikasjoner = data.get('publikasjoner_oversikt')
        if not publikasjoner:
            logger.error("Missing publikasjoner_oversikt in XML response")
            return None

        publikasjoner_liste = publikasjoner.get('publikasjoner_liste')
        if not publikasjoner_liste:
            logger.error("Missing publikasjoner_liste in XML response")
            return None

        publications = publikasjoner_liste.get('publikasjon', [])
        if not publications:
            logger.warning("No publications found in response")
            return []

        # Handle both single publication (dict) and multiple publications (list)
        if isinstance(publications, dict):
            publications = [publications]

        # Safely extract IDs
        publication_ids = []
        dates = []
        for pub in publications:
            date_str = pub.get('dato')
            # check if date is within range provdied by the argumentof the function
            if date_str:
                #date = datetime.strptime(date_str, "%Y-%mm-%dT%H:%M:%S").date()
                # Parse dates that are like 2024-10-22T00:00:00
                date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S").date()
                if date >= date_range.from_date and date <= date_range.to_date:
                    pub_id = pub.get('id')
                    if pub_id:
                        publication_ids.append(pub_id)
                        dates.append(date)
                    else:
                        logger.warning(f"Publication found without ID: {pub}")
                else:
                    logger.warning(f"Publication found outside date range: {date}")
            else:
                logger.warning(f"Publication found without date: {pub}")

        return publication_ids, dates

    except RequestException as e:
        logger.error(f"Network error occurred: {str(e)}")
        return None
    except ExpatError as e:
        logger.error(f"XML parsing error: {str(e)}")
        return None
    except KeyError as e:
        logger.error(f"Unexpected data structure: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return None


def extract_text_from_xml(xml_string):
    root = ET.fromstring(xml_string)
    extracted_text = []
    current_name = ""
    timestamp_pattern = re.compile(r"\[\d{2}:\d{2}:\d{2}\]")

    for a_tag in root.findall(".//A"):  # Find all <A> tags
        name_tag = a_tag.find("Navn")
        if name_tag is not None:
            current_name = name_tag.text.strip() if name_tag.text else ""

        text_parts = [elem.tail.strip() if elem.tail else "" for elem in a_tag.iter() if elem.tail]
        text_content = " ".join(text_parts).strip()
        text_content = timestamp_pattern.sub("", text_content)  # Remove timestamps

        if current_name:
            extracted_text.append(f"{current_name}\n{text_content}")
            current_name = ""  # Reset name after use
        else:
            extracted_text.append(text_content)

    text = "\n".join(filter(None, extracted_text))
    # Remove all occurences of timestamps on the format: [12:05:54]
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    return text
