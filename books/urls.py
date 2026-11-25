from django.urls import path
from . import views

# the namespace, so links are written like "books:book_list"
app_name = "books"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("books/", views.book_list, name="book_list"),
    # the same view again, but urls.py passes an extra option to it
    path("books/new/", views.book_list, {"only_new": True}, name="new_books"),
    path("books/search/", views.search, name="search"),
    path("books/suggest/", views.suggest_book, name="suggest_book"),
    path("books/<int:book_id>/", views.book_detail, name="book_detail"),
    path("books/<int:book_id>/json/", views.book_json, name="book_json"),
    # an old address that now sends people to the book list
    path("all-books/", views.old_book_list, name="old_book_list"),
]
