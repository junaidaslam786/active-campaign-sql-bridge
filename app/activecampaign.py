# app/activecampaign.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("ACTIVE_CAMPAIGN_API_URL")
API_KEY = os.getenv("ACTIVE_CAMPAIGN_API_KEY")

def get_all_contacts(limit=100, offset=0):
    """
    Fetch contacts from ActiveCampaign.
    Pagination: limit (max 100), offset for batches.
    """
    url = f"{API_URL}/api/3/contacts"
    headers = {"Api-Token": API_KEY}
    params = {"limit": limit, "offset": offset}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("contacts", [])
