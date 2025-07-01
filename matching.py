def partial_matches(characters, full_name):
    matches = []
    
    all_names = full_name.split()
    for name in all_names:
        for key in characters:
            if name.lower() in key.lower():
                if key not in matches:
                    matches.append(key)

    return matches