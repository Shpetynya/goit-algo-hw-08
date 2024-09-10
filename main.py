import pickle
from adressbook import AddressBook, Record


def parse_input(user_input):
    parts = user_input.split()
    command = parts[0]
    args = parts[1:]
    return command, args

def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Error: Not enough arguments provided."
        except KeyError as e:
            return f"Error: {e} not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
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
def change_contact(args, book):
    """Функція для зміни телефону контакту."""
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} changed from {old_phone} to {new_phone}."
    else:
        return f"Contact {name} not found."

@input_error
def show_phone(args, book):
    """Функція для показу телефонів контакту."""
    name = args[0]
    record = book.find(name)
    if record:
        return f"Phones for {name}: {', '.join(p.value for p in record.phones)}"
    else:
        return f"Contact {name} not found."

@input_error
def show_all(args, book):
    """Функція для показу всіх контактів."""
    return str(book)

@input_error
def add_birthday(args, book):
    """Функція для додавання дати народження контакту."""
    name = args[0]
    birthday = args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} set to {birthday}."
    else:
        return f"Contact {name} not found."


@input_error
def show_birthday(args, book):
    """Функція для показу дати народження контакту."""
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday for {name}: {record.birthday.value}"
    else:
        return f"Birthday for {name} is not set or contact not found."


@input_error
def birthdays(args, book):
    """Функція для показу днів народження на наступному тижні."""
    upcoming_birthdays = book.get_upcoming_birthdays()
    return '\n'.join([f"{bd['name']} - {bd['birthday']}" for bd in upcoming_birthdays])


def save_data(book, filename="addressbook.pkl"):
    """Функція для збереження даних у файл"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    """Функція для загрузки файлу"""
    try:   # Відкриваємо файл якщо він існує
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повертаємось до поточної адресної книги якщо файл ще не існує

def main():
    book = load_data() # Підгружаємо файл у головну функцію
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)   # Якщо закриваємо бот, виконується автоматичне збереження файлу
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
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
