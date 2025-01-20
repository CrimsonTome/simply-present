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


def get_data() -> tuple[list[tuple[str, str]], str]:
    """This function gets the fronter data from Simply Plural."""
    payload: dict = {}
    headers: dict[str, str] = {"Authorization": secrets["SimplyPluralAPIKey"]}

    response: requests.Response = requests.request(
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
    # fronters = " ".join([item["content"]["member"] for item in data])
    # ^ not anymore, it's now an array of member IDs

    # get the fronter ids in an array
    fronter_list = [item["content"]["member"] for item in data]
    # print(fronter_list)

    # Get uid (system ID)
    # only need to get for first member as it's the same for all members
    uid = data[0]["content"]["uid"]
    # print(uid)

    fronters_concat = []

    # suppress warning for now...
    # pylint: disable=consider-using-enumerate
    for i in range(len(fronter_list)):
        response = requests.request(
            "GET",
            SIMPLY_PLURAL_BASE_URL + "/member/" + uid + "/" + fronter_list[i],
            headers=headers,
            data=payload,
            timeout=10,
        )
        # print(response)
        response_content: str = response.text
        data = json.loads(response_content)
        name: str = data["content"]["name"]
        avatar_url: str = data["content"]["avatarUrl"]
        fronters_concat.append((name, avatar_url))

    # Get the avatar URL of the fronter
    avatar_url: str = fronters_concat[0][1]

    return fronters_concat, avatar_url


# Initialize the client class.
# App ID is fine to be public, it's not a secret
RPC = Presence("1324497000779218944")
RPC.connect()

start_time: float = time.time()

while True:  # The presence will stay on as long as the program is running
    fronters, avatarURL = get_data()
    # Convert fronters list to a string
    # pylint: disable=invalid-name
    fronter_details: str = " & ".join([name for name, _ in fronters])
    # Set the presence and output to console
    if avatarURL:
        print(
            RPC.update(
                state="(from Simply Plural)",
                # set details to all active fronter names
                details=fronter_details,
                large_image=avatarURL,
                # set large text to first fronter name because the avatar is the first fronter too
                large_text=fronters[0][0],
                start=int(start_time),
            )
        )
    else:
        print(
            RPC.update(
                state="(from Simply Plural)",
                details=fronter_details,
                start=int(start_time),
            )
        )
    time.sleep(15)  # Can only update rich presence every 15 seconds
