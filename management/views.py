from django.shortcuts import render
from management.models import MyUser, Book, Author


def index(request):
    state = None
    book_content = []
    author_content = []
    if request.method == 'POST':
        if request.POST['search_book']:
            search_title = request.POST.get('search_book', '')
            book_search_result = Book.objects.filter(title__iexact=search_title)
            for book in book_search_result:
                book_content_temp = {'book_info': book, 'authors_info': Author.objects.filter(book__title=book.title)}
                book_content.append(book_content_temp)
            state = 'search_book_success'
        elif request.POST['search_author']:
            search_name = request.POST.get('search_author', '')
            authors = Author.objects.filter(name__iexact=search_name)
            author_ids = authors.values('author_id')

            for i in range(len(authors)):
                author_content.append({
                    'author': authors[0],
                    'books': Book.objects.filter(author_ids__author_id__exact=author_ids[i]['author_id'])
                })
            state = 'search_author_success'
    else:
        book_recent = Book.objects.all().reverse()[:10]
        for book in book_recent:
            book_content_temp = {'book_info': book, 'authors_info': Author.objects.filter(book__title=book.title)}
            book_content.append(book_content_temp)
        author_content = Author.objects.all().order_by("-author_id")[:10]
        state = 'show_recent'

    content = {
        'active_menu': 'index',
        'state': state,
        'book_content': book_content,
        'author_content': author_content,
    }
    return render(request, 'management/index.html', content)


def add_author(request):
    state = None
    if request.method == 'POST':
        if Author.objects.all().exists():
            author_last = Author.objects.all().order_by('-author_id')[0]
            new_author_id = int(author_last.author_id) + 1
        else:
            new_author_id = 0
        new_author = Author(
            author_id=new_author_id,
            name=request.POST.get('name', ''),
            age=request.POST.get('age', 0),
            country=request.POST.get('country', ''),
        )
        new_author.save()
        state = 'success'
    content = {
        'active_menu': 'add_author',
        'state': state,
    }
    return render(request, 'management/add_author.html', content)


def show_authors(request):
    authors = Author.objects.all().order_by('name')

    content = {
        'active_menu': 'show_author',
        'authors': authors,
    }
    return render(request, 'management/show_authors.html', content)


def show_author_detail(request):
    state = None
    author_content = None
    if request.method == 'GET':
        operate = request.GET.get('operate', '')
        author_id = request.GET.get('author_id', '')
        if operate == 'delete':
            Author.objects.filter(author_id__exact=author_id).delete()
            state = 'delete success'
        else:
            author_search = Author.objects.filter(author_id__exact=author_id)
            if len(author_search) == 0:
                state = 'no such a author'
            else:
                author = author_search[0]
                book = Book.objects.filter(author_ids__author_id=author_id)
                author_content = {'author': author, 'book': book}
                state = 'success'

    content = {
        'active_menu': 'show author detail',
        'state': state,
        'author_content': author_content,
    }

    return render(request, 'management/show_author_detail.html', content)


def change_book_detail(request):
    state = None
    book_content = None
    if request.method == 'POST':
        operate = request.POST.get('operate', '')
        old_isbn = request.POST.get('isbn', '')
        if operate == 'send':
            book = Book.objects.filter(isbn__exact=old_isbn)
            authors = Author.objects.filter(book__isbn__exact=old_isbn)
            book_content = {'book': book, 'authors': authors}
            state = 'changing'
        else:
            book = Book.objects.get(isbn__exact=old_isbn)
            new_authors = request.POST.getlist('new_author_ids')
            book.author_ids.clear()
            for new_author in new_authors:
                book.author_ids.add(new_author)
            Book.objects.filter(isbn__exact=old_isbn).update(
                isbn=request.POST.get('isbn', ''),
                title=request.POST.get('title', ''),
                publisher=request.POST.get('publisher', ''),
                publish_date=request.POST.get('publish_date', ''),
                Price=request.POST.get('Price', 0),
            )
            state = 'success'

    content = {
        'active_menu': 'add_book',
        'state': state,
        'book_content': book_content,
    }

    return render(request, 'management/change_book_detail.html', content)


def change_author_detail(request):
    state = None
    author_content = None
    if request.method == 'POST':
        operate = request.POST.get('operate', '')
        author_id = request.POST.get('author_id', '')
        author = Author.objects.filter(author_id__exact=author_id)
        if operate == 'send':
            author_content = author
            state = 'changing'
        else:
            author.update(
                name=request.POST.get('new_name', ''),
                age=request.POST.get('new_age', ''),
                country=request.POST.get('new_country', ''),
            )
            author_content = author
            state = 'success'

    content = {
        'active_menu': 'add_book',
        'state': state,
        'author_content': author_content,
    }

    return render(request, 'management/change_author_detail.html', content)


def add_book(request):
    state = None
    if request.method == 'POST':
        new_book = Book(
            isbn=request.POST.get('isbn', ''),
            title=request.POST.get('title', ''),
            publisher=request.POST.get('publisher', ''),
            publish_date=request.POST.get('publish_date', ''),
            Price=request.POST.get('Price', 0),
        )
        new_book.save()
        a_ids = request.POST.getlist('a_ids')
        for a_id in a_ids:
            # author_temp = Author.objects.filter(author_id__exact=a_id)
            new_book.author_ids.add(a_id)
        state = 'success'

    author_list = Author.objects.all().order_by('name')

    content = {
        'active_menu': 'add_book',
        'author_list': author_list,
        'state': state,
    }

    return render(request, 'management/add_book.html', content)


def show_book(request):
    book_list = Book.objects.all().order_by('title')
    book_content = []

    for book in book_list:
        book_content_temp = {'book_info': book, 'authors_info': Author.objects.filter(book__title=book.title)}
        book_content.append(book_content_temp)

    content = {
        'active_menu': 'show_book',
        'book_content': book_content,
    }

    return render(request, 'management/show_book.html', content)


def show_book_detail(request):
    state = None
    book_content = None
    if request.method == 'GET':
        operate = request.GET.get('operate', '')
        book_isbn = request.GET.get('book_isbn', '')
        if operate == 'delete':
            Book.objects.filter(isbn__exact=book_isbn).delete()
            state = 'delete success'
        else:
            book_search = Book.objects.filter(isbn__iexact=book_isbn)
            if len(book_search) == 0:
                state = 'No such a book'
            else:
                book = book_search[0]
                authors = Author.objects.filter(book__isbn__exact=book_isbn)
                book_content = {'book': book, 'authors': authors}
                state = 'success'

    content = {
        'active_menu': 'show book detail',
        'state': state,
        'book_content': book_content,
    }

    return render(request, 'management/show_book_detail.html', content)





















