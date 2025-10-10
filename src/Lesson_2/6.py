import os
from random import choice


# Встроенные слова для игры
STANDART_WORDS = [
    "банан",
    "пончик",
    "граната",
    "помидор",
    "торнадо",
    "паркет",
    "иллюзия",
    "ссора",
    "барабулька",
    "рыбак",
    "сторож",
]

# Важные сообщения для вывода и рендера
MESSAGES = {
    "start_message": "Добро пожаловать в Весельницу!\n"
    + "Для начала необходимо загрузить словарь слов для угадывания.\n"
    + "\nВсе слова должны быть записаны только с использованием "
    + "кириллицы, все буквы строчные.\n"
    + "1 - Использовать только встроеннный словарь.\n"
    + "2 - Ввести свои слова по одному.\n"
    + "3 - Ввести строку своих слов, разделенных пробелами.",
    "word_field": "{}\nДлина слова: {}",
    "attemps_info": "Попытка: {}/{}",
    "commands_info": ""
    + "Во время разгадки слова вы можете воспользоваться "
    + "следующими командами:\n"
    + "1. Если вы устали отгадывать слово, то введите 'СДАЮСЬ'.\n"
    + "2. Если вы захотите выключить приложение, то введите 'СТОП'.",
    "jester_25": ""
    + "  |    \n"
    + "  |    \n"
    + "  |    \n"
    + "  |    \n"
    + "  |    \n"
    + "--|--  ",
    "jester_50": ""
    + "  ---- \n"
    + "  |    \n"
    + "  |    \n"
    + "  |    \n"
    + "  |    \n"
    + "--|--  ",
    "jester_75": ""
    + "  ---- \n"
    + "  |   |\n"
    + "  |   0\n"
    + "  |    \n"
    + "  |    \n"
    + "--|--  ",
    "jester_99": ""
    + "  ---- \n"
    + "  |   |\n"
    + "  |   0\n"
    + "  |  /|\\\n"
    + "  |    \n"
    + "--|--  ",
    "jester_100": ""
    + "  ---- \n"
    + "  |   |\n"
    + "  |   0   - {}\n"
    + "  |  /|\\\n"
    + "  |  / \\  \n"
    + "--|--  ",
}


class JesterState:
    """Хранение информации и состоянии текущей сессии."""

    def __init__(self, max_attemps: int):
        """Инициализация объекта JesterState.

        Аргументы:
            max_attemps (int): максимальное кол-во попыток в сессии.
        """
        self.is_alive = True
        self.current_attemp = 1
        self.max_attemps = max_attemps

    def wrong_answer(self) -> None:
        """Обработка неправильного угадывания"""
        self.current_attemp += 1

        if self.current_attemp > self.max_attemps:
            self.is_alive = False

    def get_percent(self) -> int:
        """Получение процента завершенности виселицы

        Вывод:
            int: процентное представление: 0 <= percent <= 100
        """
        return int(self.current_attemp / self.max_attemps * 100)


def render_word_field(current_string: str) -> None:
    """Рендер поля строки для угадывания слова.

    Аргументы:
        current_string (str): строка со всеми (не)угаданными буквами.
    """
    print(
        MESSAGES["word_field"].format(
            current_string.replace("", " ")[1:],
            len(current_string),
        )
    )


def render_jester_state(jester_state: JesterState) -> None:
    """Рендер виселицы.

    Аргументы:
        jester_state (JesterState): информация о состоянии сессии.
    """
    percent = jester_state.get_percent()

    if percent <= 25:
        print(MESSAGES["jester_25"])

    elif percent <= 50:
        print(MESSAGES["jester_50"])

    elif percent <= 75:
        print(MESSAGES["jester_75"])

    elif percent <= 99:
        print(MESSAGES["jester_99"])

    else:
        print(
            MESSAGES["jester_100"].format(
                "спасите" if jester_state.is_alive else "x_x (здох)"
            )
        )

    if jester_state.is_alive:
        print(
            MESSAGES["attemps_info"].format(
                jester_state.current_attemp,
                jester_state.max_attemps,
            )
        )


