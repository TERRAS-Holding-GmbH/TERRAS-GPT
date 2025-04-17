import os
import requests
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SHAREPOINT_SITE_NAME = os.getenv("SHAREPOINT_SITE_NAME")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_API = "https://graph.microsoft.com/v1.0"

def authenticate():
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )
    result = app.acquire_token_silent(SCOPE, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPE)
    if "access_token" not in result:
        raise Exception("Authentication failed:", result.get("error_description"))
    return result["access_token"]

def get_site_id(access_token, site_name):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GRAPH_API}/sites?search={site_name}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    sites = res.json().get("value", [])
    if not sites:
        raise Exception("No SharePoint site found with that name.")
    return sites[0]["id"]

def list_files(access_token, site_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    # Get the default document library (drive)
    drive_url = f"{GRAPH_API}/sites/{site_id}/drive/root/children"
    res = requests.get(drive_url, headers=headers)
    res.raise_for_status()
    items = res.json().get("value", [])
    for item in items:
        print(f"📄 {item['name']} | {item['webUrl']}")

if __name__ == "__main__":
    token = authenticate()
    site_id = get_site_id(token, SHAREPOINT_SITE_NAME)
    list_files(token, site_id)
