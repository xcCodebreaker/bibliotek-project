from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.middleware.csrf import get_token
from django.utils.html import escape

# There is no database yet, so the books are kept in a normal Python list for now.
# Each book is a dictionary. This gets replaced by a real model later.
BOOKS = [
    {"id": 1, "title": "Python Crash Course", "author": "Eric Matthes", "year": 2019, "is_new": False},
    {"id": 2, "title": "Django for Beginners", "author": "William S. Vincent", "year": 2024, "is_new": True},
    {"id": 3, "title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "year": 2019, "is_new": False},
    {"id": 4, "title": "Learning Python", "author": "Mark Lutz", "year": 2013, "is_new": False},
    {"id": 5, "title": "Two Scoops of Django", "author": "Daniel Feldroy", "year": 2024, "is_new": True},
]


def find_book(book_id):
    # go through the list and return the book with this id, or None
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None


def menu():
    # links at the top of every page, built from the url names (not typed by hand)
    html = "<p>"
    html = html + '<a href="' + reverse("books:home") + '">Home</a> | '
    html = html + '<a href="' + reverse("books:book_list") + '">All books</a> | '
    html = html + '<a href="' + reverse("books:new_books") + '">New books</a> | '
    html = html + '<a href="' + reverse("books:suggest_book") + '">Suggest a book</a> | '
    html = html + '<a href="' + reverse("books:about") + '">About</a>'
    html = html + "</p><hr>"
    return html


def home(request):
    html = menu()
    html = html + "<h1>Welcome to Bibliotek</h1>"
    html = html + "<p>A small library website. Have a look at our books.</p>"
    html = html + '<form action="' + reverse("books:search") + '" method="get">'
    html = html + '<input type="text" name="q" placeholder="Search books"> '
    html = html + "<button type=\"submit\">Search</button></form>"
    return HttpResponse(html)


def about(request):
    html = menu()
    html = html + "<h1>About</h1>"
    html = html + "<p>Bibliotek is a practice project for learning Django.</p>"
    return HttpResponse(html)


def book_list(request, only_new=False):
    # only_new comes from urls.py (the extra dictionary in path())
    if only_new:
        title = "New books"
    else:
        title = "All books"

    html = menu()
    html = html + "<h1>" + title + "</h1><ul>"
    for book in BOOKS:
        if only_new and not book["is_new"]:
            continue
        link = reverse("books:book_detail", args=[book["id"]])
        html = html + '<li><a href="' + link + '">' + book["title"] + "</a> by " + book["author"] + "</li>"
    html = html + "</ul>"
    return HttpResponse(html)


def book_detail(request, book_id):
    # book_id comes from the url, for example /books/3/ gives book_id = 3
    book = find_book(book_id)
    if book is None:
        raise Http404("Book not found")

    html = menu()
    html = html + "<h1>" + book["title"] + "</h1>"
    html = html + "<p>Author: " + book["author"] + "</p>"
    html = html + "<p>Year: " + str(book["year"]) + "</p>"
    json_link = reverse("books:book_json", args=[book["id"]])
    html = html + '<p><a href="' + json_link + '">See this book as JSON</a></p>'
    return HttpResponse(html)


def book_json(request, book_id):
    book = find_book(book_id)
    if book is None:
        return JsonResponse({"error": "Book not found"}, status=404)
    return JsonResponse(book)


def search(request):
    # the search word comes from the query string, for example /books/search/?q=python
    query = request.GET.get("q", "")

    html = menu()
    # escape() stops people from putting their own HTML into the page
    html = html + "<h1>Search results for: " + escape(query) + "</h1><ul>"
    found = 0
    for book in BOOKS:
        if query.lower() in book["title"].lower() or query.lower() in book["author"].lower():
            link = reverse("books:book_detail", args=[book["id"]])
            html = html + '<li><a href="' + link + '">' + book["title"] + "</a></li>"
            found = found + 1
    html = html + "</ul>"
    if found == 0:
        html = html + "<p>No books found.</p>"
    return HttpResponse(html)


def suggest_book(request):
    # GET shows the form, POST means the form was sent
    if request.method == "POST":
        title = request.POST.get("title", "")
        html = menu()
        html = html + "<h1>Thank you!</h1>"
        html = html + "<p>We got your suggestion: " + escape(title) + "</p>"
        return HttpResponse(html)

    # Django needs a csrf token in every POST form (a safety check)
    token = get_token(request)
    html = menu()
    html = html + "<h1>Suggest a book</h1>"
    html = html + '<form method="post">'
    html = html + '<input type="hidden" name="csrfmiddlewaretoken" value="' + token + '">'
    html = html + '<input type="text" name="title" placeholder="Book title"> '
    html = html + '<button type="submit">Send</button></form>'
    return HttpResponse(html)


def old_book_list(request):
    # this page moved, so send the visitor to the new address
    return redirect("books:book_list")
