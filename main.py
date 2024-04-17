from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if  len(value[1:]) <= 15 and value[1:].isdigit():
            self.__value = value
        else:
            raise ValueError('Wrong telephone number')

class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Wrong date, expected DD.MM.YYYY")
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            phone = Phone(phone)
            self.phones.append(phone)
        except ValueError as i:
            raise ValueError(f"Error adding phone: {i}")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone number not found in record.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                try:
                    new_phone = Phone(new_phone)
                except ValueError as i:
                    raise ValueError(f"Error: {i}")
                p.value = new_phone.value
                return
        raise ValueError("Phone number not found in record.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            raise ValueError(f"Error adding birthday: {e}")

    def __str__(self):
        phones_str = ', '.join(str(phone.value) for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {self.birthday.value if self.birthday else None}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def find_next_weekday(self, day,weekday: int):
        days_ahead = weekday - day.weekday()
        if days_ahead <= 0:
            days_ahead += 7
            next_weekday = day + timedelta(days = days_ahead)
            if next_weekday.weekday() in [5,6]:
                next_weekday = next_weekday + timedelta(days = (7 - next_weekday.weekday()))
            return next_weekday
        
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        current_date = datetime.today().date()
        next_week = current_date + timedelta(weeks=1)
        for record in self.values():
            if record.birthday:
                next_birthday = record.birthday.date.replace(year=current_date.year)
                if current_date <= next_birthday <= next_week:
                    if next_birthday.weekday() in [5,6]:
                        next_birthday = self.find_next_weekday(next_birthday, 0)
                    upcoming_birthdays.append(f"{record.name.value}: {next_birthday.strftime("%d,%m,%Y")}")
                elif current_date > next_birthday:
                    next_birthday = record.birthday.date.replace(year=current_date.year + 1)
                    if current_date <= next_birthday <= next_week:
                        if next_birthday.weekday() in [5,6]:
                            next_birthday = self.find_next_weekday(next_birthday, 0)
                        upcoming_birthdays.append(f"{record.name.value}: {next_birthday.strftime("%d,%m,%Y")}")
        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise KeyError('Expected Name and Phone number')
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        raise KeyError(' Wrong arguments, expected - Name, OldNumber, NewNumber')
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Name not found")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phones(args, book: AddressBook):
    if len(args) != 1:
        raise KeyError('Expected Name')
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Name not found")
    return [p.value for p in record.phones]

@input_error
def show_all(book: AddressBook):
    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    contact = book.find(name)
    if contact:
        contact.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        record = Record(name)
        record.add_birthday(birthday)
        book.add_record(record)
        return f"New contact {name} created with birthday {birthday}"


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    contact = book.find(name)
    if contact:
        return f"{contact.name}'s birthday is on {contact.birthday.value}"
    else:
        return f"No contact found with name {name}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return upcoming_birthdays
    else:
        return ["No birthdays this week"]


def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:]
    return command, args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()