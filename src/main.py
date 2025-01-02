from pypresence import Presence # For setting up Discord RPC
import time
import requests # Will be needed later for SP requests
from pathlib import Path
import json

# Load secrets from file, this includes the DiscordAppID and your Simply PLugin API key
secretsPath = Path('secrets.json')
with secretsPath.open() as file:
    secrets = json.load(file)

# Start the RPC connection
CLIENT_ID = secrets['DiscordAppID']
RPC = Presence(CLIENT_ID)  # Initialize the client class
RPC.connect() # Start the RPC connection

# Debug print to make sure the connection was successful
print(RPC.update(state="Lookie Lookie", details="A test of qwertyquerty's Python Discord RPC wrapper, pypresence!"))  # Set the presence

while True:  # The presence will stay on as long as the program is running
    time.sleep(15) # Can only update rich presence every 15 seconds