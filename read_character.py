import load
import matching

def list_all():
    characters = load.load_characters()
    print()
    for key in characters:
        print(key)
    print()
    read()

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
                #Later development: add options to 1. Re-enter name 2. list all characters 3. return to menu 4. Exit
            elif len(matches) == 1:
                name = matches[0]
            else:
                print("Exact match not found. Did you mean: ")
                print()
                for match in matches:
                    print(match)
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