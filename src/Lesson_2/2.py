def check_winners(scores: list[int], student_score: int) -> None:
    """Функция для проверки попадения в тройку победителей.

    Аргументы:
        scores (list[int]): все баллы участников олимпиады.
        student_score (int): ваш балл в олимпиаде.
    """
    if student_score in sorted(scores, reverse=True)[:3]:
        print("Вы в тройке победителей")
        return

    print("Вы не попали в тройку победителей")


if __name__ == "__main__":
    answer = input("Введите очки всех участников через пробел\n> ")
    scores = list(map(int, answer.split()))

    current_score = int(input("Введите кол-во ваших очков: "))

    check_winners(scores, current_score)
