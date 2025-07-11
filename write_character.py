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
            if ui.if_restart(f"Continue creating new character with name {name}?", yes_priority=True) == False:
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

        if ui.if_restart("Would you like to add custom fields?", no_priority=True):
            add_custom_fields(characters[name])
        
        print(f"\n === {name} === ")
        for key in characters[name]:
            print(f"  - {key}: {characters[name][key]}")
        print()

        if ui.if_restart("Add character to LoreLedger?", yes_priority=True) == False:
            print("Character creation cancelled...")
            continue

        #Save to JSON file (characters.json):
        load.save_characters(characters)
        print("Character succesfully added to your LoreLedger!\n")

        #Ask if user wants to add another character
        if ui.if_restart("Add another character?", yes_priority=True) == False:
            print("Returning to Main Menu... ")
            return

# Turn comma separated items to a list
def to_list(items):
    return items.strip().split(", ")

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
    while True:
        #Ask for custom field name
        field = input("Custom field name: ")
        if ui.if_restart(f"Is {field} a list?", no_priority=True):
            #If the custom field is list, collect the values with add_list_field:
            field_value = add_list_field(field, f"{field}: ")
        #Otherwise ask for the value for the field
        else:
            field_value = input(f"{field}: ")
        #Append to custom_fields list as a tuple:
        character[field] = field_value
        #Ask if user wants to add another custom field and return all custom field tuples as list to use.
        if ui.if_restart("Would you like to add another custom field?", yes_priority=True) == False:
            return character

        
def edit_character():
    while True:
        
        characters = load.load_characters()
        to_edit = input("Which character would you like to edit? ")
        #"list" gives option to list all characters before restarting the loop
        if to_edit == "list":
            read_character.list_all()
            continue
        elif to_edit.lower().strip() == "back":
            print("Returning to Main Menu...")
            return
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
                if ui.if_restart(f"Would you like to edit {matches[0]}?", yes_priority=True) == False:
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
        if ui.if_restart("Save changes?", yes_priority=True) == False:
            print("Character edit canceled")
            continue
            
        #Save to JSON file:
        load.save_characters(edited)
        print("== Character succesfully updated ==\n")

        if ui.if_restart("Would you like to edit another character?", yes_priority=True) == False:
            print("Returning to Main Menu...")
            return

#Helper function to search for
def get_edit_info(characters, name):
    while True:
        field = get_field(characters[name], show_add_option=True)
        if field == "BACK":
            return name, False
        #Add custom fields to character:
        elif field == "Add":
            add_custom_fields(characters[name])

        #Edit character:
        else:

            while True:
                action = input(f"Would you like to edit or delete {field}? (edit/delete): ").lower().strip()

                #Delete field instead of 
                if action == "delete":
                    handle_delete_field(characters[name], field)
                    break
                elif action == "edit":

                    #Edit field
                    if field != "Name":
                        if type(characters[name][field]) is list:
                            new_info = input(f"Add to {field}: ").strip()
                            characters[name][field].append(new_info)
                        else:
                            new_info = input(f"Change {field} to: ")
                            characters[name][field] = new_info
                    else: 
                        new_name = input("New Name: ")
                        characters[new_name] = characters.pop(name)
                        name = new_name
                    break
                else:
                    print("Invalid option. Please type 'edit' or 'delete'.")

        if ui.if_restart("Continue editing?", yes_priority=True) == False:
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
        if ui.if_restart(f"Delete entire field: {field}?"):
            del character[field]
            print(f"{field} deleted")
        else:
            print("Deletion cancelled")



def delete_from_list(characters, name):
    print("not yet availabe")
    return

#Number each key for the specific character and number them. Allows to choose which to edit
def get_field(character, show_add_option=False):
    while True:
        i = 1
        fields = ["Name"]
        print("1. Name")
        #Print all options:
        for key in character:
            i += 1
            print(f"{i}. {key}")
            fields.append(key)
        
        if show_add_option:
            i += 1
            print(f"{i}. Add new field")
            fields.append("Add")

        print("\nEnter the number or name of field")
        field = input("Which field would you like to edit: ").strip()
        if field.lower() == "back":
            return "BACK"
        elif field.lower() == "exit":
            ui.confirm_exit()

        #Clean field name and capitalize it for comparison of all keys
        field_clean = field.strip().capitalize()

        if field_clean == "Add new field":
            field_clean == "Add"

        if field_clean in fields:
            return field_clean
        
        else:
            try:
                choice = int(field)
                if 1 <= choice <= len(fields):
                    return fields[int(field) -1]
                else:
                    print(f"Error: No option {field}")       
            except ValueError:
                print("Error: field not found")
                print("Type only number or name of field (without number)")
                print("To edit another character type in 'new'")