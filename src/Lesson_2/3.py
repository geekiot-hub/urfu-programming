"""
Требуется написать программу, которая будет перебирать кол-во
пирожных от 1 до N, и отвечать, на какие коробки (по 3 или 5)
пирожных их можно расфасовать и можно ли такое сделать вообще.

Ввод: N - макс. кол-во пирожных

Вывод: K (1 <= K <= N) - можно/нельзя расфасовать по 3/5 ...
"""


def print_pack_report(max_cakes_cnt: int) -> None:
    """
    Написание отчета по возможности фасовки
    от 1 до max_cakes_cnt кексов.

    Аргументы:
        max_cakes_cnt (int): максимальное число кексов для фасовки.
    """
    for cakes_cnt in range(1, max_cakes_cnt + 1):
        mult_by_3 = cakes_cnt % 3 == 0
        mult_by_5 = cakes_cnt % 5 == 0

        if mult_by_3 and mult_by_5:
            print(f"{cakes_cnt} - расфасуем по 3 или 5")

        elif mult_by_3:
            print(f"{cakes_cnt} - расфасуем по 3")

        elif mult_by_5:
            print(f"{cakes_cnt} - расфасуем по 5")

        else:
            print(f"{cakes_cnt} - не заказываем!")


if __name__ == "__main__":
    answer = input("Введите макс. кол-во кексов: ")
    max_cakes_cnt = int(answer)
    print_pack_report(max_cakes_cnt)
