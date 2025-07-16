import load
import matching
import ui

def list_all():
    characters = load.load_characters()
    print()
    for key in characters:
        print(key)
    return

def read(name):
    #Load characters:
    characters = load.load_characters()

    while True:
        if name == 'list':
            list_all()
            name = input("Which character would you like to view: ")
            continue
        elif name == "back":
            return
        elif name == "exit":
            ui.confirm_exit()
        print()

        #Error handling:
        if name not in characters:
            matches = matching.partial_matches(characters, name)
            if len(matches) == 0:
                print("Error: Character not found.")
                print("List all characters by typing 'list'")
                name = input("Which character would you like to view: ")
                continue
            elif len(matches) == 1:
                name = matches[0]
            else:
                print("Exact match not found.\nDid you mean: ")
                print()
                for match in matches:
                    print(f"- {match}")
                print()
                name = input("Which character would you like to view: ")
                continue

        #Print all values
        print(f"=== {name} ===")
        for key in characters[name]:
            if type(characters[name][key]) == list:
                print(f"{key}:")
                for item in characters[name][key]:
                    print(f"  - {item}")
            else:
                print(f"{key}: {characters[name][key]}")
        print()
        return