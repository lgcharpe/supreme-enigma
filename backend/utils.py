from typing import Optional
import pycountry


def get_language_name(iso_code: str) -> Optional[str]:
    """
    Convert ISO language code to full language name.
    Handles both 2-letter (639-1) and 3-letter (639-2/T) codes.

    Args:
        iso_code (str): ISO language code (e.g., 'nb', 'nob', 'en', 'eng')

    Returns:
        str: Full language name or None if not found

    Examples:
        >>> get_language_name('nb')
        'Norwegian Bokmål'
        >>> get_language_name('eng')
        'English'
    """
    try:
        # Try to find language by ISO code
        language = pycountry.languages.get(alpha_2=iso_code)
        if language is None:
            # If 2-letter code fails, try 3-letter code
            language = pycountry.languages.get(alpha_3=iso_code)

        if language is None:
            return None

        return language.name
    except (AttributeError, KeyError):
        return None
