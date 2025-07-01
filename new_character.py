import json
import load
import name_check

def new_character():
    #read characters.json
    characters = load.load_characters()
    
    full_name = input("Name: ")
    each_name = full_name.split()

    #Check if character already exists and return if True:
    if full_name in characters:
        print("Character already exists.\nExiting...")
        return

    #Check if part of name already exists:
    for name in each_name:
        matches = name_check.if_name_exists(characters, name)
    if matches != []:
        print("Similar names found:\n")
        for match in matches:
            print(match)
            print()
        while True:
            confirm = input(f"Continue creating new character with name {full_name}? (y/n)").lower()
            if confirm == "n" or confirm == "no":
                print("Character creation canceled\nExiting...")
                return
            elif confirm == "y" or confirm == "yes":
                break
            else:
                print("Please enter 'yes' or 'no.")

    #To be added:
    """
        Better error handling (if name is empty etc.)
            Options:
                1. Edit Character (later implementation)
                2. Overwrite old
                3. Read existing character sheet
                4. Exit
    """

    age = input("Age: ")
    gender = input("Gender: ")
    family = input("Family members: ")
    appearance = input("Appearance notes: ")

        

    # Family => list
    family_members = family.strip().split(", ")
    
    
    # Add character info into dictionary (characters)
    characters[full_name] = {
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