import sys

def confirm_exit():
    while True:
        confirm = input("Are you sure you wish to exit LoreLedger? (y/n)")
        if confirm == "y" or confirm == "yes":
            print("Exiting LoreLedger...\nGoodbye!")
            sys.exit()
        elif confirm == "n" or confirm == "no":
            print("Exit cancelled...")
            return
        else:
            print("Please enter 'yes' or 'no'.")