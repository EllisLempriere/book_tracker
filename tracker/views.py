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
from tracker.forms import RegisterForm, NewBookForm
from tracker.models import ToReadBook, InProgressRead, Series, UserBook, FinishedRead
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


class CurrentBooks(LoginRequiredMixin, TemplateView):
    template_name = 'current-books.html'
    context_object_name = 'current_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["to_read"] = ToReadBook.objects.filter(user=self.request.user)
        context["in_progress"] = InProgressRead.objects.filter(user=self.request.user)
        return context


class CompletedBooks(LoginRequiredMixin, TemplateView):
    template_name = 'completed-books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["finished_books"] = FinishedRead.objects.filter(user=self.request.user)
        return context


class BookAdd(LoginRequiredMixin, FormView):
    form_class = NewBookForm
    template_name = 'book-add.html'
    success_url = reverse_lazy('book_add')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# HTMX
def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")


@login_required
def book_detail(request, book_pk, book_type):
    if book_type == 'to-read':
        user_book = get_object_or_404(ToReadBook, book_id=book_pk)
    elif book_type == 'in-progress':
        user_book = get_object_or_404(InProgressRead, book_id=book_pk)
    else:
        return

    finished_reads = FinishedRead.objects.filter(book_id=book_pk).filter(user=request.user)

    return render(request, 'partials/book-detail.html', {'user_book': user_book, 'finished_reads': finished_reads})


@login_required
@require_http_methods(['DELETE'])
def remove_book(request, book_pk, book_type):
    if book_type == 'to-read':
        ToReadBook.objects.get(book_id=book_pk, user=request.user).delete()
        reorder(request.user)
        books = ToReadBook.objects.filter(user=request.user)
        return render(request, 'partials/to-read-list.html', {'to-read': books})
    elif book_type == 'in-progress':
        InProgressRead.objects.get(book_id=book_pk, user=request.user).delete()
        books = InProgressRead.objects.filter(user=request.user)
        return render(request, 'partials/in-progress-list.html', {'in-progress': books})
    else:
        return


# @login_required
# def add_book(request):
#     title = request.POST.get('booktitle')
#
#     book = Book.objects.get_or_create(title=title)[0]
#
#     if not UserBook.objects.filter(book=book, user=request.user).exists():
#         UserBook.objects.create(
#             book=book,
#             user=request.user,
#             order=get_max_order(request.user)
#         )
#
#     books = UserBook.objects.filter(user=request.user)
#     messages.success(request, f"Added {title} to book list")
#     return render(request, 'partials/book-list.html', {'books': books})
#
#
# @login_required
# def search_book(request):
#     search_text = request.POST.get('search')
#
#     userbooks = UserBook.objects.filter(user=request.user)
#     results = Book.objects.filter(name__icontains=search_text).exclude(
#         name__in=(userbooks.values_list('book__title', flat=True))
#     )
#     context = {"results": results}
#     return render(request, 'partials/search-results.html', context)
#
#
# def clear(request):
#     return HttpResponse("")
#
#
# def sort(request):
#     book_pks_order = request.POST.getlist('book_order')
#     books = []
#     updated_books = []
#
#     userbooks = UserBook.objects.prefetch_related('book').filter(user=request.user)
#     for idx, book_pk in enumerate(book_pks_order, start=1):
#         userbook = next(u for u in userbooks if u.pk == int(book_pk))
#
#         if userbook.order != idx:
#             userbook.order = idx
#             updated_books.append(userbook)
#
#         books.append(userbook)
#
#     UserBook.objects.bulk_update(updated_books, ['order'])
#     context = {'books': books}
#
#     return render(request, 'partials/book-list.html', context)
#
#
# @login_required
# def books_partial(request):
#     books = UserBook.objects.filter(user=request.user)
#     return render(request, 'partials/book-list.html', {'books': books})
#
#
# @login_required
# def upload_cover(request, pk):
#     userbook = get_object_or_404(UserBook, pk=pk)
#     cover = request.FILES.get('cover')
#     userbook.book.cover.save(cover.name, cover)
#     context = {'userbook': userbook}
#     return render(request, 'partials/book-detail.html', context)
