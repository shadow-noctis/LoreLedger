from difflib import get_close_matches

def characters_by_surname(characters, surname):
    character_list = []
    for character in characters:
        name = character.split()
        current_surname = name.pop()
        if current_surname == surname:
            name = ' '.join(name)
            character_list.append(name)
    return character_list



def partial_matches(characters, given_name, surname):
    same_surname = characters_by_surname(characters, surname)
    return get_close_matches(given_name, same_surname)