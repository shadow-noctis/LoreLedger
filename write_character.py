import copy
import load
import matching
import read_character
import ui

def new_character():
    while True:
        #read characters.json
        characters = load.load_characters()
        
        print("\n=== Adding new Character ===")
        surname = input("Surname: ")
        if surname.lower() == "back":
            return
        elif surname.lower() == "exit":
            ui.confirm_exit()

        given_name = input("Given names: ")
        name = f"{given_name} {surname}"
        
        #Check if character already exists and return if True:
        if name in characters:
            print("Character already exists.\n")
            continue

        #Check if part of name already exists:
        matches = matching.partial_matches(characters, given_name, surname)
        if matches != []:
            print("Similar names found:\n")
            for match in matches:
                print(f" - {match} {surname}")
            print()
            if ui.if_restart(f"Continue creating new character with name {name}? (Y/n) ", yes_priority=True) == False:
                print("Character creation canceled...")
                continue

        #To be added:
        """
            Better options for user (if name is empty etc.)
                Options:
                    1. Edit Character (later implementation)
                    2. Overwrite old
                    3. Read existing character sheet
                    4. Exit
        """

        #Collect necessary information:
        age = input("Age: ")
        gender = input("Gender: ")
        print("You can add story titles and family members separated by comma or type '/detailed' to add one item at time.")
        family = input("Family members: ").strip()
        if family.lower() == "/detailed":
            family = add_list_field("Family", message="Add family member: ")
        else:
            family = to_list(family)
        story = input("Titles related to character: ").strip()
        if story.lower() == "/detailed":
            story = add_list_field("Titles", message="Add related title: ")
        else:
            story = to_list(story)
        
        # Add character info into dictionary
        characters[name] = {
            "Age": age,
            "Gender": gender,
            "Family": family,
            "Titles": story
        }

        if ui.if_restart("Would you like to add custom fields? (y/N) ", no_priority=True):
            custom_fields = add_custom_fields()
            for custom_field in custom_fields:
                characters[name][custom_field[0]] = custom_field[1]
        
        print(f"\n === {name} === ")
        for key in characters[name]:
            print(f"  - {key}: {characters[name][key]}")
        print()

        if ui.if_restart("Add character to LoreLedger? [Y/n] ", yes_priority=True) == False:
            print("Character creation cancelled...")
            continue

        #Save to JSON file (characters.json):
        load.save_characters(characters)
        print("Character succesfully added to your LoreLedger!\n")

        #Ask if user wants to add another character
        if ui.if_restart("Add another character? [Y/n] ", yes_priority=True) == False:
            print("Returning to Main Menu... ")
            return

# Turn comma separated items to a list
def to_list(items):
    return items.strip().split(", ")

# Add list item by item option or add custom field if list
def add_list_field(field, message="Add: "):
    print(f"\nYou can add multiple items in {field} (Leave empty to stop)")
    print("Useful tip: type 'drop' to cancel previous input\n")
    to_add_list = []
    while True:
        to_add = input(message)
        if to_add.strip() == "":
            return to_add_list
        elif to_add.strip().lower() == "drop":
            if len(to_add_list) == 0:
                print(f"Your current {field} is empty")
            to_add_list.pop()
        else:
            to_add_list.append(to_add)
        print(f"{field}: {to_add_list}")


def add_custom_fields():
    print("\nAdd first descriptive name (Skills, Appearance, Home town, etc.)")
    print("Add then relative information to that field\n")
    custom_fields = []
    while True:
        #Ask for custom field name
        field = input("Custom field name: ")
        if ui.if_restart(f"Is {field} a list? (y/N): ", no_priority=True):
            #If the custom field is list, collect the values with add_list_field:
            field_value = add_list_field(field, f"{field}: ")
        #Otherwise ask for the value for the field
        else:
            field_value = input(f"{field}: ")
        #Append to custom_fields list as a tuple:
        custom_fields.append((field, field_value))
        #Ask if user wants to add another custom field and return all custom field tuples as list to use.
        if ui.if_restart("Would you like to add another custom field? (Y/n): ", yes_priority=True) == False:
            return custom_fields



#Menu for deleting
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

#Delete all characters:
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

#Delete single character
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
                if ui.if_restart(f"Would you like to delete character {matches[0]}? (y/N) ", no_priority=True) == False:
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
        if ui.if_restart(f"Are you sure you want to proceed? (y/N) ") == False:
            print("Delete canceled")
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
        #"list" gives option to list all characters before restarting the loop
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
                continue

            #One match found: Asks user if they want to edit that character:
            elif len(matches) == 1:
                print("Similar name found:\n")
                print(f"  - {matches[0]}\n")
                if ui.if_restart(f"Would you like to edit {matches[0]}? (Y/n) ", yes_priority=True) == False:
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

        # Save unedited character and edit copy or the dictionary
        edited = copy.deepcopy(characters) 
        old_character = copy.deepcopy(characters[to_edit])
        name, updated = get_edit_info(edited, to_edit)

        if updated == False:
            print("Edit cancelled...")
            continue

        print("\n   === EDIT DETAILS ===\n")
        print("Previous character information:\n")
        print(f" === {to_edit} === ")
        for key in old_character:
            print(f"{key}: {old_character[key]}")

        print()
        print(" == New Information: == \n")
        print(f" === {name} === ")
        for key in updated:
            print(f"{key}: {updated[key]}")

        #Confirm changes:
        if ui.if_restart("Save changes? (Y/n) ", yes_priority=True) == False:
            print("Character edit canceled")
            
        #Save to JSON file:
        load.save_characters(edited)
        print("== Character succesfully updated ==\n")

        if ui.if_restart("Would you like to edit another character? (Y/n) ", yes_priority=True) == False:
            print("Returning to Main Menu...")
            return

#Helper function to search for
def get_edit_info(characters, name):
    while True:
        field = get_field(characters, name)
        if field == "BACK":
            return name, False
        # If field is a list, append new information into it.
        elif field != "Name":
            if type(characters[name][field]) is list:
                print("To instead delete from list type '/delete'")
                new_info = input(f"Add to {field}: ").strip()
                if new_info.lower() == "/delete":
                    updated_list = delete_from_list(name)
                    characters[name][field] = updated_list
                else:
                    characters[name][field].append(new_info)
            else:
                new_info = input(f"Change {field} to: ")
                characters[name][field] = new_info
        else: 
            new_name = input("New Name: ")
            characters[new_name] = characters.pop(name)
            name = new_name

        if ui.if_restart("Continue editing? (Y/n)", yes_priority=True) == False:
            return name, characters[name]


def delete_from_list(characters, name):
    print("not yet availabe")
    return

#Number each key for the specific character and number them. Allows to choose which to edit
def get_field(characters, name):
    while True:
        i = 1
        fields = ["Name"]
        print("1. Name")
        for key in characters[name]:
            i += 1
            print(f"{i}. {key}")
            fields.append(key)
        print("\nEnter the number or name of field")
        field = input("Which field would you like to edit: ").strip().capitalize()
        if field == "Back" or field == "New":
            return "BACK"
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