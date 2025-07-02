import load
import matching
import read_character

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
        
        
        # Add character info into dictionary
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
        confirm = input("Would you like to add another character? (Y/n) ")
        if confirm == "n":
            break

def delete():
    print("            === Deletion options: ===   \n")
    print("  all         -  delete *ALL* characters.")
    print("  character   -  delete specific character from LoreLedger")
    print("  rule        -  delete all characters with specific condition (e.g. delete all characters of specific story)")
    print("  clearbackup -  delete your backup (Note! Backup not yet available.)")
    print("  back        -  return to main menu\n")
    print("                        === Important ===")
    print("LoreLedger does not currently have option to recover deleted files.")
    print("         Deleting character info will be permanent\n")
    print("             ~ Happy deleting will lead to void ~\n")

    while True:
        delete_type = input("What would you like to delete: ")
        match delete_type:
            case "all":
                delete_all()
            case "character":
                delete_character()
            case "rule":
                print("Rule deleting not yet available (Coming soon)")
            case "clearbackup":
                print("Backup not yet available. Practice caution when deleting something from your LoreLedger.")
            case "back":
                return
            case "exit":
                return
            case _:
                print("Unknown command. Please refer to the list above or return to main menu by typing 'back'")
                continue
        return

def delete_all():
    print("                         === WARNING === ")
    print("You are about to delete ALL characters currently stored in your LoreLedger")
    print("LoreLedger does *not* currently support backup. *All* files will be permanently deleted.")
    confirm = input("Please type in 'delete all my characters' to confirm you wish to proceed: ")
    if confirm == "delete all my characters":
        print("Deleting all characters...")
        load.save_characters({})
        print("Your LoreLedger is now empty.\nReturning back to Main Menu")
        return
    print("Canceling delete...")
    return

def delete_character():
    print("                         === WARNING === ")
    print("You are about to delete a character currently stored in your LoreLedger")
    print("         LoreLedger does *not* currently support backup.")
    print("            ~ Happy deleating will lead to void ~\n")
    while True:
        to_delete = input("Which character would you like to delete: ")
        characters = load.load_characters()
        if to_delete == "back" or to_delete == "exit":
            return
        elif to_delete == "list":
            read_character.list_all()
            return     
        if to_delete not in characters:
            print("Exact match not found...")
            print("Searching for close matches...")
            matches = matching.partial_matches(characters, to_delete)
            if len(matches) == 0:
                print("Error: Character not found.")
                print("To instead move to listing all characters type: 'list'")
                continue
            elif len(matches) == 1:
                print(f"One close match found:\n   - {matches[0]}")
                if_right = input(f"Would you like to delete character {matches[0]}? (y/N) ")
                if if_right == "y" or if_right == "yes":
                    to_delete = matches[0]
                else:
                    print("To list all characters instead type 'list'")
                    continue
            else:
                print("Close matches found.")
                print("Did you mean: ")
                print()
                for match in matches:
                    print(f"- {match}")
                print()
                continue

        print("\n                === WARNING ===")
        print(f"You are about to delete character: {to_delete}")
        confirm = input(f"Are you sure you want to proceed? (y/N) ").lower()
        if confirm != "y" and confirm != "yes":
            print("Delete canceled: Your character remains safe.")
            new = input("Would you like to delete another character? (y/N) ")
            if new != "yes" and new != "y":
                print("Returning to Main Menu...")
                return
            else:
                continue
        print(f"Deleting character {to_delete}...")
        characters.pop(to_delete)
        load.save_characters(characters)
        print("Character succesfully deleted from your LoreLedger!")
        new = input("Would you like to delete another character? (y/N) ").lower()
        if new != "yes" and new != "y":
            print("Returning to Main Menu...")
            return