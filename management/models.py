# Book {ISBN (PK), Title, AuthorID (FK), Publisher, PublishDate, Price}
# Author {AuthorID (PK), Name, Age, Country}

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    permission = models.IntegerField(default=1)

    def __str__(self):
        return self.user.username


class Author(models.Model):
    author_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField()
    country = models.CharField(max_length=80)

    class META:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    isbn = models.CharField(primary_key=True, max_length=13)
    title = models.CharField(max_length=99)
    author_ids = models.ManyToManyField(
        Author,
        related_name="book",
    )
    publisher = models.CharField(max_length=80)
    publish_date = models.DateField()
    Price = models.IntegerField()

    class META:
        ordering = ['title']

    def __str__(self):
        return self.title
