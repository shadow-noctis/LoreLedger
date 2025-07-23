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


#Check for partial matches. If surname provided, return only characters with the same surname
def partial_matches(characters, given_name, surname=None):
    if surname != None:
        matching = characters_by_surname(characters, surname)
    else:
        matching = list_characters(characters)
    return get_close_matches(given_name, matching, cutoff=0.5)

def print_numbered_list(to_number):
    i = 1
    for item in to_number:
        print(f"{i}. {item}")
        i += 1

def token_match(query, full_name):
    query_tokens = query.lower().split()
    name = full_name.lower()
    for q in query_tokens:
        if q not in name:
            return False
    return True