def clear_screen() -> None:
    """Метод для быстрой очистки экрана"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_user_words() -> list[str]:
    """Получение дополнительных слов для загадывания от пользователя,
    используется только в связке с ENTER.

    Вывод:
        list[str]: список всех указанных пользователем слов.
    """
    words = list()
    print("Вводите слова через ENTER...")
    print("Введите пустую строчку, если хотите закончить набор слов.")
    print()
    while word := input("> "):
        words.append(word)

    return words


def get_user_guess(
    random_word_len: int,
    current_string: str,
    jester_state: JesterState,
) -> str:
    """Окно для получения догадки пользователя со всеми рендерами.

    Аргументы:
        random_word_len (int): длина загаданного слова.
        current_string (str): строка со всеми (не)угаданными буквами.
        jester_state (JesterState): информация о состоянии сессии.

    Вывод:
        str: обработанная догадка пользователя или команда.
    """
    while True:
        clear_screen()

        render_word_field(current_string)
        render_jester_state(jester_state)

        guess = input("Введите вашу догадку:\n> ")

        if guess == "СДАЮСЬ":
            return guess

        if guess == "СТОП":
            return guess

        if len(guess) == random_word_len:
            return guess
        else:
            print(
                "\nДлина вашего слова не совпадает "
                + "с длиной загаданного!\n"
                + f"Длина загаданного: {random_word_len}\n"
                + f"Длина вашего слова: {len(guess)}"
            )
            input("\nНажмите ENTER, чтобы продолжить...")


def main():
    """Основная функция для запуска игры."""
    clear_screen()
    print(MESSAGES["start_message"])

    mode = int(input("> "))

    words = list()

    match mode:
        case 1:
            words = STANDART_WORDS
        case 2:
            clear_screen()
            words = get_user_words()
        case 3:
            clear_screen()
            print("Введите строчку всех слов через пробел...")
            words = input("> ").split()

    if mode != 1:
        clear_screen()
        print("Хотите ли вы включить в набор слов стандартные слова?")
        answer = input("да/нет\n> ").lower()
        if answer == "да":
            for standart_word in STANDART_WORDS:
                if standart_word not in words:
                    words.append(standart_word)

    clear_screen()
    if len(words) == 0:
        print("Ваш словарь пуст! Запустите программу заново!!!")
        exit()

    print(f"Ваш словарь: {", ".join(words)}" + ".")
    print("\n" + MESSAGES["commands_info"])

    input("Нажмите ENTER, чтобы продолжить...")

    while True:
        random_word = choice(words)

        current_string = "_" * len(random_word)

        jester_state = JesterState(10)

        is_win = False

        while True:
            guess = get_user_guess(
                len(random_word), current_string, jester_state
            )

            if guess == "СДАЮСЬ":
                jester_state.is_alive = False
                break

            if guess == "СТОП":
                exit()

            raw_current_string = list()

            for idx, (true_letter, guess_letter) in enumerate(
                zip(random_word, guess)
            ):
                if true_letter == guess_letter:
                    raw_current_string.append(true_letter)
                else:
                    raw_current_string.append(current_string[idx])

            current_string = "".join(raw_current_string)

            if guess == random_word or current_string == random_word:
                is_win = True
                break

            else:
                jester_state.wrong_answer()

                if not jester_state.is_alive:
                    break

        clear_screen()

        if is_win:
            print("Ты отгадал слово!\n")
            print("!! (⌒▽⌒) !!")
        else:
            print("Вы проиграли и были повешены :(")
            render_jester_state(jester_state)

        print(f"Загаданное слово: {random_word}")

        if is_win:
            print(f"Число попыток: {jester_state.current_attemp}")

        answer = input("\nПродолжим? да/нет\n> ")
        if answer.lower() != "да":
            exit()


if __name__ == "__main__":
    main()
