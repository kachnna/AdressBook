from abc import abstractmethod, ABC


class ContactNotFound(Exception):
    pass


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ContactNotFound as e:
            print("\nSorry, but I couldn't find any contacts in the Address book.")
        # except Exception as e:
        #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

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
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
            print("\n{:^163}".format("-" * 163))
            print(pattern_headline.format("Id", "Name ^",
                  "Phone", "Email", "Birthday", "Address"))
            print("{:^163}".format("-" * 163))
            for id, obj in sorted(data.items(), key=lambda x: x[1].name.value):
                print(pattern_body.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
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
            for id, obj in sorted(data.items(), key=lambda x: x[1].name.value):
                print(pattern_body.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.tag.value),
                    check_value(obj.notes.value),
                ))
            print("\n{:^163}".format("-" * 163))
        else:
            raise ContactNotFound


class ViewContact(AbstractView):
    @input_error
    def display(self, data: dict):
        if data:
            pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}| {:<25}|"
            pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}| {:<25}|"
            print("\n{:^190}".format("-" * 190))
            print(pattern_headline.format("Id", "Name ^",
                  "Phone", "Email", "Birthday", "Address", "Tag"))
            print("{:^190}".format("-" * 190))
            for id, obj in sorted(data.items(), key=lambda x: x[1].name.value):
                print(pattern_body.format(
                    id,
                    check_value(obj.name.value),
                    check_value(obj.phone.value),
                    check_value(obj.email.value),
                    check_value(obj.birthday.value),
                    check_value(obj.address.value),
                    check_value(obj.tag.value),
                ))
            pattern_headline = "| {:<186} |"
            pattern_body = "| {:<186} |"
            print("{:^190}".format("-" * 190))
            print(pattern_headline.format("Notes"))
            print("{:^190}".format("-" * 190))
            for obj in sorted(data.values(), key=lambda x: x[0].name.value):
                print(pattern_body.format(
                    check_value(obj.notes),
                ))
            print("{:^190}".format("-" * 190))
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
            for id, obj in sorted(data.items(), key=lambda x: x[1][0].name.value):
                print(pattern_body.format(
                    id,
                    check_value(obj[0].name.value),
                    check_value(obj[0].phone.value),
                    check_value(obj[0].email.value),
                    check_value(obj[0].birthday.value),
                    check_value(obj[1]),
                ))
            print("{:^120}".format("-" * 120))
        else:
            raise ContactNotFound


def display_contacts(view: AbstractView, data) -> None:
    view.display(data)
