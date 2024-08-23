from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=255)
    isbn_code = models.CharField(max_length=13, unique=True)  # ISBN codes are usually 13 digits
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
