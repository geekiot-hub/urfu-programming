class Transport:
    """Родительский класс для видов транспорта"""

    def __init__(self, weight: int, name: str):
        """Инициализация транспорта

        Args:
            weight (int): вес транспорта
            name (str): название транспорта
        """
        self.weight = weight
        self.name = name

    def get_info(self) -> str:
        """Вывод информации о транспорте

        Returns:
            str: информация о транспорте
        """
        return f"Weight: {self.weight}\nName: {self.name}"


class Car(Transport):
    """Класс для объектов типа Машина.
    Наследован от Transport.
    """

    def __init__(self, weight: int, name: str, price: int):
        """Инициализация машины

        Args:
            weight (int): вес машины.
            name (str): марка машины.
            price (int): цена машины.
        """
        super().__init__(weight, name)
        self.price = price

    def get_info(self) -> str:
        """Получение информации о машине.

        Returns:
            str: информация о машине.
        """
        return super().get_info() + f"\nPrice: {self.price}"


class Skate(Transport):
    """Класс для объектов типа Skate.
    Наследован от Transport.
    """

    def __init__(self, weight: int, name: str, price: int):
        """Инициализация скейта

        Args:
            weight (int): вес скейта.
            name (str): название скейта.
            price (int): цена скейта.
        """
        super().__init__(weight, name)
        self.price = price

    def get_info(self) -> str:
        """Получение информации о скейте.

        Returns:
            str: информация о скейте.
        """
        return f"Name: {self.name}\nPrice: {self.price}"


class Chair(Transport):
    """Класс для объектов типа Chair.
    Наследован от Transport.
    """

    def __init__(self, weight: int, name: str, price: int):
        """Инициализация кресла.

        Args:
            weight (int): вес кресла.
            name (str): название кресла.
            price (int): цена кресла.
        """
        super().__init__(weight, name)
        self.price = price

    def get_info(self) -> str:
        """Получение полезной информации о кресле.

        Returns:
            str: строчка "I'm a chair!"
        """
        return "I'm a chair!"


def print_transport_info(transport):
    """Функция для отображения информации о транспорте.

    Args:
        transport (Transport): объект,
        наследованный от класса Transport.
    """
    if isinstance(transport, Transport):
        print(transport.get_info())


car = Car(10, "Машина", 13_000)
skate = Skate(0.05, "Скейт Крутой", 100)
chair = Chair(0.01, "Кресло Дорогое", 1_000)

print("1. car")
print_transport_info(car)
print()

print("2. skate")
print_transport_info(skate)
print()

print("3. chair")
print_transport_info(chair)
