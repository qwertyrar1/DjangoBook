from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Book, Author, Category, File
from .functions import search_feature_render, filter_feature_render
from django.core.cache import cache
from django.http import FileResponse


class IndexView(generic.ListView):
    paginate_by = 4
    model = Book
    template_name = 'books/index.html'
    context_object_name = 'latest_book_list'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'latest_book_list': Book.objects.order_by("-pub_date")[::-1],
            'categories': Category.objects.all(),
        })
        return context

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
        cache.set('temporary_query', search_query)

        return search_feature_render(request, search_query)
    else:
        return search_feature_render(request, cache.get('temporary_query'))


def filter_feature(request):
    if request.method == 'POST':
        filter_query = request.POST.getlist('filter_query')
        cache.set('temporary_query', filter_query)

        return filter_feature_render(request, filter_query)
    else:
        return filter_feature_render(request, cache.get('temporary_query'))


def download_file(request, file_id):
    file_instance = get_object_or_404(File, pk=file_id)
    file_path = file_instance.file_field.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)