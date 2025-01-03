import json
import time
from pathlib import Path
from pypresence import Presence  # For setting up Discord RPC
import requests  # Will be needed later for SP requests


SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# Load secrets from file, this includes your Simply PLugin API key
secretsPath = Path("secrets.json")
with secretsPath.open(encoding="utf-8") as file:
    secrets: dict[str, str] = json.load(file)


def get_data() -> tuple[str, str]:
    """This function gets the fronter data from Simply Plural. \n
    Assume everything here breaks if there are multiple fronters"""
    payload: dict = {}
    headers: dict[str, str] = {"Authorization": secrets["SimplyPluralAPIKey"]}

    response = requests.request(
        "GET",
        SIMPLY_PLURAL_BASE_URL + "/fronters/",
        headers=headers,
        data=payload,
        timeout=10,
    )
    response_content: str = response.text
    data = json.loads(response_content)
    # Get current fronters, this probably breaks if there are multiple fronters
    # Stripping out anything that isn't a member ID such as [] and ''
    fronters = "".join([item["content"]["member"] for item in data])

    # Get uid (system ID)
    uid = "".join([item["content"]["uid"] for item in data])

    # Get the name of the fronter using the uid and member id
    # This 100% breaks if there are multiple fronters
    response = requests.request(
        "GET",
        SIMPLY_PLURAL_BASE_URL + "/member/" + uid + "/" + fronters,
        headers=headers,
        data=payload,
        timeout=10,
    )
    response_content: str = response.text
    data = json.loads(response_content)
    name: str = "".join(data["content"]["name"])

    avatar_url: str = "".join(data["content"]["avatarUrl"])

    return name, avatar_url


# Initialize the client class.
# App ID is fine to be public, it's not a secret
RPC = Presence("1324497000779218944")
RPC.connect()

start_time: float = time.time()

while True:  # The presence will stay on as long as the program is running
    fronter, avatarURL = get_data()
    # Set the presence and output to console
    if avatarURL:
        print(
            RPC.update(
                state="(from Simply Plural)",
                details=fronter,
                large_image=avatarURL,
                large_text=fronter,
                start=int(start_time),
            )
        )
    else:
        print(
            RPC.update(
                state="(from Simply Plural)",
                details=fronter,
                start=int(start_time),
            )
        )
    time.sleep(15)  # Can only update rich presence every 15 seconds
