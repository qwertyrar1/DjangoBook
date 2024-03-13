from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from .models import Book, Author
from itertools import chain


class IndexView(generic.ListView):
    paginate_by = 4
    model = Book
    template_name = 'books/index.html'
    context_object_name = 'latest_book_list'

    def get_queryset(self):
        return Book.objects.order_by("-pub_date")[::-1]


class DetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    author_books = Book.objects.filter(author_id=author_id)
    context = {
        "author": author,
        "author_books": author_books,
    }
    return render(request, 'books/author.html', context)


def search_feature(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']

        book_search = Book.objects.filter(name__icontains=search_query)
        author_search_id = Author.objects.filter(fullname__icontains=search_query)
        author_search = Book.objects.filter(author__in=author_search_id)
        objects = list(chain(book_search, author_search))

        page_number = request.GET.get("page")
        paginator = Paginator(objects, 4)
        page_obj = paginator.get_page(page_number)

        return render(request, 'books/index.html', {'query': search_query, 'page_obj': page_obj})
    else:
        return render(request, 'books/index.html', {})

