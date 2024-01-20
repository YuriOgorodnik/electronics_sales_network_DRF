from django.db import models


class Company(models.Model):
    """
    Модель Company представляет собой компанию в иерархии сети по продаже электроники.
    Она может быть заводом, розничной сетью или индивидуальным предпринимателем
    """

    FACTORY = 0
    RETAIL_NETWORK = 1
    INDIVIDUAL_ENTREPRENEUR = 2
    COMPANY_TYPES = [
        (FACTORY, "Factory"),
        (RETAIL_NETWORK, "Retail Network"),
        (INDIVIDUAL_ENTREPRENEUR, "Individual Entrepreneur"),
    ]

    name = models.CharField(max_length=255, verbose_name="название компании")
    company_type = models.IntegerField(
        choices=COMPANY_TYPES, verbose_name="тип компании"
    )
    email = models.EmailField(unique=True, verbose_name="электронная почта компании")
    country = models.CharField(max_length=50, verbose_name="страна нахождения компании")
    city = models.CharField(max_length=50, verbose_name="город нахождения компании")
    street = models.CharField(max_length=100, verbose_name="улица нахождения компании")
    house_number = models.CharField(
        max_length=20, verbose_name="номер дома нахождения компании"
    )
    supplier = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="clients"
    )
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="задолженность перед поставщиком"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время создания записи"
    )

    def __str__(self):
        """
        Возвращает строковое представление объекта Company, содержащее его название
        """
        return self.name

    @property
    def hierarchy_level(self):
        """
        Определяет и возвращает уровень иерархии компании
        """

        # Завод всегда находится на 0 уровне
        if self.company_type == self.FACTORY:
            return 0

        # Если поставщик не указан, считаем уровень максимальным
        if not self.supplier:
            return max(self.RETAIL_NETWORK, self.INDIVIDUAL_ENTREPRENEUR)

        # В противном случае определяем уровень на основе поставщика
        return self.supplier.hierarchy_level + 1


class Product(models.Model):
    """
    Модель Product представляет собой продукт, который продает компания
    """

    name = models.CharField(max_length=200, verbose_name="название продукта")
    model = models.CharField(max_length=200, verbose_name="модель продукта")
    release_date = models.DateField(verbose_name="дата выхода продукта на рынок")
    company = models.ForeignKey(
        Company, related_name="products", on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Возвращает строковое представление объекта Product, содержащее название и модель продукта
        """
        return f"{self.name} ({self.model})"
