import load
import matching

def list_all():
    characters = load.load_characters()
    for key in characters:
        print(key)
        
        #Not yet functional, will just exit the program.
    read_further = input("You can type in the name of a character to view the character sheet: ")

def read(name):
    #Load characters:
    characters = load.load_characters()

    #Error handling:
    if name not in characters:
        matches = matching.partial_matches(characters, name)
        if len(matches) == 0:
            print("Character not found. Exiting...")
            #Later development: add options to 1. Re-enter name 2. list all characters 3. return to menu 4. Exit
        elif len(matches) == 1:
            name = matches[0]
        else:
            print("Exact match not found. Did you mean: ")
            print()
            for match in matches:
                print(match)
            print()
            new_name = input("Re-enter name: ")
            print()
            if new_name == "e" or new_name == "exit":
                print("Exiting...")
                return
            else:
                read(new_name)
                return

    #Print all values
    print(name)
    for key in characters[name]:
        print(f"{key}: {characters[name][key]}")
    print()

read("Anami")