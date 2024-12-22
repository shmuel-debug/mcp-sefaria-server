import requests

SEFARIA_API_BASE_URL = "http://localhost:8000"

def get_request_json_data(endpoint, ref=None, param=None):
    """
    Helper function to make GET requests to the Sefaria API and parse the JSON response.
    """
    url = f"{SEFARIA_API_BASE_URL}/{endpoint}"

    if ref:
        url += f"{ref}"

    if param:
        url += f"?{param}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None

def get_commentary_text(ref):
    """
    Retrieves the title and text of a commentary.
    """
    data = get_request_json_data("api/v3/texts/", ref)

    if data and "versions" in data and len(data['versions']) > 0:
        title = data['title']
        text = data['versions'][0]['text']
        return title, text
    else:
        print(f"Could not retrieve commentary text for {ref}")
        return None, None

def get_parasha_data():
    """
    Retrieves the weekly Parasha data using the Calendars API.
    """
    data = get_request_json_data("api/calendars")

    if data:
        calendar_items = data.get('calendar_items', [])
        for item in calendar_items:
            if item.get('title', {}).get('en') == 'Parashat Hashavua':
                parasha_ref = item.get('ref')
                parasha_name = item.get('displayValue', {}).get('en')
                return parasha_ref, parasha_name
    
    print("Could not retrieve Parasha data.")
    return None, None

def get_first_verse(parasha_ref):
    """
    Extracts the first verse from the Parasha range.
    """
    if parasha_ref:
        return parasha_ref.split("-")[0]
    else:
        return None

def get_hebrew_text(parasha_ref):
    """
    Retrieves the Hebrew text and version title for the given verse.
    """
    data = get_request_json_data("api/v3/texts/", parasha_ref)

    if data and "versions" in data and len(data['versions']) > 0:
        he_pasuk = data['versions'][0]['text']
        return  he_pasuk
    else:
        print(f"Could not retrieve Hebrew text for {parasha_ref}")
        return None

def get_english_text(parasha_ref):
    """
    Retrieves the English text and version title for the given verse.
    """
    data = get_request_json_data("api/v3/texts/", parasha_ref, "version=english")

    if data and "versions" in data and len(data['versions']) > 0:
        en_vtitle = data['versions'][0]['versionTitle']
        en_pasuk = data['versions'][0]['text']
        return en_vtitle, en_pasuk
    else:
        print(f"Could not retrieve English text for {parasha_ref}")
        return None, None

async def get_commentaries(parasha_ref)-> list[str]:
    """
    Retrieves and filters commentaries on the given verse.
    """
    data = get_request_json_data("api/related/", parasha_ref)

    commentaries = []
    if data and "links" in data:
        for linked_text in data["links"]:
            if linked_text.get('type') == 'commentary':
                commentaries.append(linked_text.get('sourceHeRef'))

    return commentaries

async def get_text(reference: str) -> str:
    """
    Retrieves the text for a given reference.
    """
    return str(get_hebrew_text(reference))
