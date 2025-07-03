import load
import matching
import read_character
import ui

def new_character():
    while True:
        #read characters.json
        characters = load.load_characters()
        
        print("\n=== Adding new Character ===")
        name = input("Name: ")

        if name == "back":
            return
        elif name == "exit":
            ui.confirm_exit()
        
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
            if ui.if_restart(f"Continue creating new character with name {name}? (Y/n) ", yes_priority=True) == False:
                print(f"Character creation canceled with name {name}...")
                continue

        #To be added:
        """
            Better error handling (if name is empty etc.)
                Options:
                    1. Edit Character (later implementation)
                    2. Overwrite old
                    3. Read existing character sheet
                    4. Exit
        """

        #Collect necessary information:
        age = input("Age: ")
        gender = input("Gender: ")
        family = input("Family members: ")
        story = input ("Appears in:  ")
        # Collect appearance features:
        appearance = []

        print("\nSuggested way to enter appearance:")
        print(" -  Start with a general description")
        print(" -  Then add specific features (e.g. 'Scar on left cheek')")
        print("You can stop at any time by pressing Enter with no input\n.")
        add_appearance = True
        while add_appearance:
            appearance_detail = input("Appearance detail: ").strip()
            print(appearance_detail)
            if appearance_detail == "":
                break
            appearance.append(appearance_detail)
            add = input("Add another detail? (y/N)").lower().strip()
            if add != "y" and add != "yes" and add != "":
                add_appearance = False


        # Turn family and story input to lists:
        family = to_list(family)
        story = to_list(story)
        
        
        # Add character info into dictionary
        characters[name] = {
            "Age": age,
            "Gender": gender,
            "Family": family,
            "Appearance": appearance,
            "Titles": story
        }
        
        print(f" === {name} === ")
        for key in characters[name]:
            print(f"  - {key}: {characters[name][key]}")

        if ui.if_restart("Add character to LoreLedger? [Y/n]", yes_priority=True) == False:
            print("Character creation cancelled...")
            continue

        #Save to JSON file (characters.json):
        load.save_characters(characters)
        print("Character succesfully added to your LoreLedger!\n")

        #Ask if user wants to add another character
        if ui.if_restart("Add another character? [Y/n] ") == False:
            print("Returning to Main Menu... ")
            return
        
def to_list(items):
    return items.strip().split(", ")

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
            continue
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
        print("== Character succesfully deleted from your LoreLedger. ==")
        if ui.if_restart("Delete another character? [y/N] ", no_priority=True) == False:
            print("Returning to Main Menu...")
            return
        
def edit_character():
    characters = load.load_characters()
    while True:

        to_edit = input("Which character would you like to edit? ")
        #List all characters before restarting the loop
        if to_edit == "list":
            read_character.list_all()
            continue
        #No exact match found
        if to_edit not in characters:
            print("Character not found in LoreLedger")
            print("Searching for similar names...")
            matches = matching.partial_matches(characters, to_edit)
            #No matches found
            if matches == []:
                print("Error: Character not found.")
                print("Please try another name or type 'list' to view all characters.")

            #One match found: Asks user if they want to edit that character
            if len(matches) == 1:
                print("Similar name found:\n")
                print(f"  - {matches[0]}\n")
                if ui.if_restart(f"Would you like to edit {matches[0]}? (y/N) ", no_priority=True) == False:
                    print("Please try another name or type 'list' to list all characters")
                    continue
                else:
                    to_edit = matches[0]
            #Multiple matches found. List them and ask for a new name
            #Further development: numbered list user can choose from
            else:
                print("Did you mean: \n")
                for name in matches:
                    print(f"  - {name}")
                continue

        #Asks user which field to edit (Name, Family, ect.)
        field = get_field(characters, to_edit)
        if field == "BACK":
            print("Returning to Main Menu...")
            return
        elif field == "RESTART":
            continue
        if field != "Name":
        #If field is a list, append new information into it.
            if type(characters[to_edit][field]) is list:
                    
                new_info = input(f"Add to {field}: ")
                old_info = characters[to_edit][field].copy()
                new_list = old_info.copy()
                new_list.append(new_info)
                new_info = new_list
            else:
                new_info = input(f"Change {field} to: ")
                old_info = characters[to_edit][field]
        else:
            new_info = input(f"Change {field} to: ")
            old_info = to_edit

        #Let's user view the changes to be made:
        print("\n   === EDIT DETAILS ===")
        print(f"\n  == {to_edit} ==")
        print(f"Old details    {field}: {old_info}")
        print(f"New details    {field}: {new_info}")

        #Confirm changes:
        if ui.if_restart("Save changes? (Y/n) ", yes_priority=True) == False:
            print("Character edit canceled")
            
        #Save to JSON file:
        if field != "Name":
            characters[to_edit][field] = new_info
        else:
            characters[new_info] = characters.pop(to_edit)

        load.save_characters(characters)
        print("== Character succesfully updated ==\n")

        if ui.if_restart("Would you like to edit another character? (Y/n) ", yes_priority=True) == False:
            print("Returning to Main Menu...")
            return


def get_field(characters, name):
    while True:
        i = 1
        fields = ["Name"]
        print("1. Name")
        for key in characters[name]:
            i += 1
            print(f"{i}. {key}")
            fields.append(key)
        field = input("(Enter number) Which field would you like to edit: ").strip().capitalize()
        if field == "Back":
            return "BACK"
        elif field == "New":
            return "RESTART"
        elif field == "Exit":
            ui.confirm_exit()
        elif field not in fields:
            field.strip(".")
            try:
                if int(field) > i or int(field) < 1:
                    print(f"Error: No option {int(field)}.")
                else:
                    return fields[int(field) -1]
            except:
                print("Error: field not found")
                print("Type only number or name of field (without number)")
                print("To edit another character type in 'new'")
        else:
            return field
        
def edit_name():
    print("Unavailable")