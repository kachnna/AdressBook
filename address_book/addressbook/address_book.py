from collections import UserDict
from dataclasses import dataclass
from datetime import datetime, timedelta
import pickle
from abc import abstractmethod, ABC
from pathlib import Path
from data import TestData
from record import Notes, Record, Name, Phone, Email, Birthday, Address, Tag
import textwrap


class Contact_not_found(Exception):
    pass


class MyContactsIterator:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.keys = list(dictionary.keys())
        self.index = 0

    def __next__(self):
        if self.index < len(self.keys):
            key = self.keys[self.index]
            value = self.dictionary[key]
            self.index += 1
            yield key, value
        raise StopIteration


@dataclass
class AddressBook(UserDict):
    def __init__(self):
        self.counter: int
        self.filename = "contacts.bin"
        self.path = Path("./" + self.filename)

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.contacts, file)

    def read_from_file(self):
        if self.path.is_file() == False:
            test_data = TestData()
            self.contacts = test_data.test_contacts

        else:
            with open(self.filename, "rb") as file:
                self.contacts = pickle.load(file)
        return self.contacts

    def __iter__(self):
        return MyContactsIterator(self.contacts)

    def input_error(func):
        def wrapper(*args):
            try:
                return func(*args)
            except KeyError as e:
                print(
                    f"Username not provided or user not found. Try again.\nError details: {str(e)}\n"
                )
            except IndexError as e:
                print(
                    f"Incorrect data has been entered. Try again.\nError details: {str(e)}\n"
                )
            except ValueError as e:
                print(
                    f"I'm sorry, but I don't understand your request. Try again.\nError details: {str(e)}\n"
                )
            except Contact_not_found as e:
                print(f"Contact not found.")
            # except Exception as e:
            #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

        return wrapper

    @input_error
    def check_entered_values(self, name=None, phone=None, email=None, birthday=None, address=None, tag=None, notes=None):
        if name.value is None and phone.value is None and email.value is None and birthday.value is None and address.value is None and tag.value is None and notes.value is None:
            return False
        else:
            return True

    @input_error
    def check_if_object_exists(self, name):
        if name is None:
            pass
        results = {}
        contact_name = name if isinstance(name, str) else name.value
        for key, obj in self.contacts.items():
            if isinstance(obj.name, str):
                value = obj.name
            else:
                value = obj.name.value if hasattr(
                    obj.name, 'value') else obj.name
            if contact_name.lower() in value.lower():
                results[key] = obj
        return results

    @input_error
    def check_latest_id(self):
        list_of_id = []
        for key_id in self.contacts.keys():
            list_of_id.append(key_id)
        max_ID = max(list_of_id)
        return max_ID

    @input_error
    def func_find(self, name):
        if name in self.contacts:
            print("{:^60}".format("-" * 60))
            print("{:^20}|{:^40}".format("Name", name))
            print(
                "{:^20}|{:^40}".format(
                    "Phone", self.check_value(self.contacts[name][0])
                )
            )
            print(
                "{:^20}|{:^40}".format(
                    "Email", self.check_value(self.contacts[name][1])
                )
            )
            print(
                "{:^20}|{:^40}".format(
                    "Birthday", self.check_value(self.contacts[name][2])
                )
            )
            print(
                "{:^20}|{:^40}".format(
                    "Address", self.check_value(self.contacts[name][3])
                )
            )
            print(
                "{:^20}|{:^40}".format(
                    "Tag", self.check_value(self.contacts[name][4]))
            )
            print("{:^60}".format("-" * 60))
            # print(f"Notes: {self.check_value(self.contacts[name][5]):{60}}")
            print(
                "\n".join(
                    textwrap.wrap(
                        f"Notes: {self.check_value(self.contacts[name][5])}", width=60
                    )
                )
            )
            print("{:^60}".format("-" * 60))
        else:
            raise Contact_not_found

    @input_error
    def func_search(self, keyword):
        print("{:^150}".format("-" * 150))
        print(
            "{:^30}|{:^20}|{:^30}|{:^20}|{:^50}".format(
                "Name", "Phone", "Email", "Birthday", "Address"
            )
        )
        print("{:^150}".format("-" * 150))
        contact_counter = 0
        contacts_sorted = dict(
            sorted(self.contacts.items(), key=lambda x: x[0]))
        for key, value in contacts_sorted.items():
            if (
                keyword.lower() in key.lower()
                or keyword in value[0]
                or keyword in value[0].replace(" ", "")
                or keyword.lower() in value[1].lower()
                or keyword in value[2]
                or keyword.lower() in value[3].lower()
            ):
                print(
                    "{:^30}|{:^20}|{:^30}|{:^20}|{:^50}".format(
                        key,
                        self.check_value(value[0]),
                        self.check_value(value[1]),
                        self.check_value(value[2]),
                        self.check_value(value[3]),
                    )
                )
                contact_counter += 1
        if contact_counter == 0:
            raise Contact_not_found

    @input_error
    def func_search_notes(self, keyword):
        print("{:^70}".format("-" * 70))
        # print("{:^20}|{:^40}|{:^50}".format("Name", "Tag", "Notes"))
        print("{:^20}|{:^40}".format("Name", "Tag"))
        print("{:^70}".format("-" * 70))
        contact_counter = 0
        contacts_sorted = dict(
            sorted(self.contacts.items(), key=lambda x: x[0]))
        for key, value in contacts_sorted.items():
            if (
                keyword.lower() in value[4].lower()
                or keyword.lower() in value[5].lower()
            ):
                print("{:^20}|{:^40}".format(key, self.check_value(value[4])))
                print("{:^70}".format("-" * 70))
                print(
                    "\n".join(
                        textwrap.wrap(
                            f"Notes: {self.check_value(value[5])}",
                            width=70,
                        )
                    )
                )

                print("{:^70}".format("=" * 70))

                contact_counter += 1
        if contact_counter == 0:
            raise Contact_not_found
