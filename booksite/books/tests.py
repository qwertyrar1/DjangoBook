from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from .models import Book, Category, Author
from .functions import search_feature_render, filter_feature_render
from django.core.paginator import Paginator
from django.core.files.uploadedfile import SimpleUploadedFile


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Категория 1")
        self.category2 = Category.objects.create(name="Категория 2")

        self.author1 = Author.objects.create(fullname="Автор 1")
        self.author2 = Author.objects.create(fullname="Автор 2")

        image_file1 = SimpleUploadedFile("image1.jpg", b"file_content", content_type="image/jpeg")
        image_file2 = SimpleUploadedFile("image2.jpg", b"file_content", content_type="image/jpeg")

        self.book1 = Book.objects.create(
            name="Книга 1",
            description="Описание книги 1",
            pub_date=timezone.now(),
            author=self.author1,
            download_links=["http://example.com/book1.pdf"],
            image=image_file1
        )
        self.book1.categories.add(self.category1)

        self.book2 = Book.objects.create(
            name="Книга 2",
            description="Описание книги 2",
            pub_date=timezone.now(),
            author=self.author2,
            download_links=["http://example.com/book2.pdf"],
            image=image_file2
        )
        self.book2.categories.add(self.category2)

    def test_index_view(self):
        response = self.client.get(reverse('books:book'))
        self.assertEqual(response.status_code, 200)

        self.assertQuerysetEqual(
            response.context['latest_book_list'],
            [self.book1, self.book2],
            ordered=False
        )
        self.assertQuerysetEqual(
            response.context['categories'],
            [self.category1, self.category2],
            ordered=False
        )


class FeatureRenderViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.category1 = Category.objects.create(name="Категория 1")
        self.category2 = Category.objects.create(name="Категория 2")

        self.author = Author.objects.create(fullname="Тестовый Автор")
        self.image_file = SimpleUploadedFile("image.jpg", b"file_content", content_type="image/jpeg")

        for i in range(20):
            book = Book.objects.create(
                name=f"Книга {i}",
                description=f"Описание книги {i}",
                download_links=["http://example.com/book.pdf"],
                pub_date=timezone.now(),
                author=self.author,
                image=self.image_file,
            )
            if i % 2 == 0:
                book.categories.add(self.category1)
            else:
                book.categories.add(self.category2)

    def test_search_render(self):
        request = self.factory.get(reverse('books:search-view'))
        response = search_feature_render(request, '')

        self.assertEqual(response.status_code, 200)

        for page_number in range(1, 6):
            request = self.factory.get(reverse('books:search-view') + f'?page={page_number}')
            response = search_feature_render(request, '')

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, f'Книга {(page_number - 1) * 4}')

    # books:filter-view
    def test_filter_render(self):
        request = self.factory.get(reverse('books:filter-view'), {'query': ['Категория 1', ]})
        response = filter_feature_render(request, ['Категория 1', ])

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Книга 0')
        self.assertNotContains(response, 'Книга 1')

        self.assertContains(response, 'Page 1 of 3')




