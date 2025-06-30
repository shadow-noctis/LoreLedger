import os
import json

def load_characters():
    if os.path.isfile("characters.json"):
        with open("characters.json", "r") as file:
            characters = json.load(file)
            return characters
    return {}