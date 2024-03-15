from django.db import models
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class Book(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    description = models.CharField()
    pub_date = models.DateTimeField('date published')
    download_links = ArrayField(models.CharField(max_length=200))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/static/books/images', blank=True)

    def book_categories(self):
        return [i.name for i in self.categories.all()]

    def __str__(self):
        return self.name

