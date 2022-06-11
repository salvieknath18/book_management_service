from models.book import Book


def add_book(book_data):
    book = Book(**book_data)
    book.save()
    return book.id


def update_book(obj_id, book_data):
    Book.objects.get(id=obj_id).update(**book_data)
    return Book.objects.get(id=obj_id).to_json()


def delete_book(obj_id):
    book = Book.objects.get(id=obj_id)
    book.delete()


def get_book(obj_id):
    return Book.objects.get(id=obj_id).to_json()


def get_all_books():
    return Book.objects().to_json()


def add_book_copy(obj_id):
    pass


def remove_book_copy(obj_id, copy_id):
    pass
