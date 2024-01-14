from address_book import AddressBook
from record import Notes, Record, Name, Phone, Email, Birthday, Address, Tag
from thefuzz import fuzz
import inter


def clossest_match(querry: str, commands):
    """filters commands if they start with querry,
    if no command found querry is shortened by one char from the end
    and function tries again (recursively)"""
    if len(querry) == 0:
        return []
    matched_commands = list(filter(lambda x: x.startswith(querry), commands))
    if len(matched_commands) > 0:
        return matched_commands
    else:
        return clossest_match(querry[:-1], commands)


def command_hint(user_str: str, commands, threshold: int = 0) -> str:
    """return string with hint for user describig
    closest match to the available bot commands"""
    user_str = user_str.strip()
    hint = ""
    # for short string use startwith
    if len(user_str) <= 3:
        hits = clossest_match(user_str, commands)
    else:  # for longer strings use fuzzy string matching
        # calculate similarity scores for each command
        # ratio
        # scores = [fuzz.ratio(user_str, command) for command in commands]
        # partial
        # print(commands)
        scores = [fuzz.partial_ratio(user_str, command)
                  for command in commands]

        # threshold = 0
        scores = list(filter(lambda x: x >= threshold, scores))
        # print(scores)
        # find best score
        best_score = max(scores)
        # print(best_score)
        # find all commands with best scores
        hits = [
            command for score, command in zip(scores, commands) if score == best_score
        ]
        # print(hits)

    if len(hits) > 0:
        hint = f"Did you mean?: {', '.join(hits)}"
    return hint

################## HELP ######################


def help(object):
    print(
        """Choose one of the commands:
    - hello - let's say hello,
    - find - to find a contact by name,
    - search - to find a contact after entering keyword (except tag and notes),
    - search notes - to find a contact name after entering keyword by searching by tag or notes,
    - show all - to show all of your contacts from address book,
    - show - to display N contacts from Address Book,
    - show notes - to display contact name with tag and notes,
    - add - to add new contact to Address Book,
    - birthday - to display days to birthday of the user,
    - upcoming birthdays - to check upcoming birthdays from your conatct in Address Book
    - edit phone - to change phone of the user,
    - edit email - to change email of the user,
    - edit birthday - to change birthday of the user,
    - edit address - to change address of the user,
    - edit tag - to change tag of the user,
    - edit notes - to change notes of the user,      
    - delete - to remove contact from Address Book,
    - good bye, close, exit or . - to say good bye and close the program.
After entering the command, you will be asked for additional information if needed to complete the command.""")

###################     HELLO   ###########################


def func_hello(object):
    print("How can I help you?")

##################### ADD ##############################


def add_func(obj):
    to_add = True
    print("\nPlease complete the information below. Name is mandatory, but the rest you can skip by clicking Enter.")
    name = Name(input("\nEnter name*: "))
    contact = obj.check_if_object_exists(name)

    if len(contact) > 0:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        inter.display_contacts(inter.ViewContact(), contact)
        choice = input("\nWould you like to update the contact? (Y/N): ")
        if choice.lower() in ["y", "yes", "true"]:
            to_add = False
            while True:
                att = input("\nPlease choose which information would you like to change? "
                            "\nName, Phone, Email, Birthday, Address, Tag, or Notes: ").lower().strip()

                if att in ["name", "phone", "email", "birthday", "address", "tag", "notes"]:
                    new_value = input(
                        f"Input new {att} of the contact (press Enter to keep current): ").strip()

                    if new_value:
                        object.edit(contact, att, new_value)
                    else:
                        print(f"Keeping current {att}.")

                    another_change = input(
                        "\nDo you want to make another change? (Y/N): ")
                    if another_change.lower() not in ["y", "yes", "true"]:
                        object.save_to_file()
                        print("Contact editing complete.")
                        break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
        else:
            print("Contact not confirmed for editing.")

    phone = Phone(input("Enter new phone: "))
    email = Email(input("Enter new email: "))
    birthday = Birthday(input("Enter new birthday: "))
    address = Address(input("Enter new address: "))
    tag = Tag(input("Enter new tag: "))
    notes = Notes(input("Enter new notes: "))

    if obj.check_entered_values(name, phone, email, birthday, address, tag, notes):
        if to_add:
            new_contact = obj.add(name, phone, email,
                                  birthday, address, tag, notes)
            obj.save_to_file()
            inter.display_contacts(inter.ViewContact(), new_contact)
            print("Contact added successfully.")
        raise ValueError(
            "You did not enter any data to change the contact information. Please try again.")

####################### SHOW ###########################


def show_all_func(object):
    result = object.show()
    inter.display_contacts(inter.ViewContacts(), result)

