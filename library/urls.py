from django.urls import path
from . import views

app_name = "library"

urlpatterns = [

    path('books/', views.BooksListView.as_view(), name='books_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_details'),
    path('books/new/', views.BookCreateView.as_view(), name='book_create'),
    path('books/edit/<int:pk>/', views.BookUpdateView.as_view(), name='book_edit'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
    path('authors/new/', views.AuthorCreateView.as_view(), name='author_create'),
    path('authors/<int:pk>/', views.AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/', views.AuthorsListView.as_view(), name='author_list'),
    path('books/<int:pk>/recommend/', views.RecommendBookView.as_view(), name='book_recommend'),
    path('books/<int:pk>/review/', views.ReviewBookView.as_view(), name='book_review'),
]