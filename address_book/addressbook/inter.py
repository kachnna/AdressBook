from abc import abstractmethod, ABC
from record import Notes, Record, Name, Phone, Email, Birthday, Address, Tag
from dataclasses import dataclass


class ContactNotFound(Exception):
    pass


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ContactNotFound as e:
            print("\nSorry, but I couldn't find any contacts in the Address book.")
    return wrapper


def check_value(value):
    if value is None:
        return ""
    return value


class AbstractView(ABC):
    @abstractmethod
    def display(self, data):
        pass


class ViewContacts(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<40}|"
            separator = ("{:<163}".format("-" * 143))
            print(separator)
            print(pattern.format("Id", "Name", "Phone",
                  "Email", "Birthday", "Address"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
                ))
            print(separator)
        else:
            raise ContactNotFound


class ViewNotes(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "|{:<20}|{:<20}|{:<136}"
            separator = ("{:^176}".format("-" * 176))
            print(separator)
            print(pattern.format("Name", "Tag", "Notes"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern.format(
                    check_value(obj.name.value),
                    check_value(obj.tag.value),
                    check_value(obj.notes.value),
                ))
            print(separator)
        else:
            raise ContactNotFound


class ViewContact(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_contacts = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            pattern_tag_notes = "|{:^161}|"
            separator = ("{:^163}".format("-" * 163))
            print(separator)
            print(pattern_contacts.format("Id", "Name",
                  "Phone", "Email", "Birthday", "Address"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern_contacts.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
                ))
                print(separator)
                print("\n{:^163}".format("-" * 163))
                print(pattern_tag_notes.format("Tag"))
                print(separator)
                print(pattern_tag_notes.format(check_value(obj.tag.value)))
                print(separator)
                print(pattern_tag_notes.format("Notes"))
                print(separator)
                print(pattern_tag_notes.format(check_value(obj.notes.value)))
                print(separator)
        else:
            raise ContactNotFound


class ViewContactBirthday(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<17}|"
            separator = ("{:^120}".format("-" * 120))
            print(pattern.format("Id", "Name ^", "Phone",
                  "Email", "Birthday", "Days to Birthday"))
            print(separator)
            for id, obj in sorted(data.items(), key=lambda x: getattr(x[1][0], 'name', x[1][0])):
                print(pattern.format(
                    id,
                    check_value(getattr(obj[0], 'name', obj[0]).value),
                    check_value(getattr(obj[0], 'phone', obj[0]).value),
                    check_value(getattr(obj[0], 'email', obj[0]).value),
                    check_value(getattr(obj[0], 'birthday', obj[0]).value),
                    check_value(obj[1]),
                ))
            print(separator)
        else:
            raise ContactNotFound


def display_contacts(view: AbstractView, data) -> None:
    view.display(data)
