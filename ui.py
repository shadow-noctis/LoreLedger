import sys

def confirm_exit():
    while True:
        confirm = input("Are you sure you wish to exit LoreLedger? (y/n) ")
        if confirm == "y" or confirm == "yes":
            print("Exiting LoreLedger...\nGoodbye!")
            sys.exit()
        elif confirm == "n" or confirm == "no":
            print("Exit cancelled...")
            return
        else:
            print("Please enter 'yes' or 'no'.")

def if_restart(message, yes_priority=False, no_priority=False):
    yes_set = {"yes", "y"}
    no_set = {"no", "n"}
    while True:
        response = input(message).lower().strip()
        print(response)
        if response == "exit":
            confirm_exit()
        elif response in yes_set:
            return True
        elif response in no_set:
            return False
        elif response == "":
            if yes_priority:
                return True
            elif no_priority:
                return False
        print("Unknown command. Please enter 'y' or 'n'")