import load

def list_all():
    characters = load.load_characters()
    for key in characters:
        print(key)
    read_further = input("You can type in the name of a character to view the character sheet: ")

list_all()