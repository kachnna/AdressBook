from dataclasses import dataclass
from record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes


class TestData:
    test_contacts = {1: Record(Name("Bruce Wayne"), Phone("600 123 456"), Email("bwayne@gothammail.com"),
                               Birthday("1985-10-20"), Address("174 Batman Street, Gotham City"), Tag(
                                   "superhero, Batman, billionaire"),
                               Notes("Bruce Wayne is the billionaire playboy philanthropist."),),
                     2: Record(Name("Piotr Wiśniewski"), Phone("512 987 654"), Email("pwisniewski@email.com"), Birthday("1992-03-07"),
                               Address("Warszawa, 00-001, ul. Kwiatowa 5/3"), Tag("Mechanik"), Notes(""),),
                     }


@property
def value(self):
    return self._value


@value.setter
def value(self, new_value):
    self._value = new_value
