from django.contrib.auth.views import LogoutView
from django.urls import path

from tracker import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('current_books/', views.CurrentBooks.as_view(), name="current_books"),
    # path('completed_books', views.CompletedBooks.as_view(), name="completed-books")
    path('book_add/', views.BookAdd.as_view(), name="book_add")
]

htmx_views = [
    path('check_username/', views.check_username, name="check-username"),
    path('book_detail/<int:book_pk>/<str:book_type>/', views.book_detail, name="book_detail"),
    path('remove_book/<int:book_pk>/<str:book_type>/', views.remove_book, name="remove_book")
    # path('add_book/', views.add_book, name="add-book"),
    # path('delete_book/<int:pk>/', views.delete_book, name="delete-book"),
    # path('search-book/', views.search_book, name="search-book"),
    # path('clear/', views.clear, name="clear"),
    # path('sort/', views.sort, name="sort"),
    # path('book_list_partial', views.books_partial, name="book-list-partial"),
    # path('upload_cover/<int:pk>/', views.upload_cover, name="upload-cover")
]

urlpatterns += htmx_views
