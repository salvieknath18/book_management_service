from models.book import Book
import datetime


def add_book(book_data):
    book = Book(**book_data)
    book.save()
    return book.id


def update_book(obj_id, book_data):
    print(book_data)
    Book.objects.get(id=obj_id).update(**book_data)
    return Book.objects.get(id=obj_id)


def delete_book(obj_id):
    book = Book.objects.get(id=obj_id)
    book.delete()


def get_book(obj_id):
    return Book.objects.get(id=obj_id)


def get_book_by_isbn(isbn):
    return Book.objects.get(isbn=isbn)


def clean_book(book):
    book_data = dict()
    book_data["id"] = str(book.id)
    book_data["isbn"] = book.isbn
    book_data["title"] = book.title
    book_data["description"] = book.description
    book_data["genre"] = book.genre
    book_data["author"] = book.author
    book_data["year_published"] = datetime.datetime.strftime(book.year_published, "%d/%m/%Y")
    book_data["total_count"] = book.total_count
    book_data["available_count"] = book.available_count
    return book_data


def get_all_books():
    return Book.objects()


def clean_all_books(books):
    return [clean_book(book) for book in books]


def get_book_by_genre(genre):
    books = Book.objects.get(genre=genre)
    return books


def update_available_copy_count(book, updated_available_count):
    book.available_count = updated_available_count
    book_data = clean_book(book)
    book_data["year_published"] = datetime.datetime.strptime(book_data["year_published"], "%d/%m/%Y")
    book.update(**book_data)
    return book


def get_available_copy_count(isbn):
    book = Book.objects.get(isbn=isbn)
    available_copy_count = book.available_count
    return available_copy_count


def get_total_count(isbn):
    book = Book.objects.get(isbn=isbn)
    total_copy_count = book.total_count
    return total_copy_count


def increment_copy_count(book):
    available_count = book.available_count
    total_count = book.total_count
    if available_count >= total_count:
        raise Exception("Invalid Request to increment copy count")
    else:
        update_available_copy_count(book, available_count+1)


def decrement_copy_count(book):
    available_count = book.available_count
    if available_count <= 0:
        raise Exception("Invalid Request to decrement copy count")
    else:
        update_available_copy_count(book, available_count-1)


def sort_by_genre():
    books = get_all_books()
    genre_counter = dict()
    for book in books:
        genre = book.genre
        if genre in genre_counter:
            genre_counter[genre] += 1
        else:
            genre_counter[genre] = 1
    return [{"x": key, "y": value} for key, value in genre_counter.items()]
