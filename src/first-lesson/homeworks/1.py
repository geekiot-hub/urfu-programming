# Задание 1
# Вы работаете в IT-отделе городского транспортного предприятия. Ваша
# команда разрабатывает новую систему электронных билетов для трамваев.
# Один из ваших коллег заметил интересную закономерность в нумерации
# билетов и предложил внедрить функцию, которая будет определять "почти
# счастливые" билеты.
# Ваша задача - написать функцию на Python, которая будет проверять,
# является ли предыдущий или следующий билет "счастливым".
# Входные данные: строку с шестизначным номером "почти счастливого"
# билета. Выходные данные: булево значение True, если предыдущий или
# следующий билет счастливый, и False в противном случае.


def check_neighbor_lucky(ticket_num: int) -> bool:
    """Checking whether the neighboring ticket is a "lucky ticket".

    Args:
        ticket_num (int): ticket number to check.

    Returns:
        bool: is the neighboring ticket a "lucky ticket".
    """
    # Ticket numbers can range from (0, 999_999)
    # However, ticket number 0 has no neighbor on the left and is unlucky.
    # A ticket with number 999_999 has no neighbor on the right and is unlucky.
    # Therefore, a ticket with number n is unlucky if n < 1 or n > 999_999.
    if ticket_num < 1 or ticket_num > 999_999:
        return False

    def check_lucky(num: int) -> bool:
        """Checking whether the ticket is a "lucky ticket"

        Args:
            num (int): ticket number to check.

        Returns:
            bool: is the ticket a "lucky ticket".
        """
        string_num = str(num).zfill(6)

        left_sum = sum(map(int, string_num[:3]))
        right_sum = sum(map(int, string_num[3:]))

        return left_sum == right_sum

    return check_lucky(ticket_num - 1) or check_lucky(ticket_num + 1)


# Start verification...
if __name__ == "__main__":
    for ticket_num in range(0, 999_999 + 1):
        print(ticket_num, check_neighbor_lucky(ticket_num))
