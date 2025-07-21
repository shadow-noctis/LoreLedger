import load

def search(search_term=None):
    while True:
        print("Please note: Currently capitalization of search term matters when searching.")
        found = False
        characters = load.load_characters()
        if search_term == None:
            search_term = input("Search term: ")
        search_term.lower().strip()
        for character in characters:
            for field in characters[character]:
                current_search = characters[character][field]
                if type(current_search) is list:
                    if search_term in current_search:
                        print(f"\n == {character} ==\n{field}: {current_search}")
                        found = True
                elif search_term == current_search:
                    print(f" == {character} ==\n{field}: {current_search}")
                    found = True
        if found == False:
            print("No matches found.\nPlease try again")
            search_term = None
            continue
        else:
            return

    