###################### SHOW ALL NOTES ####################


def show_notes(object):
    result = object.func_show_notes()
    inter.display_contacts(inter.ViewNotes(), result)

######################### EDIT ##########################


def edit_func(object):
    name = Name(input("\nEnter name of contact you would like to edit: "))
    contact = object.check_if_object_exists(name)
    if contact:
        print("\nI've found in the Address Book the contact you want to edit:")
        inter.display_contacts(inter.ViewContact(), contact)
        choice = input(
            "\nPlease confirm if this is the contact you want to edit? (Y/N): ")

        if choice.lower() in ["y", "yes", "true"]:
            while True:
                att = input("\nPlease choose which information would you like to change? "
                            "\nName, Phone, Email, Birthday, Address, Tag, or Notes: ").lower().strip()

                if att in ["name", "phone", "email", "birthday", "address", "tag", "notes"]:
                    new_value = input(
                        f"Input new {att} of the contact (press Enter to keep current): ").strip()

                    if new_value:
                        object.edit(contact, att, new_value)
                    else:
                        print(f"Keeping current {att}.")

                    another_change = input(
                        "\nDo you want to make another change? (Y/N): ")
                    if another_change.lower() not in ["y", "yes", "true"]:
                        object.save_to_file()
                        print("Contact editing complete.")
                        break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
        else:
            print("Contact not confirmed for editing.")
    else:
        print(f"Contact with name '{name.value}' not found.")

################# DELETE ################################


def delete_func(object):
    name = Name(input("\nPlease enter name of the contact: "))
    contact = object.check_if_object_exists(name)
    if len(contact) > 0:
        print("\nI've found in the Address Book this contact.")
        inter.display_contacts(inter.ViewContact(), contact)
        info_delete = input(
            "\nWhat would you like to delete?\n Contact, Name, Phone, Email, Birthday, Address, Tag, or Notes: ")
        if info_delete.lower().strip() == "contact":
            choice_1 = input(
                "\nAre you sure you want to delete hole contact form Addres Book? (Y/N): ")
            if choice_1.lower().strip() in ["y", "yes", "true"]:
                for contact_id in contact.keys():
                    object.delete(contact_id)
                    object.save_to_file()
                print("\nContact deleted successfully.")
            else:
                print("\n No contact was delete from this Address Book.")
        elif info_delete.lower().strip() in ["phone", "email", "birthday", "address", "tag", "notes"]:
            while True:
                choice_2 = input(
                    f"You would like to delete {info_delete} of the {name.value} (Y/N): ")
                if choice_2.lower().strip() in ["y", "yes", "true"]:
                    object.delete_info(contact, info_delete)
                else:
                    print(f"{info_delete} was not deleted.")
                another_change = input(
                    "\nDo you want to make another change? (Y/N): ")
                if another_change.lower().strip() not in ["y", "yes", "true"]:
                    object.save_to_file()
                    print("Delete complete.")
                    break
                else:
                    print("\nInvalid choice. Please choose a valid attribute.")
                    continue
    else:
        print(f"Contact not found.")


