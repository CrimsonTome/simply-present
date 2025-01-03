import json
import time
from pathlib import Path
from pypresence import Presence  # For setting up Discord RPC
import requests  # Will be needed later for SP requests


SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# Load secrets from file, this includes your Simply PLugin API key
secretsPath = Path("secrets.json")
with secretsPath.open(encoding="utf-8") as file:
    secrets = json.load(file)

# Assume everything here breaks if there are multiple fronters


def get_data():
    """This function gets the fronter data from Simply Plural."""
    payload = {}
    headers = {"Authorization": secrets["SimplyPluralAPIKey"]}

    response = requests.request(
        "GET",
        SIMPLY_PLURAL_BASE_URL + "/fronters/",
        headers=headers,
        data=payload,
        timeout=10,
    )
    response_content = response.text
    data = json.loads(response_content)
    # Get current fronters, this probably breaks if there are multiple fronters
    # Stripping out anything that isn't a member ID such as [] and ''
    fronters = "".join([item["content"]["member"] for item in data])
    # print(members)

    # Get uid (system ID)
    uid = "".join([item["content"]["uid"] for item in data])
    # print(uid)

    # Get the name of the fronter using the uid and member id
    # This 100% breaks if there are multiple fronters
    response = requests.request(
        "GET",
        SIMPLY_PLURAL_BASE_URL + "/member/" + uid + "/" + fronters,
        headers=headers,
        data=payload,
        timeout=10,
    )
    response_content = response.text
    data = json.loads(response_content)
    name = "".join(data["content"]["name"])

    avatar_url = "".join(data["content"]["avatarUrl"])

    return name, avatar_url


# Initialize the client class.
# App ID is fine to be public, it's not a secret
RPC = Presence("1324497000779218944")
RPC.connect()

start_time = time.time()

while True:  # The presence will stay on as long as the program is running
    fronter, avatarURL = get_data()
    # Set the presence and output to console
    print(
        RPC.update(
            state="(from Simply Plural)",
            details=fronter,
            large_image=avatarURL,
            large_text=fronter,
            start=start_time,
        )
    )  # Set the presence
    time.sleep(15)  # Can only update rich presence every 15 seconds
