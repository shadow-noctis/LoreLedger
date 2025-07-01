import load
import matching

def new_character():
    while True:
        #read characters.json
        characters = load.load_characters()
        
        print("\nAdding new Character:")
        print("Return to Main menu: back")
        name = input("Name: ")

        if name == "exit" or name == "back":
            return
        
        #Check if character already exists and return if True:
        if name in characters:
            print("Character already exists.\nExiting...")
            return

        #Check if part of name already exists:
        matches = matching.partial_matches(characters, name)
        if matches != []:
            print("Similar names found:\n")
            for match in matches:
                print(match)
            print()
            while True:
                confirm = input(f"Continue creating new character with name {name}? (y/n)").lower().strip()
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
        story = input ("Appears in... ")

            

        # Family & story => list
        family_members = family.strip().split(", ")
        story_list = story.strip().split(", ")
        
        
        # Add character info into dictionary (characters)
        characters[name] = {
            "Age": age,
            "Gender": gender,
            "Family": family_members,
            "Appearance notes": appearance,
            "Titles": story_list
        }
        
        #Save to JSON file (characters.json):
        load.save_characters(characters)
        print("Character succesfully added to your LoreLedger!\n")


        #Further development: Option to add new character, return to main menu or exit.