from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path("", views.IndexView.as_view(), name="book"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("author/<int:author_id>", views.author, name="author"),
    path("search/", views.search_feature, name="search-view"),
    path("filter/", views.filter_feature, name="filter-view"),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]