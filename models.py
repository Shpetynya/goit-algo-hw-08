import re
from datetime import datetime

class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    """Клас для зберігання номера телефону."""
    def __init__(self, phone):
        if not self.validate_phone(phone):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(phone)

    @staticmethod
    def validate_phone(phone):
        """Перевіряє, чи номер телефону складається з 10 цифр."""
        return bool(re.fullmatch(r'\d{10}', phone))

class Birthday(Field):
    """Клас для зберігання дати народження."""
    def __init__(self, value):
        self.value = value  # Значення зберігається як рядок
        self._validate()

    def _validate(self):
        """Валідація формату дати"""
        try:
            # Перевірка формату дати, але не зміна value
            datetime.strptime(self.value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        """Для відображення дати у вигляді рядка."""
        return self.value  # Повертаємо рядок у вихідному форматі
