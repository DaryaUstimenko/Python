from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Контактный телефон')
    note = models.TextField(blank=True, verbose_name='Примечание')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
