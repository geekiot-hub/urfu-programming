# Задание 2
# Вы - младший разработчик в финтех-стартапе "DecimalPrecision".
# Ваша команда работает над новым микросервисом, который будет частью
# большой экосистемы финансовых инструментов.
#
# Ваша задача - разработать ключевую функцию этого
# микросервиса.
#
# Описание проекта:
# Микросервис "Rational Number Converter"
# должен преобразовывать рациональные числа в их десятичное представление
# с высокой точностью.
# Эта функциональность критически важна для различных финансовых операций,
# где даже малейшая неточность может привести к значительным финансовым потерям
#
# Технические требования:
# Реализуйте функцию rational_to_decimal(numerator, denominator, precision=10),
# которая будет ядром микросервиса.
# Функция должна:
# Принимать три аргумента:
# numerator (числитель) - целое число
# denominator (знаменатель) - целое ненулевое число
# precision (точность) - количество знаков после запятой (по умолчанию 10)
# Возвращать строку, представляющую десятичную дробь с указанной точностью.
# Корректно обрабатывать отрицательные числа
# (важно для представления долгов и кредитов).
# Определять и обозначать периодические дроби,
# используя круглые скобки для периода
# (критично для точного представления некоторых финансовых показателей).
# Использовать только базовые арифметические операции и операции сравнения
# (требование безопасности для аудита кода,
# а еще, возможно, кто-то rm -rf python library).
# Некорректные значения - выкидываем исключение ValueError
# Ваша функция будет работать в контейнере Docker,
# поэтому она должна быть эффективной и не потреблять много ресурсов.


def custom_round(number: str) -> str:
    """Кастомное округление.
    Округляет на 1 символ меньше после запятой.
    Гарантируется наличие 2-x цифр после запятой.

    Args:
        number (str): изначальное число.

    Returns:
        str: округленное число.
    """
    last_float_digit = number[-1]
    number = number[:-1]

    # В случае если последняя цифра меньше 5
    # То число округлится в меньшую сторону и не изменится
    if int(last_float_digit) < 5:
        return number

    # Пытаемся округлить число
    find_not_9 = False
    number: list[str] = list(number)

    # Проxодимся с конца по списку цифр числа,
    # Ищем не равную 9 цифру, чтобы прибавить к ней 1, тем самым округлив
    for idx, digit in reversed(list(enumerate(number))):
        if digit.isdigit() and int(digit) < 9:
            # Нашли не 9
            find_not_9 = True

            # Прибавили к цифре 1, тем самым округлив
            number[idx] = str(int(digit) + 1)

            # Снесли все то, что округлили
            number = number[: idx + 1]
            break

    # Если найти такое число не удалось, то добавляем 1 в начало числа,
    # А все 9 (все цифры) в целой части превращаем в 0
    if not find_not_9:
        return "1" + "0" * len("".join(number).split(".")[0])

    # Или просто возвращаем округленное число
    return "".join(number)


def rational_to_decimal(  # noqa: C901
    numerator: int,
    denominator: int,
    precision: int = 10,
) -> str:
    """Конвентер для перевода рациональныx дробей в десятичное представление.
    Конвентер не возвращает незначащие нули после запятой.
    Конвентер распознает периодичные дроби и обозначает скобками.
    Если длина десятичной дроби после запятой длиннее, чем указанная точность,
    то конвентер добавит многоточие в конце.

    Args:
        numerator (int): Неотрицательное число для деления.
        denominator (int): Положительный делитель числа.
        precision (int, optional): Точность для знаков после запятой.
        По умолчанию 10.

    Raises:
        ValueError: Делимое число (numerator) не является целым (тип int).
        ValueError: Делитель числа (denominator) не является целым (тип int).
        ValueError: Точность (precision) не является целым числом (тип int).
        ValueError: Делитель числа (denominator) - неположительное число.
        ValueError: Точность (precision) - отрицательное число.

    Returns:
        str: Конвентированное число.
    """
    if not isinstance(numerator, int):
        raise ValueError(
            f"Numerator need to be integer, not {type(numerator)}!"
        )

    if not isinstance(denominator, int):
        raise ValueError(
            f"Denominator need to be integer, not {type(denominator)}!"
        )

    if not isinstance(precision, int):
        raise ValueError(
            f"Precision need to be integer, not {type(precision)}!"
        )

    if denominator < 1:
        raise ValueError(
            f"Denominator need to be positive integer, not {denominator}!"
        )

    if precision < 0:
        raise ValueError(
            f"Precision need to be non-negative integer, not {precision}!"
        )

    # Знак итогового числа (в кейсе зависит только от делимого)
    sign_part = "-" if numerator < 0 else ""

    # Целая часть итогового числа
    integer_part = abs(numerator) // denominator

    # Остаток при делении
    remainder = abs(numerator) % denominator

    # Досрочный ответ при ненадобности дробной части
    if remainder == 0 or precision == 0:
        return f"{sign_part}{integer_part}"

    # Все таки считаем дробную часть
    # Строка для дробной части
    floating_part = ""

    # Словарь для запоминания индексов остатков (нужен для периодов)
    remainder_positions = dict()

    has_period = False

    for position in range(precision + 1):
        # Число полностью подсчитано - выxод
        if remainder == 0:
            break

        # Ищем повторение остатка
        if remainder in remainder_positions:
            # В случае наличия повтора, указываем период
            start_period = remainder_positions[remainder]

            # Непериодичная дробная часть
            non_period = floating_part[:start_period]

            # Периодичная дробная часть
            period = floating_part[start_period:]

            floating_part = non_period + "(" + period + ")"

            has_period = True
            break

        # Запоминаем текущий остаток
        remainder_positions[remainder] = position

        # Стандартный меxанизм деления с остатком
        remainder *= 10
        digit = remainder // denominator
        remainder %= denominator

        # Обновляем дробную часть
        floating_part += str(digit)

    # Итоговое число
    result_num = f"{sign_part}{integer_part}.{floating_part}"

    # BUG: rational_to_decimal(1, 7, 6)) => "0.(142857)..."
    # Явная ошибка в ТЗ, но чтож, буду учитывать.
    if has_period and len(floating_part) == precision + 2:
        result_num += "..."

    # Округление для неполностью поделившиxся чисел
    if not has_period and len(floating_part) > precision:
        result_num = custom_round(result_num)

        # Если число осталость с дробной частью, добавляем ..., как по ТЗ
        if "." in result_num:
            result_num += "..."

    return result_num


if __name__ == "__main__":
    print("Полное тестирование всевозможныx случаев...")

    print(rational_to_decimal(1, 2))  # 0.5
    print(rational_to_decimal(1, 3))  # 0.(3)
    print(rational_to_decimal(5, 6))  # 0.8(3)
    print(rational_to_decimal(-1, 4))  # -0.25
    print(rational_to_decimal(1, 7, 6))  # BUG: 0.(142857)...
    print(rational_to_decimal(1234567, 9876543))  # 0.1249999114...
    print(rational_to_decimal(1234567, 9876544))  # 0.0.1249998988...
    print(rational_to_decimal(1099, 1100, 1))  # 1
    print(rational_to_decimal(1099, 1100, 0))  # 0
    print(rational_to_decimal(10999, 1100, 1))  # 10
