import yelpapi

DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = '2781 24th St, San Francisco, CA'
SEARCH_LIMIT = 3

CONSUMER_KEY = "Qc2J7qFeS_pdWlqG_mCSag"
CONSUMER_SECRET = "JT7dL9ULPBn2aKabj5pATHrPMAs"
TOKEN = "OX_ZJxP12zlw3NBwfAkK5QSpwFOBe8O4"
TOKEN_SECRET = "GGOpNP6XvQGxfkgmsOYxysuc89k"

API = yelpapi.YelpAPI(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET)

def search(term, limit=SEARCH_LIMIT):
    return API.search_query(term=term, location=DEFAULT_LOCATION, limit=limit)['businesses']

def business(business_id):
    return API.business_query(id=business_id)
