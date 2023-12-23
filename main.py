from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self._value = None  # Приватний атрибут для значення
        self.set_value(value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)

class Name(Field):
    def __init__(self, first_name):
        self.set_first_name(first_name)

    def set_first_name(self, first_name):
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("First name is required and must be a non-empty string")
        self.set_value(first_name.strip())

class Phone(Field):
    def is_valid(self, number):
        if re.match(r'^\d{10}$', number):
            return True
        return False

    def set_value(self, value):
        if not self.is_valid(value):
            raise ValueError('Invalid number')
        super().set_value(value)

class Birthday(Field):
    def set_value(self, date_str):
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            self._value = date_obj
        else:
            self._value = None

    def days_to_birthday(self):
        if self._value:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self._value.month, self._value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self._value.month, self._value.day).date()
            days_left = (next_birthday - today).days
            return days_left
        return None
            

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
            return f"Phone number {phone} added successfully"
        except ValueError as e:
            return f"Error: {e}"

    def remove_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)
                return f"Phone number {phone} removed successfully"
        return f"Phone number {phone} not found"

    def edit_phone(self, old_phone, new_phone):
        for phone_obj in self.phones:
            if phone_obj._value == old_phone:
                phone_obj._value = new_phone
                return f"Phone number {old_phone} edited successfully"
        raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for phone_obj in self.phones:
            if phone_obj._value == phone:
                return phone_obj
        return None

    def get_phones(self):
        return [str(phone._value) for phone in self.phones]


    def __str__(self):
        phones_str = "; ".join(self.get_phones())
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name._value] = record

    def iterator(self, batch_size=1):
        current_index = 0
        while current_index < len(self.data):
            yield list(self.data.values())[current_index:current_index + batch_size]
            current_index += batch_size

    def find(self, name):
        return self.data.get(name)
    
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted successfully"
        return f"Record {name} not found"

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

john = Record("John", "2000-05-20")
print(john.birthday.days_to_birthday())  # Виведення кількості днів до наступного дня народження

# Перевірка пагінації
for batch in book.iterator(batch_size=1):
    for record in batch:
        print(record)

