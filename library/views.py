from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .forms import BookForm, AuthorForm

from library.models import Book, Author
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .services import BookService


class ReviewBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        if not request.user.has_perm('library.can_review_book'):
            return HttpResponseForbidden('У вас нет прав для рецензирования книги.')

        # Логика рецензирования книги
        book.review = request.POST.get('review')
        book.save()

        return redirect('library:book_details', pk=pk)


class RecommendBookView(LoginRequiredMixin, View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)

        if not request.user.has_perm('library.can_recommend_book'):
            return HttpResponseForbidden('У вас нет прав для рекомендации книги.')

        # Логика рекомендации книги
        book.recommend = True
        book.save()

        return redirect('library:book_details', pk=pk)


# @method_decorator(cache_page(60 * 15), name='dispatch')
class BooksListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Book
    template_name = 'library/books_list.html'
    context_object_name = 'books'
    permission_required = 'library.view_book'

    def get_queryset(self):
        return Book.objects.filter(publication_date__year__gt=1000)


class BookCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.add_book'


# @method_decorator(cache_page(60 * 15), name='dispatch')
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'library/book_details.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['author_books_count'] = Book.objects.filter(author=self.object.author).count()
        print(context)
        book_id = self.object.id
        context['average_rating'] = BookService.calculate_average_rating(book_id)
        context['is_popular'] = BookService.is_popular(book_id)

        return context


class BookUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/book_form.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.change_book'


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    template_name = 'library/book_confirm_delete.html'
    success_url = reverse_lazy('library:books_list')
    permission_required = 'library.delete_book'


class AuthorCreateView(CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author_list')


class AuthorUpdateView(UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'library/author_form.html'
    success_url = reverse_lazy('library:author_list')


class AuthorsListView(ListView):
    model = Author
    template_name = 'library/author_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        queryset = cache.get('authors_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('authors_queryset', queryset, 60 * 15)
        return queryset
