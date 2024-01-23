from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView, ListView
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from book_tracker import settings
from tracker.forms import RegisterForm
from tracker.models import Book, UserBook
from tracker.utils import get_max_order, reorder


class IndexView(TemplateView):
    template_name = 'index.html'


class Login(LoginView):
    template_name = 'registration/login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super.form_valid(form)


class BookList(LoginRequiredMixin, ListView):
    template_name = 'books.html'
    model = UserBook
    context_object_name = 'books'

    def get_template_names(self):
        if self.request.htmx:
            return 'partials/book-list-elements.html'
        return 'books.html'

    def get_queryset(self):
        return UserBook.objects.prefetch_related('book').filter(user=self.request.user)


# HTMX
def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")


@login_required
def add_book(request):
    name = request.POST.get('bookname')

    book = Book.objects.get_or_create(name=name)[0]

    if not UserBook.objects.filter(book=book, user=request.user).exists():
        UserBook.objects.create(
            book=book,
            user=request.user,
            order=get_max_order(request.user)
        )

    books = UserBook.objects.filter(user=request.user)
    messages.success(request, f"Added {name} to book list")
    return render(request, 'partials/book-list.html', {'books': books})


@login_required
@require_http_methods(['DELETE'])
def delete_book(request, pk):
    UserBook.objects.get(pk=pk).delete()

    reorder(request.user)

    books = UserBook.objects.filter(user=request.user)
    return render(request, 'partials/book-list.html', {'books': books})


@login_required
def search_book(request):
    search_text = request.POST.get('search')

    userbooks = UserBook.objects.filter(user=request.user)
    results = Book.objects.filter(name__icontains=search_text).exclude(
        name__in=(userbooks.values_list('book__name', flat=True))
    )
    context = {"results": results}
    return render(request, 'partials/search-results.html', context)


def clear(request):
    return HttpResponse("")


def sort(request):
    book_pks_order = request.POST.getlist('book_order')
    books = []
    updated_books = []

    userbooks = UserBook.objects.prefetch_related('book').filter(user=request.user)
    for idx, book_pk in enumerate(book_pks_order, start=1):
        userbook = next(u for u in userbooks if u.pk == int(book_pk))

        if userbook.order != idx:
            userbook.order = idx
            updated_books.append(userbook)

        books.append(userbook)

    UserBook.objects.bulk_update(updated_books, ['order'])
    context = {'books': books}

    return render(request, 'partials/book-list.html', context)


@login_required
def detail(request, pk):
    userbook = get_object_or_404(UserBook, pk=pk)
    context = {'userbook': userbook}
    return render(request, 'partials/book-detail.html', context)


@login_required
def books_partial(request):
    books = UserBook.objects.filter(user=request.user)
    return render(request, 'partials/book-list.html', {'books': books})


@login_required
def upload_cover(request, pk):
    userbook = get_object_or_404(UserBook, pk=pk)
    cover = request.FILES.get('cover')
    userbook.book.cover.save(cover.name, cover)
    context = {'userbook': userbook}
    return render(request, 'partials/book-detail.html', context)
