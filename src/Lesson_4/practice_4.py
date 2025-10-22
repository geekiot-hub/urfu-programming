from enum import Enum


class Skills(Enum):
    """
    Перечисление навыков членов команды.
    """

    STRONG: str = "Strong"
    BRAVE: str = "Brave"
    HARDY: str = "Hardy"
    SMART: str = "Smart"


class Role(Enum):
    """
    Перечисление ролей в команде.
    """

    CAPTAIN: str = "Captain"
    WORKER: str = "Worker"
    DEAD: str = "Dead"


class CrewMember:
    """
    Член команды на космическом корабле.

    Attrs:
        name (str): Имя члена экипажа.
        health (int): Здоровье члена экипажа от 0 до 100.
        role (Role): Роль члена экипажа.
        skills (list[Skills]): Навыки участника.
    """

    def __init__(
        self,
        name: str,
        health: int,
        role: Role,
        skills: list[Skills] | None = None,
    ):
        """
        Инициализация члена команды.

        Args:
            name (str): Имя члена экипажа.
            health (int): Здоровье члена экипажа от 0 до 100.
            role (Role): Роль члена экипажа.
            skills (list[Skills] | None, optional): Навыки участника.
            По умолчанию None.
        """
        self.name = name
        self.health = health
        self.role = role
        self.skills = [] if skills is None else skills


class Mission:
    """
    Миссия для экипажа

    Attrs:
        target (str): цель миссии.
        resources (list[str]): ресурсы для миссии.
        events (list[str]): события, возможные во время миссии.
    """

    def __init__(
        self,
        target: str,
        resources: list[str],
        events: list[str],
    ):
        """
        Инициализация миссии экипажа.

        Args:
            target (str): цель миссии.
            resources (list[str]): ресурсы для миссии.
            events (list[str]): события, возможные во время миссии.
        """
        self.target = target
        self.resources = resources
        self.events = events


class SpaceShip:
    def __init__(
        self,
        fuel: int,
        current_speed,
        mission: Mission,
        members: list[CrewMember],
        hull_strength: int = 100,
    ):
        """
        Инициализация космического корабля.

        Args:
            fuel (int): кол-во топлива от 0 до 100 т.
            current_speed (_type_): текущая скорость в м/c.
            mission (Mission): миссия для выполнения.
            members (list[CrewMember]): участники команды корабля.
            hull_strength (int, optional): прочность корпуса.
            По умолчанию 100.
        """
        self.fuel = fuel
        self.current_speed = current_speed
        self.hull_strength = hull_strength
        self.mission = mission
        self.members = members

    def get_info(self):
        """Получение информации о корабле.

        Returns:
            str: краткая информация о корабле.
        """
        template = (
            "Ваш корабль: {} т. топлива, прочность корпуса: {}%"
            + "\nТекущая скорость: {} м/c"
            + "\nЦель миссии: {}"
            + "\nВаши ресурсы: {}"
            + "\nЧлены экипажа: {}"
            + "\nИх роли: {}"
        )

        return template.format(
            self.fuel,
            self.hull_strength,
            self.current_speed,
            self.mission.target,
            self.mission.resources,
            [member.name for member in self.members],
            [member.role.value for member in self.members],
        )

    def start_travels(self):
        """
        Попытка запуска космического корабля и выполнение миссии.
        """
        print("Вы разбились, ум ваче сей!")


if __name__ == "__main__":
    current_mission = Mission(
        target="Захватить планету Нибиру",
        resources=["Палка", "Замок", "Цепочка"],
        events=["Коллапс сверхновой", "Встреча с Ктулху", "8 марта"],
    )

    captain = CrewMember(
        name="Капитанчик Кабанчик",
        health=10,
        role=Role.CAPTAIN,
        skills=[Skills.BRAVE, Skills.SMART],
    )
    engineer = CrewMember(
        name="Инженер Женя",
        health=100,
        role=Role.WORKER,
        skills=[Skills.HARDY, Skills.SMART],
    )
    billy = CrewMember(
        name="Билли",
        health=-1,
        role=Role.DEAD,
        skills=None,
    )

    space_ship = SpaceShip(
        fuel=200,
        current_speed=10,
        mission=current_mission,
        members=[captain, engineer, billy],
        hull_strength=99,
    )

    print(space_ship.get_info())

    print("\nНачинаем приключение! 3...2...1...")
    space_ship.start_travels()
