import read_character
import write_character
import delete_character
import search
import dictionary

def main():
    print(" === Welcome to LoreLedger! ===\n")
    print("Type 'options' to see all available commands.\n")

    while True:
        print()
        print("=== LoreLedger Main Menu ===\n")

        #Ask for command. Split the reponse in case name/argument passed on:
        response = input("What would you like to do: ").strip()
        parts = response.split(maxsplit=1)
        command = parts[0].lower()
        if len(parts) > 1:
            argument = parts[1]
        else:
            argument = None
        #match command to use right function
        match command:
            case "options":
                print("\n=== LoreLedger Menu ===\n")
                print("Type one of the following commands:")
                print("   options - Show commands menu")
                print("   list    - List all characters")
                print("   read    - View a specific character info")
                print("   search  - Search by story/name (Not yet available)")
                print("   add     - Add a new character")
                print("   edit    - Edit a character")
                print("   delete  - Delete all character files or specific. Delete can also be used to delete your backups.")
                print("   backup  - Restores previous state before delete all (This will overwrite your current characters stored in LoreLedger)")
                print("   restore - Restores deleted characters currently not in your LoreLedger")
                print("   back    - Return back to the main menu")
                print("   exit    - Exit the program")
                print()
            case "list":
                if argument == None:
                    read_character.list_all()
                else:
                    read_character.list_all(title=argument)
            case "read":
                if argument == None:
                    name = input("Which character would you like to view: ")
                    read_character.read(name)
                else:
                    read_character.read(argument)
            case "search":
                if argument == None:
                    search.search()
                else:
                    search.search(search_term=argument)
            case "add":
                write_character.new_character()
            case "edit":
                if argument == None:
                    name = input("Which character would you like to edit? ")
                    write_character.edit_character(name)
                else:
                    write_character.edit_character(argument)
            case "delete":
                if argument == None:
                    delete_character.delete()
                elif argument == "all":
                    delete_character.delete_all()
                elif argument == "rule":
                    delete_character.delete_by_rule()
                else:
                    delete_character.delete_character(argument)
            case "backup":
                delete_character.restore_backup()
            case "restore":
                delete_character.restore_deleted_characters()
            case "dictionary":
                if argument != None:
                    arguments = argument.split()
                    add = False
                    tag = None
                    edit = False
                    delete = False
                    for argument in arguments:
                        if argument.lower() == "add":
                            add = True
                        elif argument.lower() == "delete":
                            delete = True
                        elif argument.lower() == "edit":
                            print("Hello")
                            edit = True
                        elif argument.lower().startswith("tag="):
                            tag = argument.split("=", 1)[1].strip()
                    dictionary.dictionary(add, tag, delete, edit)
                else:
                    dictionary.dictionary()
            case "exit":
                print("Exiting LoreLedger...\nGoodbye!")
                return
            case _:
                print("Unknown command. Type 'options' to see all available commands.")

main()