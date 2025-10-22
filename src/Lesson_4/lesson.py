from abc import ABC, abstractmethod


class Printable(ABC):
    @abstractmethod
    def print_info(self) -> None:
        pass


class Book(Printable):
    def __init__(
        self,
        title: str,
        year: int,
        author: str,
    ) -> None:
        self.title = title
        self.year = year
        self.author = author

    def print_info(self) -> None:
        print(self)

    def info(self) -> str:
        return 'Книга "{}", автора: {}, {} года.'.format(
            self.title,
            self.author,
            self.year,
        )

    @classmethod
    def from_string(cls, string: str):
        title, year, author = string.split(";")
        return cls(title, int(year), author)

    @property
    def age(self) -> int:
        return self.year

    @age.setter
    def age(self, value: int):
        self.year = value

    def __str__(self) -> str:
        return self.info()

    def __eq__(self, other) -> bool:
        return isinstance(other, Book) and self.author == other.author


class EBook(Book):
    def __init__(
        self, title: str, year: int, author: str, format_: str
    ) -> str:
        super().__init__(title, year, author)
        self.format = format_

    def info(self) -> str:
        return 'Электронная книга "{}", автора: {}, {} года.'.format(
            self.title,
            self.author,
            self.year,
        )

    @classmethod
    def from_string(cls, string: str):
        title, year, author, format_ = string.split(";")
        return cls(title, int(year), author, format_)


book = Book.from_string("Новый Заголовок;2021;Новый автор")
print(book)
book.print_info()

ebook = EBook.from_string("Новый Заголовок;2021;Новый автор;epub")
print(ebook)
