from .models import Book, Author, Category
from django.core.paginator import Paginator
from itertools import chain
from django.shortcuts import render


def search_feature_render(request, query):
    book_search = Book.objects.filter(name__icontains=query)
    author_search_id = Author.objects.filter(fullname__icontains=query)
    author_search = Book.objects.filter(author__in=author_search_id)
    objects = list(chain(book_search.order_by("-pub_date")[::-1], author_search.order_by("-pub_date")[::-1]))

    page_number = request.GET.get("page")
    paginator = Paginator(objects, 4)
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/index.html', {'query': query,
                                                'page_obj': page_obj,
                                                'categories': Category.objects.all(),
                                                })


def filter_feature_render(request, query):
    all_books = Book.objects.order_by("-pub_date")[::-1]
    category_filter = []
    for book in all_books:
        for category in query:
            if category not in book.book_categories():
                break
        else:
            category_filter.append(book)
    if not query:
        category_filter = all_books
    page_number = request.GET.get("page")
    paginator = Paginator(category_filter, 4)
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/index.html', {'query': query,
                                                'page_obj': page_obj,
                                                'categories': Category.objects.all(),
                                                'name_of_checked': query,
                                                })