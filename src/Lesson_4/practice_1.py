class Employee:
    """Сотрудник Великой Компании"""

    def __init__(self, has_2_hands: bool, expirience: int):
        """Инициализация сотрудника

        args:
            has_2_hands (bool): качественно ли выполняет работу
            expirience (int): опыт работы в компании (в годах)
        """
        self.has_2_hands = has_2_hands
        self.expirience = expirience

    def get_salary(self) -> int:
        """Расчет зарплаты сотрудника

        Returns:
            int: зарплата в $ за месяц
        """
        salary = (
            1_000 * (2 if self.has_2_hands else 2.5) * self.expirience
        )

        return int(salary)


class Manager(Employee):
    """Менеджер Великой Компании

    Наследование от класса Employee
    """

    def __init__(self, has_2_hands: bool, expirience: int):
        """Инициализация менеджера

        Args:
            has_2_hands (bool): качественно ли выполняет работу
            expirience (int): опыт работы в компании (в годах)
        """
        super().__init__(has_2_hands, expirience)

    def get_salary(self) -> int:
        """Расчет зарплаты менеджера

        Returns:
            int: зарплата в $ за месяц
        """
        salary = super().get_salary() * 0.5
        return int(salary)


class Developer(Employee):
    """Разработчик Великой Компании

    Наследование от класса Employee
    """

    def __init__(
        self,
        has_2_hands: bool,
        expirience: int,
        love_python: bool = False,
    ):
        """Инициализация разработчика

        Args:
            has_2_hands (bool): качественно ли выполняет работу
            expirience (int): опыт работы в компании (в годах)
            love_python (bool, optional): нравится ли python.
            по умолчанию False
        """
        super().__init__(has_2_hands, expirience)
        self.love_python = love_python

    def get_salary(self) -> int:
        """Расчет зарплаты разработчика

        Returns:
            int: зарплата в $ за месяц
        """
        if self.love_python:
            print("Я боюсь змей, с тебя штраф")
            return -1_000

        return int(1_500 * self.expirience)


employee = Employee(has_2_hands=True, expirience=5)
manager = Manager(has_2_hands=True, expirience=5)
developer = Developer(
    has_2_hands=True, expirience=5, love_python=True
)

print(employee.get_salary(), "\n")
print(manager.get_salary(), "\n")
print(developer.get_salary(), "\n")
