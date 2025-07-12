import read_character
import write_character
import delete_character

def main():
    print(" === Welcome to LoreLedger! ===\n")
    print("Type 'options' to see all available commands.\n")

    while True:
        print()
        print("=== LoreLedger Main Menu ===\n")

        command = input("What would you like to do: ").lower().strip()
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
                read_character.list_all()
            case "read":
                read_character.read()
            case "search":
                print("Search not yet available.")
            case "add":
                write_character.new_character()
            case "edit":
                write_character.edit_character()
            case "delete":
                delete_character.delete()
            case "backup":
                delete_character.restore_backup()
            case "restore":
                print("Not yet available")
            case "exit":
                print("Exiting LoreLedger...\nGoodbye!")
                return
            case _:
                print("Unknown command. Type 'options' to see all available commands.")

main()