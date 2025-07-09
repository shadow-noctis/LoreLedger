import ui
import load
import read_character
import matching
import os

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
    if confirm != "delete all my characters":
        print(f"{confirm} does not match 'delete all my characters'")
        confirm = input("Please type in 'delete all my characters' to confirm you wish to proceed: ")
        if confirm != "delete all my characters":
            print(" == Delete cancelled == ")
            print("Returning to Main Menu...")
            return
    print("Deleting all characters...")
    if os.path.exists("characters.json"):
        os.remove("characters.json")
        print("Your LoreLedger is now empty.\nReturning back to Main Menu")
    else:
        print("Your LoreLedger is already empty.\n Returning back to Main Menu")
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