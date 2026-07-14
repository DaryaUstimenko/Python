from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    genre = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Reader(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=20)
    email = models.EmailField()
    membership_date = models.DateField(auto_now_add=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
