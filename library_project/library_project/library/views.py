from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Reader

@login_required
@permission_required('library.view_book', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})
# Для списка читателей – требуем право view_reader (которого у группы «Читатели» нет)
@login_required
@permission_required('library.view_reader', raise_exception=True)
def reader_list(request):
    readers = Reader.objects.all()
    return render(request, 'library/reader_list.html', {'readers': readers})

# Для детальной информации о читателе – тоже требуем view_reader
@login_required
@permission_required('library.view_reader', raise_exception=True)
def reader_detail(request, pk):
    reader = get_object_or_404(Reader, pk=pk)
    return render(request, 'library/reader_detail.html', {'reader': reader})
from django.shortcuts import render
from .models import Book

def all_books(request):
    books = Book.objects.all()
    return render(request, 'library/all_books.html', {'books': books})

def available_books(request):
    books = Book.objects.filter(is_available=True)
    return render(request, 'library/available_books.html', {'books': books})
