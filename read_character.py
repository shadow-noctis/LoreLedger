import load
import matching
import ui
import write_character

def list_all():
    characters = load.load_characters()
    print()
    for key in characters:
        print(key)
    print()
    print("  === Further options: === ")
    print("read    -  View character info")
    print("delete  -  Delete character")
    print("back    -  Return to Main Menu")
    print("exit    -  Exit LoreLedger")
    while True:
        next = input("What would you like to do next: ").lower()
        match next:
            case "read":
                read()
            case "delete":
                write_character.delete_character()
            case "options":
                print("  === Options: === ")
                print("read    -  View character info")
                print("delete  -  Delete character")
                print("back    -  Return to Main Menu")
                print("exit    -  Exit LoreLedger")
            case "back":
                return
            case "exit":
                ui.confirm_exit()
            case _:
                print("Unknown command. Type 'options' to review the list of possible commands")

def read():
    #Load characters:
    characters = load.load_characters()

    while True:
        name = input("Which character would you like to view? ")
        if name == 'list':
            list_all()
            return
        elif name == "back" or name == "exit":
            return
        print()

        #Error handling:
        if name not in characters:
            matches = matching.partial_matches(characters, name)
            if len(matches) == 0:
                print("Error: Character not found.")
                print("List all characters by typing 'list'")
                name = None
                continue
            elif len(matches) == 1:
                name = matches[0]
            else:
                print("Exact match not found. Did you mean: ")
                print()
                for match in matches:
                    print(f"- {match}")
                print()
                name = None
                continue

        #Print all values
        print(name)
        for key in characters[name]:
            print(f"{key}: {characters[name][key]}")
        print()
        name = None
        print("Exit reader by typing: 'back'")