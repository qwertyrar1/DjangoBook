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


class File(models.Model):
    name = models.CharField(max_length=100, default=1)
    file_field = models.FileField(upload_to='books/static/books/files')

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    description = models.CharField()
    pub_date = models.DateTimeField('date published')
    txt_download_link = models.OneToOneField(File, on_delete=models.CASCADE, blank=True, related_name='txt_link',
                                             null=True, default=1)
    rtf_download_link = models.OneToOneField(File, on_delete=models.CASCADE, blank=True, related_name='rtf_link',
                                             null=True, default=1)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/static/books/images', blank=True)

    def book_categories(self):
        return [i.name for i in self.categories.all()]

    def __str__(self):
        return self.name
