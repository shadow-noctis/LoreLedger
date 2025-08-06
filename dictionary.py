import load

#Simple dictionary. Reads all words previously saved. If tag included, will only read words with the specific tag, "eg. Story name".
#If add passed as argument, reads all words and then asks for the new word and description to add.
def dictionary(add=False, tag=None, delete=False, edit=False):
    word_dict = load.load_characters(file="dictionary.json")
    #Flag to see if anything found:
    tag_found = False
    #No tag, so loop through the dictionary and print each word with description
    if tag == None:
        if word_dict == {}:
            print("No words yet added to dictionary\n")
        else:
            for word in word_dict:
                print(f" - {word}  →  {word_dict[word]["Description"]}")
    #Tag included, so only print matching tags.
    else:
        for word in word_dict:
            if word_dict[word]["Tags"] != None:
                if tag.strip() in word_dict[word]["Tags"]:
                    print(f" - {word}  →  {word_dict[word]["Description"]} (tags: {" ".join(word_dict[word]["Tags"])})")
                    tag_found = True
        if tag_found == False:
            print(f"Nothing tagged {tag}")

    #Add new word if add==True
    if add:
        new_word = input("New word: ")
        if new_word not in word_dict:
            description = input("Description: ")
            tags = input("Tags (optional): ").lower().strip()
            tags = tags.split()
            if tags == []:
                tags = None
            word_dict[new_word.capitalize()] = {
                "Description": description,
                "Tags": tags
                }

            print("Word added to dictionary")
        else:
            print("Word already in dictionary\nUse edit to change the description or delete")
    
    if delete:
        word = input("Delete word: ").capitalize()
        if word in word_dict:
            del word_dict[word]
            print(f"{word} deleted")
        else:
            print("Word not found\nDelete cancelled.")

    if edit:
        word = input("Edit word: ").capitalize()
        if word in word_dict:
            description = input("New description: ")
            word_dict[word]["Description"] = description
            print("Word updated")
        else:
            print("Word not found\nEdit cancelled.")

    load.save_characters(word_dict, file="dictionary.json")