import copy
import load
import matching
import read_character
import ui

importance_tags = ["Main", "Important", "Recurring", "Side"]
def new_character():
    #read characters.json
    characters = load.load_characters()
    
    print("\n=== Adding new Character ===")
    surname = input("Surname: ")
    if surname.lower() == "back":
        return
    elif surname.lower() == "exit":
        ui.confirm_exit()
        return

    given_name = input("Given names: ")
    name = f"{given_name} {surname}"
    
    #Check if character already exists and return if True:
    if name in characters:
        print("Character already exists.\n")
        if ui.if_yes_no("Overwrite old character?", no_priority=True) == False:
            print("Character creation cancelled.\nReturning to Main Menu...")

    #Check if part of name already exists:
    matches = matching.partial_matches(characters, given_name, surname)
    if matches != []:
        print("Similar names found:\n")
        for match in matches:
            print(f" - {match} {surname}")
        print()
        if ui.if_yes_no(f"Continue creating new character with name {name}?", yes_priority=True) == False:
            print("Character creation canceled...")
            return

    #Collect necessary information:
    general_info = input("General information: ")
    age = input("Age: ")
    gender = input("Gender: ")
    print("You can add titles separated by comma or type '/detailed' to add one item at time.")
    story = input("Titles: ").strip()
    if story.lower() == "/detailed":
        story = add_list_field("Titles", message="Title: ")
    else:
        story = matching.to_list(story)
    importance = numbered_list(importance_tags, message="Choose one: ")
    
    # Add character info into dictionary
    characters[name] = {
        "Description": general_info,
        "Age": age,
        "Gender": gender,
        "Titles": story,
        "Importance": importance
    }

    if ui.if_yes_no("Would you like to add custom fields?", no_priority=True):
        add_custom_fields(characters[name])
    
    print(f"\n === {name} === ")
    for key in characters[name]:
        print(f"  - {key}: {characters[name][key]}")
    print()

    if ui.if_yes_no("Add character to LoreLedger?", yes_priority=True) == False:
        print("Character creation cancelled...")
        return

    #Save to JSON file (characters.json):
    ordered_characters = matching.reorder_characters(characters, importance_tags, "Importance")
    load.save_characters(ordered_characters)
    print("Character succesfully added to your LoreLedger!\n")
        
#Number all possible options before checking if the answer is valid. Resets loop if answer invalid
def numbered_list(options, message="Your answer: "):
    while True:
        #Set numbering to begin from one
        i = 1
        for option in options:
            print(f"{i}. {option}")
            i += 1
        print("\nEnter the number or name")
        answer = input(message).strip()
        if answer.lower() == "back":
            return "BACK"
        elif answer.lower() == "exit":
            ui.confirm_exit()
            continue
        #Clean field name and capitalize it for comparison of all keys
        answer_clean = answer.strip().capitalize()
        if answer_clean in options:
            return answer_clean
        else:
            try:
                num_answer = int(answer)
                if 1 <= num_answer <= len(options):
                    return options[int(answer) -1]
                else:
                    print(f"Error: No option {answer}")    
            except ValueError:
                print("Error: field not found")
                print("Type number OR name")


# Add list item by item option or add custom field if list
def add_list_field(field, message="Add: "):
    print(f"\nYou can add multiple items in {field} (Leave empty to stop)")
    print("Useful tip: type '/drop' to cancel previous input\n")
    to_add_list = []
    while True:
        to_add = input(message)
        if to_add.strip() == "":
            return to_add_list
        elif to_add.strip().lower() == "/drop":
            if len(to_add_list) == 0:
                print(f"{field} is already empty")
            to_add_list.pop()
        else:
            to_add_list.append(to_add)


def add_custom_fields(character):
    print("\nAdd first descriptive name (Skills, Appearance, Home town, etc.)")
    print("Add then relative information to that field\n")
    #Ask for custom field name
    field = input("Custom field name: ")
    if ui.if_yes_no(f"Is {field} a list?", no_priority=True):
        #If the custom field is list, collect the values with add_list_field:
        field_value = add_list_field(field, f"{field}: ")
    #Otherwise ask for the value for the field
    else:
        field_value = input(f"{field}: ")
    #Append to custom_fields list as a tuple:
    character[field] = field_value
    #Ask if user wants to add another custom field and return all custom field tuples as list to use.
    return character

        
