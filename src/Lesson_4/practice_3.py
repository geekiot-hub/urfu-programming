class Product:
    """
    Продукт в магазине.

    Attrs:
        name (str): название продукта.
        price (int): цена продукта.
        in_stock (bool): наличие продукта на складе.
        category (str): категория продукта.
    """

    def __init__(
        self,
        name: str,
        price: int,
        in_stock: bool,
        category: str,
    ):
        """
        Инициализация продукта.

        Args:
            name (str): название продукта.
            price (int): цена продукта.
            in_stock (bool): наличие продукта на складе.
            category (str): категория продукта.
        """
        self.name = name
        self.price = price
        self.in_stock = in_stock
        self.category = category


class ShoppingCart:
    """
    Корзина в магазине.

    Attrs:
        _products (list[Product]): продукты в корзине.
    """

    def __init__(self):
        """Инициализация корзины"""
        self._products: list[Product] = list()

    @property
    def products(self) -> list:
        """
        Доступ к списку продуктам.

        Returns:
            list: список названий продуктов в корзине.
        """
        return [product.name for product in self._products]

    def add_product(self, product: Product) -> None:
        """
        Добавление продукта в корзину.

        Args:
            product (Product): продукт из магазина.
        """
        if product.in_stock:
            self._products.append(product)

    def remove_product(self, product_index: int) -> Product:
        """
        Удаление продукта из корзины.

        Args:
            product_index (int): индекс продукта в корзине.

        Returns:
            list[str]: список имен оставшихся продуктов в корзине.
        """
        self._products.pop(product_index)
        return self.products

    def get_total_price(self) -> int:
        """
        Расчет итоговой стоимости всех продуктов в корзине.

        Returns:
            int: итоговая цена без учета скидок и налогов.
        """
        return sum(product.price for product in self._products)


class Order:
    """
    Заказ в магазине

    Attrs:
        shopping_cart (ShoppingCart): корзинка покупателя.
        total_price (int): итоговая стоимость заказа.
    """

    def __init__(
        self,
        shopping_cart: ShoppingCart,
        tax: int = 0,
        discount: int = 0,
    ):
        """
        Инициализация заказа.

        Args:
            shopping_cart (ShoppingCart): корзинка покупателя.
            tax (int, optional): Налог. По умолчанию 0.
            discount (int, optional): Скидка от 0 до 100.
            По умолчанию 0.
        """
        self.shopping_cart = shopping_cart
        self.total_price = int(
            self.shopping_cart.get_total_price()
            * (100 - discount)
            / 100
            + tax
        )


class Customer:
    """
    Покупатель в магазине.

    Attrs:
        name (str): Имя покупателя.
        age (int): Возраст покупателя.
        _orders (list[Order]): список заказов.
    """

    def __init__(self, name: str, age: int):
        """
        Инициализация покупателя.

        Args:
            name (str): Имя покупателя.
            age (int): Возраст покупателя.
        """
        self.name = name
        self.age = age
        self._orders = []

    @property
    def orders(self) -> list:
        """
        Получение всех заказов покупателя.

        Returns:
            list: список итоговых цен всех заказов покупателя.
        """
        return [order.total_price for order in self._orders]

    def add_order(self, order: Order) -> None:
        """
        Добавление нового заказа.

        Args:
            order (Order): новый заказ.
        """
        self._orders.append(order)


if __name__ == "__main__":
    apple = Product("Apple", 100, True, "Fruits")
    pie = Product("Pie", 1_000, True, "Sweets")
    banana = Product("Banana", 10, False, "Fruits")

    cart = ShoppingCart()
    cart.add_product(apple)
    cart.add_product(pie)
    cart.add_product(banana)
    print("Продукты в корзине:", cart.products)
    print("Цена продуктов в корзине:", cart.get_total_price())

    order = Order(cart, 200, 10)
    print("Чек заказа (налог 200$, скидка 10%):", order.total_price)

    customer = Customer("Grisha", 24)
    customer.add_order(order)
    print("Покупки покупателя Гришы:", customer.orders)
