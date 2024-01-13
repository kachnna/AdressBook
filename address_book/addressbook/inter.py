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
    else:
        return value


class AbstractView(ABC):
    @abstractmethod
    def display(self, data):
        pass


class ViewContacts(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            print("\n{:^163}".format("-" * 163))
            print(pattern_headline.format("Id", "Name",
                  "Phone", "Email", "Birthday", "Address"))
            print("{:^163}".format("-" * 163))
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern_body.format(
                    id,
                    check_value(obj.name.value) if isinstance(
                        obj.name, Name) else check_value(obj.name),
                    check_value(obj.phone.value) if hasattr(
                        obj.phone, 'value') else check_value(obj.phone),
                    check_value(obj.email.value) if hasattr(
                        obj.email, 'value') else check_value(obj.email),
                    check_value(obj.birthday.value) if hasattr(
                        obj.birthday, 'value') else check_value(obj.birthday),
                    check_value(obj.address.value) if hasattr(
                        obj.address, 'value') else check_value(obj.address),
                ))
            print("{:^163}".format("-" * 163))
        else:
            raise ContactNotFound


class ViewNotes(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<109}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<109}|"
            print("\n{:^163}".format("-" * 163))
            print(pattern_headline.format("Id", "Name ^", "Tag", "Notes"))
            print("{:^163}".format("-" * 163))
            for id, obj in sorted(data.items(), key=lambda x: getattr(x[1], 'name', x[1])):
                print(pattern_body.format(
                    id,
                    check_value(getattr(obj, 'name', obj).value),
                    check_value(getattr(obj, 'tag', obj).value),
                    check_value(getattr(obj, 'notes', obj).value),
                ))
            print("\n{:^163}".format("-" * 163))
        else:
            raise ContactNotFound


class ViewContact(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            print("\n{:^163}".format("-" * 163))
            print(pattern_headline.format("Id", "Name",
                  "Phone", "Email", "Birthday", "Address"))
            print("{:^163}".format("-" * 163))
            for id, obj in sorted(data.items(), key=lambda x: str(x[1].name) if isinstance(x[1].name, str) else str(x[1].name.value)):
                print(pattern_body.format(
                    id,
                    check_value(obj.name.value) if isinstance(
                        obj.name, Name) else check_value(obj.name),
                    check_value(obj.phone.value) if hasattr(
                        obj.phone, 'value') else check_value(obj.phone),
                    check_value(obj.email.value) if hasattr(
                        obj.email, 'value') else check_value(obj.email),
                    check_value(obj.birthday.value) if hasattr(
                        obj.birthday, 'value') else check_value(obj.birthday),
                    check_value(obj.address.value) if hasattr(
                        obj.address, 'value') else check_value(obj.address),
                ))
            print("{:^163}".format("-" * 163))
            print("\n")
            print("{:^163}".format("-" * 163))
            print("|{:^161}|".format("Tag"))
            print("{:^163}".format("-" * 163))
            print("|{:<161}|".format(check_value(obj.tag.value) if hasattr(
                obj.tag, 'value') else check_value(obj.tag)))
            print("{:^163}".format("-" * 163))
            print("|{:^161}|".format("Notes"))
            print("{:^163}".format("-" * 163))
            print("|{:<161}|".format(check_value(obj.notes.value)if hasattr(
                obj.notes, 'value') else check_value(obj.notes)))
            print("{:^163}".format("-" * 163))
        else:
            raise ContactNotFound


class ViewContactBirthday(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<17}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<17}|"
            print("\n{:^120}".format("-" * 120))
            print(pattern_headline.format("Id", "Name ^", "Phone",
                  "Email", "Birthday", "Days to Birthday"))
            print("{:^120}".format("-" * 120))
            for id, obj in sorted(data.items(), key=lambda x: getattr(x[1][0], 'name', x[1][0])):
                print(pattern_body.format(
                    id,
                    check_value(getattr(obj[0], 'name', obj[0]).value),
                    check_value(getattr(obj[0], 'phone', obj[0]).value),
                    check_value(getattr(obj[0], 'email', obj[0]).value),
                    check_value(getattr(obj[0], 'birthday', obj[0]).value),
                    check_value(obj[1]),
                ))
            print("{:^120}".format("-" * 120))
        else:
            raise ContactNotFound


def display_contacts(view: AbstractView, data) -> None:
    view.display(data)
