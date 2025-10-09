"""
Требуется написать программу,
для шифровки и дешифровки по шифру Цезаря.

На вход подается строка, состоящая из слов в нижнем регистре.
"""

from string import ascii_lowercase


def get_shifted_letter(letter: str, shift: int) -> str:
    """Получение сдвинутой буквы для (де)шифровки.

    Аргументы:
        letter (str): буква для сдвига.
        shift (int): сдвиг для буквы.

    Вывод:
        str: сдвинутая буква.
    """
    alph = ""

    if letter in ascii_lowercase:
        alph = ascii_lowercase
    else:
        alph = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    alph_len = len(alph)
    shifted_letter = alph[(alph.index(letter) + shift) % alph_len]

    return shifted_letter


def get_shifted_text(text: str, shift: int) -> str:
    """Функция для сдвига текста в шифре Цезаря

    Аргументы:
        text (str): требующий сдвиг текст.
        shift (int): сдвиг для каждой буквы в тексте.

    Вывод:
        str: сдвинутый текст
    """
    shifted_text = ""

    for letter in text:
        if letter.isalpha():
            shifted_letter = get_shifted_letter(letter, shift)
            shifted_text += shifted_letter
        else:
            shifted_text += letter

    return shifted_text


def get_encrypted_text(text: str, shift: int) -> str:
    """Шифрование текста по шифру Цезаря.

    Аргументы:
        text (str): текст, который необходимо зашифровать.
        shift (int): сдвиг для каждой буквы текста.

    Вывод:
        str: зашифрованный текст.
    """
    return get_shifted_text(text, shift)


def get_decrypted_text(text: str, shift: int) -> str:
    """Дешифровка текста по шифру Цезаря.

    Аргументы:
        text (str): текст, который необходимо расшифровать.
        shift (int): сдвиг, используемый для шифрования текста.

    Вывод:
        str: зашифрованный текст.
    """
    return get_shifted_text(text, -shift)


if __name__ == "__main__":
    answer = input(
        "Введите режим работы\n"
        + "1 - шифрование текста\n"
        + "2 - расшифрока текста\n"
        + "> "
    )
    mode = int(answer)

    text = input("Укажите текст: ").lower()
    shift = int(input("Укажите сдвиг: "))

    result_text = ""

    if mode == 1:
        result_text = get_encrypted_text(text, shift)
    elif mode == 2:
        result_text = get_decrypted_text(text, shift)

    text_action = "зашифрованный" if mode == 1 else "расшифрованный"
    print(f"\nВаш {text_action} текст:\n{result_text}")
