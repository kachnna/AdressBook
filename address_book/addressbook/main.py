<<<<<<< Updated upstream
from addresbook import AddressBook
=======
from address_book import AddressBook
from record import Notes, Record, Name, Phone, Email, Birthday, Address, Tag
>>>>>>> Stashed changes
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

# add


def add_func(obj):
    to_add = True
    print("\nPlease complete the information below. Name is mandatory, but the rest you can skip by clicking Enter.")
    name = Name(input("\nEnter name*: "))
    contacts = obj.check_if_object_exists(name)

    if len(contacts) > 0:
        print("\nI've found in the Address Book the contact(s) with the same name:")
        inter.display_contacts(inter.ViewContact(), contacts)
        choice = input("\nWould you like to update the contact? (Y/N): ")
        if choice.lower() in ["y", "yes", "true"]:
            to_add = False
            if len(contacts) > 1:
                while True:
                    number = int(
                        input("\nPlease enter the ID number of the contact you want to update: "))
                    if number in contacts.keys():
                        break
                    else:
                        print(
                            "\nSorry, but I couldn't find any contacts with this ID. Try again...\n")
                key = number
                value = contacts[number]
            else:
                key = list(contacts.keys())[0]
                value = list(contacts.values())[0]
            print(
                "\nComplete the information below that you want to update or skip by clicking Enter.")

        else:
            print(
                f"\nContinue entering the information for a new contact: {name.value}\n")

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
        else:
            obj_updated = obj.edit(
                value, name, phone, email, birthday, address, tag, notes)
            obj.save_to_file()
            results_to_display = {}
            results_to_display[key] = obj_updated
            inter.display_contacts(inter.ViewContact(), results_to_display)
            print("Contact updated successfully.")
    else:
        raise ValueError(
            "You did not enter any data to change the contact information. Please try again.")

# show all


def show_all_func(object):
    result = object.show()
    inter.display_contacts(inter.ViewContacts(), result)

# delete


def delete_func(object):
    name = Name(input("\nEnter name of contact you would like to delete: "))
    contact = object.check_if_object_exists(name)
    if len(contact) > 0:
        print("\nI've found in the Address Book the contact you want to delete:")
        inter.display_contacts(inter.ViewContact(), contact)
        choice = input(
            "\nPlease confirm if this is the contact you want to delete? (Y/N): ")
        if choice.lower() in ["y", "yes", "true"]:
            for contact_id in contact.keys():
                object.delete(contact_id)
                object.save_to_file()
            print("\nContact deleted successfully.")
        else:
            print("\n No contact was delete from this Address Book.")
    else:
        print(f"Contact with ID {name} not found.")


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
What would you like to do with your Address Book?
Choose one of the commands:
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
After entering the command, you will be asked for additional information if needed to complete the command."""
    )
    user_addr_book = AddressBook()
    user_addr_book.read_from_file()
    OPERATIONS_MAP = {
        "hello": user_addr_book.func_hello,
        "find": user_addr_book.func_find,
        "search": user_addr_book.func_search,
        "search notes": user_addr_book.func_search_notes,
        "show all": show_all_func,
        "show": user_addr_book.func_show,
        "show notes": user_addr_book.func_show_notes,
        "add": add_func,
        "birthday": user_addr_book.func_birthday,
        "upcoming birthdays": user_addr_book.func_upcoming_birthdays,
        "edit phone": user_addr_book.func_edit_phone,
        "edit email": user_addr_book.func_edit_email,
        "edit birthday": user_addr_book.func_edit_birthday,
        "edit address": user_addr_book.func_edit_address,
        "edit tag": user_addr_book.func_edit_tag,
        "edit notes": user_addr_book.func_edit_notes,
        "delete": delete_func,
        "good bye": user_addr_book.func_exit,
        "close": user_addr_book.func_exit,
        "exit": user_addr_book.func_exit,
        ".": user_addr_book.func_exit,
    }
    while True:
        listen_enterred = input("\nEnter your command here: ")
        listen = listen_enterred.lower().strip()
        if listen in OPERATIONS_MAP:
            if listen == "add":
                OPERATIONS_MAP[listen](user_addr_book)
            elif listen == "delete":
                OPERATIONS_MAP[listen](user_addr_book)
            elif listen == "upcoming birthdays":
                keyword = input(
                    "Which time frame from today would you like to check? Please input the number of days from now: "
                ).strip()
                OPERATIONS_MAP[listen](keyword)
            elif listen in ["search", "search notes"]:
                keyword = input("Enter keyword: ").strip()
                OPERATIONS_MAP[listen](keyword)
            elif listen == "edit phone":
                name = input(
                    "Enter name of the contact to edit phone: ").strip()
                new_phone = input("Enter new phone number: ").strip()
                OPERATIONS_MAP[listen](name, new_phone)
            elif listen == "edit email":
                name = input(
                    "Enter name of the contact to edit email: ").strip()
                new_email = input("Enter new email: ").strip()
                OPERATIONS_MAP[listen](name, new_email)
            elif listen == "edit birthday":
                name = input(
                    "Enter name of the contact to edit birthday: ").strip()
                new_birthday = input("Enter new birthday: ").strip()
                OPERATIONS_MAP[listen](name, new_birthday)
            elif listen == "edit address":
                name = input(
                    "Enter name of the contact to edit address: ").strip()
                new_address = input("Enter new address: ").strip()
                OPERATIONS_MAP[listen](name, new_address)
            elif listen == "edit tag":
                name = input("Enter name of the contact to edit tag: ").strip()
                new_tag = input("Enter new tag: ").strip()
                OPERATIONS_MAP[listen](name, new_tag)
            elif listen == "edit notes":
                name = input("Enter name of the contact to edit tag: ").strip()
                new_notes = input("Enter new notes: ").strip()
                OPERATIONS_MAP[listen](name, new_notes)
            elif listen == "show":
                try:
                    number_of_contacts = int(
                        input("Enter number of contacts to display: ")
                    )
                    OPERATIONS_MAP[listen](number_of_contacts)
                except:
                    print("Entered number is not an integer. Please try again.")
            elif listen in ["good bye", "close", "exit", "."]:
                user_addr_book.save_to_file()
                OPERATIONS_MAP[listen.lower()]()
            else:
                OPERATIONS_MAP[listen.lower()](user_addr_book)
        else:
            hint_for_user = command_hint(listen, OPERATIONS_MAP.keys())
            if hint_for_user:  # not empty string
                print(hint_for_user)
            else:
                print("Invalid command.")


if __name__ == "__main__":
    main()