# SHOW ALL #

    @input_error
    def show(self):
        return self.contacts

    @input_error
    def func_show_notes(self):
        if not self.contacts:
            print("Address book is empty.")
        else:
            return self.contacts

    @input_error
    def func_upcoming_birthdays(self, days_str):
        def month_sort_key(date_str):
            date = datetime.strptime(date_str, "%d %B (%A)")
            current_month = datetime.now().month
            return (date.month - current_month) % 12

        today = datetime.now()
        formatted_date = today.strftime("%d %B %Y")
        days = int(days_str)
        last_day = today + timedelta(days=days)
        formatted_last_day = last_day.strftime("%d %B %Y")
        print(
            f"\nChecking period ({formatted_date} - {formatted_last_day}).\n")

        birthdays_list = {}
        today_birthday = {}

        for name, user_info in self.contacts.items():
            birthday_str = user_info[2]
            phone = user_info[0]
            email = user_info[1]
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()

            birthday_this_year = birthday.replace(year=today.year)
            birthday_next_year = birthday.replace(year=today.year + 1)

            if today.date() < birthday_this_year <= last_day.date():
                day_of_week = birthday_this_year.strftime("%d %B (%A)")
                if day_of_week not in birthdays_list:
                    birthdays_list[day_of_week] = []
                birthdays_list[day_of_week].append((name, phone, email))
            elif today.date() < birthday_next_year <= last_day.date():
                day_of_week = birthday_next_year.strftime("%d %B (%A)")
                if day_of_week not in birthdays_list:
                    birthdays_list[day_of_week] = []
                birthdays_list[day_of_week].append((name, phone, email))
            elif today.date() == birthday_this_year:
                day_of_week = birthday_this_year.strftime("%d %B (%A)")
                if day_of_week not in today_birthday:
                    today_birthday[day_of_week] = []
                today_birthday[day_of_week].append((name, phone, email))

        if not any(birthdays_list.values()) and not any(today_birthday.values()):
            print(f"\nNone of your contacts have upcoming birthdays in this period.")
        else:
            print(
                "   O O O O \n" "  _|_|_|_|_\n" " |         |\n",
                "|         |\n",
                "|_________|\n",
            )
        if any(today_birthday.values()):
            print('Someone has birthday today, so wish "HAPPY BIRTHDAY" today to:')
            print("{:^90}".format("*" * 90))
            print("{:^30}|{:^30}|{:^30}".format("Name", "Phone", "Email"))
            print("{:^90}".format("*" * 90))
            for day, users in sorted(today_birthday.items(), key=lambda x: x[0]):
                for user_info in users:
                    print("{:^30}|{:^30}|{:^30}".format(*user_info))
                    print("*" * 90)
        if any(birthdays_list.values()):
            print("\nSend birthday wishes to your contact on the upcoming days:")
            print("{:^120}".format("-" * 120))
            print(
                "{:^30}|{:^30}|{:^30}|{:^30}".format(
                    "Birthday", "Name", "Phone", "Email"
                )
            )
            print("{:^120}".format("-" * 120))
            for day, users in sorted(
                birthdays_list.items(), key=lambda x: month_sort_key(x[0])
            ):
                for user_info in users:
                    print("{:^30}|{:^30}|{:^30}|{:^30}".format(day, *user_info))
                    print("-" * 120)

    @input_error
    def func_show(self, number_of_contacts):
        contacts_sorted = dict(
            sorted(self.contacts.items(), key=lambda x: x[0]))
        iterator = iter(contacts_sorted.items())
        len_of_dictionary = len(list(contacts_sorted.keys()))
        self.counter = 0
        while True:
            self.counter += 1
            print("\n{:^150}".format("-" * 150))
            print(f"Page {self.counter}")
            print("{:^150}".format("-" * 150))
            print(
                "{:^30}|{:^20}|{:^30}|{:^20}|{:^50}".format(
                    "Name", "Phone", "Email", "Birthday", "Address"
                )
            )
            print("{:^150}".format("-" * 150))
            for _ in range(number_of_contacts):
                try:
                    name, contact = next(iterator)
                    print(
                        "{:^30}|{:^20}|{:^30}|{:^20}|{:^40}".format(
                            name,
                            self.check_value(contact[0]),
                            self.check_value(contact[1]),
                            self.check_value(contact[2]),
                            self.check_value(contact[3]),
                        )
                    )
                except StopIteration:
                    break
            print("{:^140}".format("-" * 140))
            if self.counter * number_of_contacts < len_of_dictionary:
                choice = input(
                    f"Do you want to display next {number_of_contacts} contact(s)? (Y/N) "
                )
                if choice not in ["y", "Y", "Yes", "yes", "True"]:
                    break
            else:
                break

