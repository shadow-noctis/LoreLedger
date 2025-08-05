import load

#Simple dictionary. Reads all words previously saved. If tag included, will only read words with the specific tag, "eg. Story name".
#If add passed as argument, reads all words and then asks for the new word and description to add.
def dictionary(add=False, tag=None):
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
        new_word = input("Word: ")
        description = input("Description: ")
        tags = input("Tags (optional): ").lower().strip()
        tags = tags.split()
        if tags == []:
            tags = None
        word_dict[new_word] = {
            "Description": description,
            "Tags": tags
            }

        #Save the new word to dictionary
        load.save_characters(word_dict, file="dictionary.json")
        print("Word added to dictionary")