def func_exit(object):
    print(
        """
                                           ..::::------:::..                                           
                                 .:-=+*#%@@@@@@@@@@@@@@@@@@@@%##*+=:.                                  
                            :-+#%@@@@@@@@@@@@%%##******##%%@@@@@@@@@@@#*=:                             
                        :+#@@@@@@@%#*+=-:..                 ..:-=+*%@@@@@@@#+-.                        
                    .=*@@@@@@#+=:                                    :-+#@@@@@@#=.                     
                  -#@@@@@#=:    .-=*:        -.         =         =+-:    :=*%@@@@#=.                  
               :*@@@@%+-    :=*%@@@=         +%:      .*@:        .#@@@#+-.   :=#@@@@#-                
             -#@@@%+:   :+#@@@@@@@+          #@@#*****@@@-         .%@@@@@@#+:   .=%@@@%=              
           :#@@@#-   :+%@@@@@@@@@#           %@@@@@@@@@@@=          -@@@@@@@@@%+:   :*@@@%=            
         .*@@@#-   -#@@@@@@@@@@@@:           @@@@@@@@@@@@*           #@@@@@@@@@@@#-   :*@@@#:          
        :%@@%-   -%@@@@@@@@@@@@@%           .@@@@@@@@@@@@#           =@@@@@@@@@@@@@%-   :#@@@=         
       =@@@*.  .#@@@@@@@@@@@@@@@#           -@@@@@@@@@@@@@           -@@@@@@@@@@@@@@@#.   +@@@*        
      =@@@=   -@@@@@@@@@@@@@@@@@%           =@@@@@@@@@@@@@:          +@@@@@@@@@@@@@@@@@-   -%@@*       
     =@@@=   +@@@@@@@@@@@@@@@@@@@-          %@@@@@@@@@@@@@=          %@@@@@@@@@@@@@@@@@@+   :%@@*      
    :@@@=   =@@@@@@@@@@@@@@@@@@@@%.        =@@@@@@@@@@@@@@@:        *@@@@@@@@@@@@@@@@@@@@=   :@@@-     
    #@@#   :@@@@@@@@@@@@@@@@@@@@@@%-      +@@@@@@@@@@@@@@@@%-     :#@@@@@@@@@@@@@@@@@@@@@@:   +@@%     
   .@@@:   *@@@@@@@@@@@@@@@@@@@@@@@@%*==*%@@@@@@@@@@@@@@@@@@@%*+*#@@@@@@@@@@@@@@@@@@@@@@@@*   .@@@=    
   =@@%    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    *@@*    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   +@@#   .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    Good bye!    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.   +@@%    
   =@@@    %@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%    *@@*    
   .@@@-   =@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=   .@@@=    
    *@@#    #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#    +@@%     
    .@@@+    *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#.   :@@@-     
     -@@@=    -%@@@@@@@@@@=.   :=#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%+-:.:=%@@@@@@@@@@#.   :%@@+      
      =@@@=    .*@@@@@@@@-        :#@@@@@*==*%@@@@@@@@@@@%*++%@@@@@*:       .%@@@@@@@@=    -@@@*       
       =@@@*.    :*@@@@@@.          =@@%:     =@@@@@@@@%-     +@@%-          +@@@@@@*.    +@@@+        
        :%@@%=     :*@@@@=           :%:       .%@@@@@#.       *%.           #@@@@*:    -%@@@=         
         .+@@@%-     .+%@%.                     .%@@@#         ..           :@@%+.    :#@@@#.          
           :#@@@%=.     :+*.                     :@@@:                     .#+-     -#@@@%-            
             :#@@@@*:                             +@+                      .     :+%@@@%=              
               :+@@@@%+-                          .%.                         :+%@@@@*-                
                  -*@@@@@#=:                       :                      :=*@@@@@#=.                  
                    .-*%@@@@@#*=:.                                   :-+#@@@@@@*=.                     
                        :=*%@@@@@@@#*+=-::.                ..:-=+*#%@@@@@@@#+:                         
                            .-+*%@@@@@@@@@@@@%%%#######%%%@@@@@@@@@@@%#+-:                             
                                  :-=+*#%%@@@@@@@@@@@@@@@@@@%%#*+=-:.                                  
                                           ...::------:::.                      
"""
    )
    exit()


def main():
    print(
        """
       db        88    ad88                                88  
      d88b       88   d8\"                                  88  
     d8\'`8b      88   88                                   88  
    d8\'  `8b     88 MM88MMM 8b,dPPYba,  ,adPPYba,  ,adPPYb,88  
   d8YaaaaY8b    88   88    88P\'   \"Y8 a8P_____88 a8\"    `Y88  
  d8\"\"\"\"\"\"\"\"8b   88   88    88         8PP\"\"\"\"\"\"\" 8b       88  
 d8\'        `8b  88   88    88         \"8b,   ,aa \"8a,   ,d88  
d8\'          `8b 88   88    88          `\"Ybbd8\"\'  `\"8bbdP\"Y8 

Hello! I am your virtual assistant.
What would you like to do with your Address Book? \nIf you need instructions write 'help'. """
    )
    user_addr_book = AddressBook()
    user_addr_book.read_from_file()
    OPERATIONS_MAP = {
        "hello": func_hello,
        "help": help,
        "find": user_addr_book.func_find,
        "search": user_addr_book.func_search,
        "search notes": user_addr_book.func_search_notes,
        "show all": show_all_func,
        "show": user_addr_book.func_show,
        "show notes": show_notes,
        "add": add_func,
        "birthday": user_addr_book.func_birthday,
        "upcoming birthdays": user_addr_book.func_upcoming_birthdays,
        "edit": edit_func,
        "delete": delete_func,
        "good bye": func_exit,
        "close": func_exit,
        "exit": func_exit,
        ".": func_exit,
    }
    while True:
        listen_enterred = input("\nEnter your command here: ")
        listen = listen_enterred.lower().strip()
        if listen in OPERATIONS_MAP:
            OPERATIONS_MAP[listen](user_addr_book)
        else:
            hint_for_user = command_hint(listen, OPERATIONS_MAP.keys())
            if hint_for_user:
                print(hint_for_user)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
