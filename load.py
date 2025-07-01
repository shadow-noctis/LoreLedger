import os
import json

def load_characters():
    if os.path.isfile("characters.json"):
        with open("characters.json", "r") as file:
            characters = json.load(file)
            return characters
    return {}


def save_characters(characters):
    with open("characters.json", "w") as out_file:
        json.dump(characters, out_file, indent=4)