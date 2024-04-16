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
        except ValueError as e:
            raise ValueError(f"Error adding phone: {e}")

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
                except ValueError as e:
                    raise ValueError(f"Error: {e}")
                p.value = new_phone.value
                return
        raise ValueError("Phone number not found in record.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.today().date()

        if self.birthday:
            birthday = self.birthday.date

            next_birthday = birthday.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            while next_birthday.weekday() >= 5:
                next_birthday += timedelta(days=1)

            days_until_birthday = (next_birthday - today).days
            if 0 <= days_until_birthday <= 7:
                upcoming_birthdays.append({
                    "name": self.name.value,
                    "congratulation_date": next_birthday.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays

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
        raise KeyError('Please enter contact name and phone number')
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
        raise KeyError('Please enter contact name')
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
    if len(args) != 2:
        raise KeyError('Please enter contact name and birthday date')
    name, birthday, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if birthday:
        record.add_birthday(birthday)
    return message

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        raise KeyError('Please enter contact name')
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Name not found")
    return record.birthday.value

@input_error
def birthdays(book: AddressBook):
    return book.get_upcoming_birthday()

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