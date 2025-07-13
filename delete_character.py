import ui
import load
import read_character
import matching
import os
import shutil

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
                ui.confirm_exit()
            case _:
                print("Unknown command. Please refer to the list above or return to main menu by typing 'back'")
                continue
        return

#Delete all characters:
def delete_all():
    print("                         === WARNING === ")
    print("You are about to delete ALL characters currently stored in your LoreLedger")
    confirm = input("Please type in 'delete all my characters' to confirm you wish to proceed: ")
    if confirm.lower() == "back":
        print(" == Delete cancelled == ")
        print("Returning to Main Menu...")
        return
    elif confirm != "delete all my characters":
        print(f"{confirm} does not match 'delete all my characters'")
        confirm = input("Please type in 'delete all my characters' to confirm you wish to proceed: ")
        if confirm != "delete all my characters":
            print(" == Delete cancelled == ")
            print("Returning to Main Menu...")
            return
    #Create backup if needed:
    if ui.if_yes_no("Would you like to backup your characters?"):
        shutil.copy("characters.json", "characters_backup.json")
        print("Backup created")

    print("Deleting all characters...")
    if os.path.exists("characters.json"):
        os.remove("characters.json")
        print("Your LoreLedger is now empty.\nReturning back to Main Menu")
    else:
        print("Your LoreLedger is already empty.\n Returning back to Main Menu")

def backup():
    print(" === Backup options ===")
    print("  - Restore deleted characters currently not in your LoreLedger")
    print("  - Restore characters after")

#Restore previous state before using delete_all
def restore_backup():
    print(" === RESTORE PREVIOUS STATE ===")
    if os.path.exists("characters_backup.json") == False:
        print("Error: No backup file found.")
        print("Returning to Main Menu...")
        return
    print("\n== IMPORTANT! ==")
    print("Restoring previus state will OVERWRITE current characters in your LoreLedger")
    print("Use backup to restore previously deleted characters not in your LoreLedger anymore")
    if ui.if_yes_no("Are you sure you want to return to previous state before delete all?"):     
        characters = load.load_characters(file="characters_backup.json")
        load.save_characters(characters)
        os.remove("characters_backup.json")
        print("Previous state succesfully restored\n")
    else:
        print("Restore cancelled")
    print("Returning to Main menu...")


#Restore deleted characters saved in deleted_characters.json
def restore_deleted_characters():
    if ui.if_yes_no("Restore deleted characters?"):
        #Check first if backup file exists:
        if os.path.isfile("deleted_characters.json"):
            backup_characters = load.load_characters(file="deleted_characters")
        else:
            print("Error: Backup file does not exist")
            print("Returning to Main Menu...") 
            return

        #Loop through characters and add any deleted characters into current characters.json dictionary
        characters = load.load_characters()
        for name in backup_characters:
            if name not in characters:
                characters[name] = backup_characters[name]
        load.save_characters(characters)
        print("Characters succesfully restored")
        if ui.if_yes_no("Delete backup file?"):
            os.remove("deleted_characters.json")
            print("Backup file cleared")
    else:
        print("Restore cancelled")
    print("Returning to Main Menu...")

#Delete single character
def delete_character():
    print("                         === WARNING === ")
    print("You are about to delete a character currently stored in your LoreLedger")
    print("Restoring previously deleted characters is not currently possible")
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
                if ui.if_yes_no(f"Would you like to delete character {matches[0]}?", no_priority=True) == False:
                    to_delete = matches[0]
                else:
                    print("To list all characters type 'list'")
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
        if ui.if_yes_no(f"Are you sure you want to proceed?") == False:
            print("Delete canceled")
            continue

        print(f"Deleting character {to_delete}...")
        backup_character = characters.pop(to_delete)
        load.save_characters(characters)
        backup_file = load.load_characters(file="deleted_characters.json")
        backup_file[to_delete] = backup_character
        load.save_characters(backup_file, file="deleted_characters.json")
        print("== Character succesfully deleted from your LoreLedger. ==")
        if ui.if_yes_no("Delete another character?", no_priority=True) == False:
            print("Returning to Main Menu...")
            return