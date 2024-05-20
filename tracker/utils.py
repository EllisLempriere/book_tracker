from django.db.models import Max
from tracker.models import UserBook, ToReadBook


def get_max_order(user) -> int:
    existing_books = UserBook.objects.filter(user=user)
    if not existing_books.exists():
        return 1
    else:
        current_max = existing_books.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1


def reorder(user):
    existing_books = ToReadBook.objects.filter(user=user)
    if not existing_books.exists():
        return

    number_of_books = existing_books.count()
    new_ordering = range(1, number_of_books + 1)

    for order, user_book in zip(new_ordering, existing_books):
        user_book.order = order
        user_book.save()
