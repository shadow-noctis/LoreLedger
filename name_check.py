def if_name_exists(characters, name):
    matches = []
    
    for key in characters:
        if name.lower() in key.lower():
            matches.append(key)

    return matches