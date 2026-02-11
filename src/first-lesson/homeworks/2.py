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


def rational_to_decimal(
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

    for position in range(precision):
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
            break

        # Запоминаем текущий остаток
        remainder_positions[remainder] = position

        # Стандартный меxанизм деления с остатком
        remainder *= 10
        digit = remainder // denominator
        remainder %= denominator

        # Обновляем дробную часть
        floating_part += str(digit)
    else:
        # Добавляем многоточие если цикл завершился,
        # а число полностью не поделилось
        floating_part += "..." if remainder != 0 else ""

    return f"{sign_part}{integer_part},{floating_part}"


if __name__ == "__main__":
    print("Полное тестирование всевозможныx случаев...")

    testing_numbers = (
        (10, 3, 10),
        (1, 81, 20),
        (-1, 2, 5),
        (1, 6, 10),
        (10, 2, 2),
        (12, 6, 0),
        (0, 2, 1),
        (141, 7, 5),
        (2, -1, 10),
        (1.5, 1, 1),
        (2, 2, -1),
    )

    for n, d, p in testing_numbers:
        try:
            result = rational_to_decimal(n, d, p)
            print(f"numerator={n}, denominator={d}, precision={p}: {result}")
        except Exception as err:
            print(f"numerator={n}, denominator={d}, precision={p}: {err}")
