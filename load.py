import os
import json

def load_characters(file="characters.json"):
    if os.path.isfile(file):
        with open(file, "r") as file:
            characters = json.load(file)
            return characters
    return {}


def save_characters(characters, file="characters.json"):
    with open(file, "w") as out_file:
        json.dump(characters, out_file, indent=4)