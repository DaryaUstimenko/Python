from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    email = models.EmailField(verbose_name='E-mail')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Seller(models.Model):
    POSITION_CHOICES = [
        ('Seller', 'Продавец'),
        ('Senior Seller', 'Старший продавец'),
        ('Sales Manager', 'Руководитель отдела продаж'),
    ]

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    email = models.EmailField(verbose_name='E-mail')
    hire_date = models.DateField(verbose_name='Дата приёма на работу')
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name='Позиция в фирме')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    sold_quantity = models.PositiveIntegerField(default=0, verbose_name='Количество проданного товара')

    def __str__(self):
        return self.name

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='Продавец')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    sale_date = models.DateField(verbose_name='Дата продажи')
    sale_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма продажи')

    def __str__(self):
        return f"Sale of {self.product.name} to {self.customer.first_name} {self.customer.last_name}"

