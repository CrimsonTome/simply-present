from pypresence import Presence # For setting up Discord RPC
import time
import requests # Will be needed later for SP requests
from pathlib import Path
import json
import time


SIMPLY_PLURAL_BASE_URL = "https://api.apparyllis.com/v1"

# Load secrets from file, this includes the DiscordAppID and your Simply PLugin API key
secretsPath = Path('secrets.json')
with secretsPath.open() as file:
    secrets = json.load(file)

# Assume everything here breaks if there are multiple fronters
def getData():
    payload={}
    headers = {
    'Authorization': secrets['SimplyPluralAPIKey']
    }   

    response = requests.request("GET", SIMPLY_PLURAL_BASE_URL+"/fronters/", headers=headers, data=payload)
    responseContent = response.text
    data = json.loads(responseContent)
    # Get current fronters, this probably breaks if there are multiple fronters, stripping out anything that isn't a member ID such as [] and ''
    fronters = ''.join([item['content']['member'] for item in data])
    # print(members)

    # Get uid (system ID)
    uid = ''.join([item['content']['uid'] for item in data])
    # print(uid)

    # Get the name of the fronter using the uid and member id
    # This 100% breaks if there are multiple fronters
    response = requests.request("GET", SIMPLY_PLURAL_BASE_URL + "/member/" + uid + "/" + fronters, headers=headers, data=payload)
    responseContent = response.text
    data = json.loads(responseContent)
    name = ''.join(data['content']['name'])
    # print(name)

    avatarURL = ''.join(data['content']['avatarUrl'])
    # print(avatarURL)
    
    return name, avatarURL

# Start the RPC connection
CLIENT_ID = secrets['DiscordAppID']
RPC = Presence(CLIENT_ID)  # Initialize the client class
RPC.connect() # Start the RPC connection
startTime=time.time()

while True:  # The presence will stay on as long as the program is running
    fronter, avatarURL = getData()
    # Set the presence
    print(RPC.update(state="(from Simply Plural)", details=fronter, large_image=avatarURL, large_text=fronter, start=startTime))# Set the presence
    time.sleep(15) # Can only update rich presence every 15 seconds
