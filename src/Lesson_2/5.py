from typing import Union


FROM_ROMAN_NUMBERS = {
    "I": 1,
    "IV": 4,
    "V": 5,
    "IX": 9,
    "X": 10,
    "XL": 40,
    "L": 50,
    "XC": 90,
    "C": 100,
    "CD": 400,
    "D": 500,
    "CM": 900,
    "M": 1000,
}

FROM_DECIMAL_NUMBERS = {
    decimal: roman for roman, decimal in FROM_ROMAN_NUMBERS.items()
}
SORTED_DECIMAL_NUMBERS = sorted(
    FROM_DECIMAL_NUMBERS.keys(),
    reverse=True,
)


def translate_to_roman(decimal: int) -> str:
    """Перевод числа из десяточного представления в римское.

    Аргументы:
        decimal (int): число в десятичной системе исчесления.

    Вывод:
        str: римское представление входного числа.
    """
    roman_number = ""
    remaining_decimal = decimal

    while remaining_decimal > 0:
        for max_decimal_number in SORTED_DECIMAL_NUMBERS:
            if remaining_decimal < max_decimal_number:
                continue

            letter_cnt = remaining_decimal // max_decimal_number
            remaining_decimal %= max_decimal_number
            roman_number += (
                FROM_DECIMAL_NUMBERS[max_decimal_number] * letter_cnt
            )

    return roman_number


def translate_from_roman(roman_number: str) -> int:
    """Перевод числа из римского в десятичное.

    Аргументы:
        roman_number (str): строка-запись римского числа.

    Вывод:
        int: запись числа в человеческой (10-ой) системе исчесления.
    """
    # Итоговое число в 10-ой СИ.
    result_number = 0

    # Предыдущая цифра у текущего числа.
    # Изначально равна 0 для правильной работы алгоритма.
    prev_number = 0

    for letter in roman_number[::-1]:
        current_number = FROM_ROMAN_NUMBERS[letter]
        if current_number >= prev_number:
            result_number += current_number

        elif current_number < prev_number:
            result_number -= current_number

        prev_number = current_number

    return result_number


def get_input_numbers_list(type_: Union[int, str]) -> list:
    """Вспомогательная функция для получения входного списка чисел.

    Аргументы:
        type_ (Union[int, str]): тип ожидаемых чисел,
        для римских чисел - str, для десятичных - int.

    Вывод:
        list: список входных чисел
    """
    numbers = list()

    while answer := input("> "):
        if answer == "OK":
            break

        numbers.append(type_(answer))

    return numbers


if __name__ == "__main__":
    answer = input(
        "Выберите режим работы:\n"
        + "1 - Из римского в десятичное число\n"
        + "2 - Из десятичного в римское число\n"
        + "> "
    )
    mode = int(answer)

    print("Вводите числа через ENTER, для выхода введите 'OK'")
    if mode == 1:
        numbers = get_input_numbers_list(type_=str)
        translated_numbers = list(
            map(
                translate_from_roman,
                numbers,
            )
        )
    else:
        numbers = get_input_numbers_list(type_=int)
        translated_numbers = list(
            map(
                translate_to_roman,
                numbers,
            )
        )

    print("Вот ваши числа: ", translated_numbers)
