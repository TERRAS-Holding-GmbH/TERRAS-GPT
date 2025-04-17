import msal
import os
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SHAREPOINT_SITE_NAME = os.getenv("SHAREPOINT_SITE_NAME")

authority = f"https://login.microsoftonline.com/{TENANT_ID}"
scope = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(CLIENT_ID, authority=authority, client_credential=CLIENT_SECRET)
result = app.acquire_token_for_client(scopes=scope)

if "access_token" in result:
    access_token = result["access_token"]
    print("Successfully acquired access token.")
else:
    print("Failed to acquire token.")

import requests

# Example query to get SharePoint sites
url = "https://graph.microsoft.com/v1.0/sites?search=TerrasHoldingAufbau"
headers = {"Authorization": f"Bearer {access_token}"}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    sites = response.json()
    print(sites)
else:
    print(f"Error: {response.status_code}")


# Example to list the user's OneDrive
url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    files = response.json()
    print(files)
else:
    print(f"Error: {response.status_code}")