# add
    @input_error
    def add(self, name, phone, email, birthday, address, tag, notes):
        id = int(self.check_latest_id() + 1)
        new_contact = Record(name.value, phone.value, email.value,
                             birthday.value, address.value, tag.value, notes.value)
        self.contacts[id] = new_contact
        return dict(filter(lambda item: item[0] == id, self.contacts.items()))

# edit
    @input_error
    def edit(self, contact, att, new_info):
        for id, obj in contact.items():
            if att == "name":
                obj.edit_name(new_info)
            elif att == "phone":
                obj.edit_phone(new_info)
            elif att == "email":
                obj.edit_email(new_info)
            elif att == "birthday":
                obj.edit_birthday(new_info)
            elif att == "address":
                obj.edit_address(new_info)
            elif att == "tag":
                obj.edit_tag(new_info)
            elif att == "notes":
                obj.edit_notes(new_info)
            else:
                return f"Unable to edit."

    @input_error
    def func_birthday(self, name):
        if name in self.contacts:
            contact = Record(
                name,
                self.contacts[name][0],
                self.contacts[name][1],
                self.contacts[name][2],
                self.contacts[name][3],
                self.contacts[name][4],
                self.contacts[name][5],
            )
            contact.days_to_birthday(contact.name, contact.birthday)
        else:
            raise Contact_not_found

# delete

    @input_error
    def delete(self, key):
        self.contacts.pop(key)

# delete contact information
    @input_error
    def delete_info(self, contact, info_delete):
        for id, obj in contact.items():
            if info_delete == "phone":
                obj.delete_phone()
            elif info_delete == "email":
                obj.delete_email()
            elif info_delete == "birthday":
                obj.delete_birthday()
            elif info_delete == "address":
                obj.delete_address()
            elif info_delete == "tag":
                obj.delete_tag()
            elif info_delete == "notes":
                obj.delete_notes()
            else:
                return f"Unable to delete."
