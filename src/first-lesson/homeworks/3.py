# Задание 3
# Ваш микросервис "Rational Number Converter" имел большой успех,
# и теперь руководство "DecimalPrecision" поручило вам разработать
# новую функцию для обратного преобразования.
#
# Эта функция будет использоваться в модуле обработки финансовых транзакций,
# где критически важна точность и надежность преобразования
# строковых данных в числовые.
#
# Описание задачи:
# Реализуйте функцию custom_string_to_int(s),
# которая преобразует строковое представление целого числа в
# соответствующее целочисленное значение типа int.
#
# Важно: вы не можете использовать встроенную функцию int()
# или любые другие встроенные функции преобразования типов.
#
# Технические требования:
# Функция должна принимать один аргумент - строку s,
# представляющую целое число.
# Функция должна возвращать целое число типа int.
# Необходимо корректно обрабатывать положительные и отрицательные числа.
# Функция должна выбрасывать исключение ValueError
# для некорректных входных данных.


def custom_string_to_int(s: str) -> int:
    """Преобразует строковое представление целого числа в int.

    Args:
        s (str): Строковое представление целого числа.

    Raises:
        ValueError: s не является строкой (тип str).
        ValueError: Вxодная строка пустая.
        ValueError: Вxодная строка не содержит чисел.
        ValueError: Вxодная строка содержит некорректный символ.

    Returns:
        int: Преобразованное целое число.
    """
    if not isinstance(s, str):
        raise ValueError(f"s должно быть строкой, а не {type(s)}!")

    if not s:
        raise ValueError("Пустая строка!")

    is_negative = False
    start_idx = 0

    if s[0] == "-":
        is_negative = True
        start_idx = 1
    elif s[0] == "+":
        start_idx = 1

    if start_idx >= len(s):
        raise ValueError("Строка не содержит число!")

    result = 0
    zero_code = ord("0")
    nine_code = ord("9")

    for char_idx in range(start_idx, len(s)):
        char = s[char_idx]
        char_code = ord(char)

        # Проверка, является ли символ цифрой
        if char_code < zero_code or char_code > nine_code:
            raise ValueError(f"Некорректный символ: '{char}'")

        digit = char_code - zero_code
        result *= 10
        result += digit

    return -result if is_negative else result


if __name__ == "__main__":
    print("Полное тестирование всевозможныx случаев...")
    test_cases = (
        "-109484",
        "+45",
        "159",
        "-",
        "+",
        "0",
        "-115",
        1.5,
        "-455p45",
    )

    for test in test_cases:
        try:
            result = custom_string_to_int(test)
            print(f"s = {test}, result = {result}")
        except Exception as err:
            print(f"s = {test}, error = {err}")
