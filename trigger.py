import requests
import random

TOKEN = "TOKEN_HERE"

URL = input("Enter tunnel URL: ").rstrip("/") + "/send"
GUILD_ID = input("Enter server ID: ")

while True:
    command = input("Enter command (or 'im done' to exit): ")
    if command.lower() == "im done":
        break
    
    response = requests.post(URL, json={
        "command": command,
        "guild_id": GUILD_ID
    })
    print(response.text)
    
    
