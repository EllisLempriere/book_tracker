from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


class User(AbstractUser):
    pass


class Series(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    @property
    def total_pages(self):
        total_pages = 0
        books = SeriesBook.objects.filter(full_series_id=self.id)
        for book in books:
            obj = Book.objects.filter(series=book)
            total_pages += obj.get('page_count')

        return total_pages

    def __str__(self):
        return f"{self.title}"


class SeriesBook(models.Model):
    full_series = models.OneToOneField(Series, on_delete=models.CASCADE)
    num_in_series = models.PositiveIntegerField()

    def __str__(self):
        return f"#{self.num_in_series} in {self.full_series.title}"


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    page_count = models.PositiveIntegerField()
    series = models.OneToOneField(SeriesBook, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = [Lower('title')]

    def __str__(self):
        return f"{self.title}"


class UserBook(models.Model):
    read_count = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ('user', 'book')


class ToReadBook(UserBook):
    order = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.book.title} at #{self.order} for {self.user}"


class Read(UserBook):
    read_number = models.PositiveIntegerField()
    start_date = models.DateField()

    class Meta(UserBook.Meta):
        abstract = True


class InProgressRead(Read):
    current_page = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} at page {self.current_page} in {self.book.title}"


class FinishedRead(Read):
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user} finished {self.book.title} at {self.end_date}"
