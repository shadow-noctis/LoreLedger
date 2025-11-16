import load
import matching
import read_character
from difflib import get_close_matches

def search(search_term=None):
    characters = load.load_characters()
    if search_term == None:
        search_term = input("Search term: ")
    character_names = matching.list_characters(characters)
    matches = get_close_matches(search_term, character_names, n=5, cutoff=0.4)
    if len(matches) == 1:
        read_character.read(name=matches[0])
    elif len(matches) > 1:
        for name in matches:
            print(f" - {name}")
    else:
        matched_items = search_item(characters, search_term)
        if len(matched_items) == 0:
            print("No matches found. Please check for typos")
        elif len(matched_items) == 1:
            read_character.read(name=matched_items[0])
        else:
            for i in range(len(matched_items)):
                print(f" - {matched_items[i]}")
    
        


def search_item(characters, search_term):
    results = []
    for name in characters:
        values = characters[name].values()
        for value in values:
            if isinstance(value, list):
                if search_term in value:
                    results.append(name)
                    break
            elif search_term.lower() in value.lower():
                results.append(name)
                break
    return results

    