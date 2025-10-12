from random import choice
from string import (
    ascii_lowercase,
    ascii_uppercase,
    digits,
    punctuation,
)


class PasswordInfo:
    """Класс для хранения информации о пароле"""

    def __init__(
        self,
        password_len: int,
        has_digits: bool,
        has_upper_case: bool,
        has_lower_case: bool,
        has_special_symbols: bool,
    ):
        """Инициализация информации о пароле.

        Аргументы:
            password_len (int): длина пароля.
            has_digits (bool): наличие цифр в пароле.
            has_upper_case (bool): наличие букв верхнего регистра.
            has_lower_case (bool): наличие букв нижнего регистра.
            has_special_symbols (bool): наличие спец. символов.
        """
        self.password_len = password_len
        self.has_digits = has_digits
        self.has_upper_case = has_upper_case
        self.has_lower_case = has_lower_case
        self.has_special_symbols = has_special_symbols

    def validate(self, password: str) -> bool:
        """Проверка на совпадение информации о пароле и пароля.

        Аргументы:
            password (str): пароль для которого требуется проверка.

        Вывод:
            bool: результат сравнения пароля и информации о нем.
        """
        password_info = parse_password_info(password)
        return self.__dict__ == password_info.__dict__


def parse_password_info(password: str) -> PasswordInfo:
    """Парсер для получения информации о пароле из пароля.

    Аргументы:
        password (str): пароль для парсинга информации.

    Вывод:
        PasswordInfo: информация о пароле.
    """
    has_digits = False
    has_upper_case = False
    has_lower_case = False
    has_special_symbols = False

    for letter in password:
        if letter in digits:
            has_digits = True

        if letter in ascii_uppercase:
            has_upper_case = True

        if letter in ascii_lowercase:
            has_lower_case = True

        if letter in punctuation:
            has_special_symbols = True

    return PasswordInfo(
        password_len=len(password),
        has_digits=has_digits,
        has_upper_case=has_upper_case,
        has_lower_case=has_lower_case,
        has_special_symbols=has_special_symbols,
    )


def generate_random_string(alph: str, string_len: int) -> str:
    """Генерация строки из случайных символов алфавита.

    Аргументы:
        alph (str): алфавит символов для выбора случайных символов.
        string_len (int): длина случайной строки символов.

    Вывод:
        str: случайная строка символов.
    """
    string = ""

    for _ in range(string_len):
        string += choice(alph)

    return string


def generate_password(password_info: PasswordInfo) -> str:
    """Генерация случайного пароля на основе информации о нем.

    Аргументы:
        password_info (PasswordInfo): информация о пароле.

    Вывод:
        str: соответствующий характеристикам случайный пароль.
    """

    alph = ""

    if password_info.has_digits:
        alph += digits

    if password_info.has_upper_case:
        alph += ascii_uppercase

    if password_info.has_lower_case:
        alph += ascii_lowercase

    if password_info.has_special_symbols:
        alph += punctuation

    while True:
        password = generate_random_string(
            alph,
            password_info.password_len,
        )

        if password_info.validate(password):
            return password


if __name__ == "__main__":
    print("Добро пожаловать в генератор паролей v2.13.1")
    _ = input("Нажмите Enter, если хотите сгенерировать пароль...")
    print("Отлично перейдем к настройке пароля!")

    answer = input("Введите необходимую длину пароля: ")
    password_len = int(answer)

    answer = input(
        "Требуется ли наличие букв в нижнем регистре (да/нет): "
    )
    has_lower_case = True if answer.lower() == "да" else False

    answer = input(
        "Требуется ли наличие букв в верхнем регистре (да/нет): "
    )
    has_upper_case = True if answer.lower() == "да" else False

    answer = input("Требуется ли наличие цифр (да/нет): ")
    has_digits = True if answer.lower() == "да" else False

    answer = input("Требуется ли наличие спец. символов (да/нет): ")
    has_special_symbols = True if answer.lower() == "да" else False

    password_info = PasswordInfo(
        password_len=password_len,
        has_digits=has_digits,
        has_upper_case=has_upper_case,
        has_lower_case=has_lower_case,
        has_special_symbols=has_special_symbols,
    )
    password = generate_password(password_info)

    print("\nВот ваш пароль:", password, sep="\n")
