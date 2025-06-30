import json
import os.path
import load

def new_character():
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    family = input("Family members: ")
    appearance = input("Appearance notes: ")

    characters = load.load_characters()
    if name in characters:
        print("Character already exists.\n Exiting...")
        return
   
        #To be added:
        """
        Better error handling (if name is empty etc.)
            Options:
                1. Edit Character (later implementation)
                2. Overwrite old
                3. Read existing character sheet
                4. Exit
        """
    # Family => list
    family_members = family.strip().split(", ")
    
    
    # Add character info into dictionary (characters)
    characters[name] = {
        "Age": age,
        "Gender": gender,
        "Family": family_members,
        "Appearance notes": appearance
    }
    
    #Save to JSON file (characters.json):
    with open("characters.json", "w") as out_file:
        json.dump(characters, out_file, indent=4)
        print("Character succesfully added to your LoreLedger!")
        #Further development: Option to add new character, return to main menu or exit.

new_character()