from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    pass


class Series(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)

    @property
    def total_pages(self):
        total_pages = 0
        books = SeriesBook.objects.filter(full_series_id=self.id)
        for book in books:
            obj = Book.objects.filter(series=book)
            total_pages += obj.get('page_count')

        return total_pages


class SeriesBook(models.Model):
    full_series = models.OneToOneField(Series, on_delete=models.CASCADE)
    num_in_series = models.PositiveIntegerField()


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    page_count = models.PositiveIntegerField()
    series = models.OneToOneField(SeriesBook, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = [Lower('title')]


class UserBook(models.Model):
    read_count = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'book')


class ToReadBook(UserBook):
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class Read(UserBook):
    read_number = models.PositiveIntegerField()
    start_date = models.DateField()

    class Meta(UserBook.Meta):
        abstract = True


class InProgressRead(Read):
    current_page = models.PositiveIntegerField()


class FinishedRead(Read):
    end_date = models.DateField()