def edit_character(to_edit):
    while True:
        characters = load.load_characters()
        #"list" gives option to list all characters before restarting the loop
        if to_edit == "list":
            read_character.list_all(side=True)
            to_edit = input("Which character would you like to edit? ")
            continue
        elif to_edit.lower().strip() == "back":
            print("Returning to Main Menu...")
            return
        elif to_edit.lower().strip() == "exit":
            ui.confirm_exit()
            print("Returning to Main Menu...")
            return
        #No exact match found
        if to_edit in characters:
            break
        else:
            if len(to_edit.split()) > 1:
                token_match = token_search(characters, to_edit)
                if token_match != False:
                    to_edit = token_match
                    break

            matches = matching.partial_matches(characters, to_edit)
            #No matches found
            if matches == []:
                print("Error: Character not found.")
                print("Please try another name or type 'list' to view all characters.")
                to_edit = input("Which character would you like to edit? ")
                continue

            #One match found: Asks user if they want to edit that character:
            elif len(matches) == 1:
                print("Similar name found:\n")
                print(f"  - {matches[0]}\n")
                if ui.if_yes_no(f"Would you like to edit {matches[0]}?", yes_priority=True) == False:
                    print("Please try another name or type 'list' to list all characters")
                    to_edit = input("Which character would you like to edit? ")
                    continue
                else:
                    to_edit = matches[0]

                #Multiple matches found. List them and ask for a new name
                #Further development: numbered list user can choose from
            else:
                print("Did you mean: \n")
                for name in matches:
                    print(f"  - {name}")
                to_edit = input("Which character would you like to edit? ")
                continue

    # Save unedited character and edit copy or the dictionary
    edited = copy.deepcopy(characters) 
    old_character = copy.deepcopy(characters[to_edit])
    while True:
        name, updated = get_edit_info(edited, to_edit)

        if updated == False:
            print("Edit cancelled...")
            print("Returning to Main Menul...")
            return

        #Print edit details for the user to confirm if they wish to save the changes made
        print("\n   === EDIT DETAILS ===\n")
        if name != to_edit:
            print(f" == {to_edit} → {name} == ")
        else:
            print(f" === {name} === ")
        for key in old_character:
            if key in updated:
                if old_character[key] != updated[key]:
                    print(f" {key}: {old_character[key]} → {updated[key]}")
            if key not in updated:
                print(f"{key}:{old_character[key]} → deleted")
        added_fields = set(updated) - set(old_character)
        for added in added_fields:
            print(f" Added field → {added}: {updated[added]}")

        #Confirm changes:
        if ui.if_yes_no("\nSave changes?", yes_priority=True) == False:
            if ui.if_yes_no("Continue eiditing? ", no_priority=True) == False:
                print("Character edit canceled\n")
                return
            else:
                continue
                
        #Reorder character's dictionary and character sheet before saving.
        updated = reorder_sheet(updated)
        edited[name] = updated
        ordered_characters = matching.reorder_characters(characters, importance_tags, "Importance")

        #Save to JSON file
        load.save_characters(edited)
        print("== Character succesfully updated ==\n")
        print("Returning to Main Menu...")
        return


#Search by token in query name to verify if all names found in a key inside JSON:
def token_search(characters, name):
    for character in characters:
        if matching.token_match(name, character):
            if ui.if_yes_no(f"Did you mean: {character} ", yes_priority=True):
                return character
            else:
                return False
    return False


#Helper function to search for
def get_edit_info(characters, name):
    while True:
        fields = ["Name"]
        for field in characters[name]:
            fields.append(field)
        fields.append("Add")
        field = numbered_list(fields, message="Which field would you like to edit: ")
        if field == "BACK":
            return name, characters[name]
        #Add custom fields to character:
        elif field == "Add":
            add_custom_fields(characters[name])

        elif field == "Name": 
            new_name = input("New Name: ")
            characters[new_name] = characters.pop(name)
            name = new_name

        elif field == "Importance":
            new_importance = numbered_list(importance_tags, message="New importance tag: ")
            characters[name][field] = new_importance
        #Edit character:
        else:
            while True:
                action = input(f"Would you like to edit or delete {field}? (edit/delete): ").lower().strip()

                #Delete field instead of 
                if action == "delete":
                    handle_delete_field(characters[name], field)
                    break
                elif action == "edit":
                    if type(characters[name][field]) is list:
                        while True:
                            new_info = input(f"Add to {field}: ").strip()
                            if new_info == "":
                                break
                            characters[name][field].append(new_info)
                    else:
                        new_info = input(f"Change {field} to: ")
                        characters[name][field] = new_info
                    break
                else:
                    print("Invalid option. Please type 'edit' or 'delete'.")

        if ui.if_yes_no("Continue editing?", yes_priority=True) == False:
            return name, characters[name]


def handle_delete_field(character, field):
    if isinstance(character[field], list):
        matching.print_numbered_list(character[field])
        choice = input("\nType the number of the item to remove or type 'all' to delete the entire field: ").strip()
        if choice == "all":
            del character[field]
            print(f"{field} deleted")
        else:
            try:
                index = int(choice) -1
                if 0 <= index < len(character[field]):
                    deleted = character[field].pop(index)
                    print(f"{deleted} deleted from {field}")
                else:
                    print("Invalid number")
            except ValueError:
                print("Invalid input.")
    else:
        if ui.if_yes_no(f"Delete entire field: {field}?"):
            del character[field]
            print(f"{field} deleted")
        else:
            print("Deletion cancelled")


def reorder_sheet(character):
    reordered = {}
    for field in character:
        if field != "Titles":
            reordered[field] = character[field]
    if "Titles" in character:
        reordered["Titles"] = character["Titles"]
    for field in character:
        if field != "Importance":
            reordered[field] = character[field]
    if "Importance" in character:
        reordered["Importance"] = character["Importance"]
    return reordered