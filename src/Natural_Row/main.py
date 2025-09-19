import sys

sys.set_int_max_str_digits(0)


def fast_get_digit(n):
    digits = 1
    count = 9

    while n > digits * count:
        n -= digits * count
        digits += 1
        count *= 10

    number = (count // 9) + (n - 1) // digits
    index = (n - 1) % digits

    return str(number)[index]


print(fast_get_digit(eval(input("Введите степень n: "))))
