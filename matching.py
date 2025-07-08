from difflib import get_close_matches

# Lists all characters with same surname: Ignores characters with different surname
def characters_by_surname(characters, surname):
    character_list = []
    for character in characters:
        name = character.split()
        current_surname = name.pop()
        if current_surname == surname:
            name = ' '.join(name)
            character_list.append(name)
    return character_list

# List all characters
def list_characters(characters):
    character_list = []
    for character in characters:
        character_list.append(character)
    return character_list



def partial_matches(characters, given_name, surname=None):
    if surname != None:
        matching = characters_by_surname(characters, surname)
    else:
        matching = list_characters(characters)
    return get_close_matches(given_name, matching, cutoff=0.5)