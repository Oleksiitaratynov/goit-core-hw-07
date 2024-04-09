from collections import defaultdict, UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


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
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError('Invalid phone number')


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(self.date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        # Phone('0951111111') == '0951111111'
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self, old_number, new_number):
        phone_to_edit = self.find_phone(old_number)
        if phone_to_edit:
            phone_to_edit.value = new_number

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find_next_birthday(self, weekday):
        pass

    def get_upcoming_birthday(self, days=7):
        pass


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "KeyError"
        except ValueError:
            return "ValueError"
        except IndexError:
            return "IndexError"
    return wrapper


@input_error
def add_contact(args, book: AddressBook):
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
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return "Phone number changed."
    else:
        return "Contact not found."


@input_error
def show_phones(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return '\n'.join(phone.value for phone in record.phones)
    else:
        return "Contact not found."


@input_error
def show_all(book: AddressBook):
    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        return "Contact not found"


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    else:
        return "Contact not found or birthday not set."


@input_error
def birthdays(args, book: AddressBook):
    days = int(args[0]) if args else 7
    upcoming_birthdays = []
    for record in book.data.values():
        if record.birthday and (0 <= (record.birthday.date - datetime.now().date()).days < days):
            upcoming_birthdays.append(record.name.value)
    return '\n'.join(upcoming_birthdays)


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
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            # реалізація
            pass

        elif command == "phone":
            # реалізація
            pass

        elif command == "all":
            # реалізація
            pass

        elif command == "add-birthday":
            # реалізація
            pass

        elif command == "show-birthday":
            # реалізація
            pass

        elif command == "birthdays":
            # реалізація
            pass

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()