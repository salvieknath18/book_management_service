import datetime

from models.borrow import Borrow
from errors import InternalServerError
from services.book_service import increment_copy_count, decrement_copy_count
from services.user_service import get_user


def map_borrow_data_with_borrow_model(book, user="",
                                      status="", borrow_date="", return_date=None):
    # we can create meta pojo class for borrow model to get data
    borrow_model = dict()
    borrow_model['book'] = book
    borrow_model['user'] = user
    borrow_model['status'] = status
    borrow_model['borrow_date'] = borrow_date if borrow_date else datetime.datetime.now()
    borrow_model['return_date'] = return_date if return_date else \
        borrow_model['borrow_date'] + datetime.timedelta(days=30)
    return borrow_model


def add_entry(entry_data):
    entry = Borrow(**entry_data)
    entry.save()
    return entry


def update_entry(obj_id, entry_data):
    Borrow.objects.get(id=obj_id).update(**entry_data)
    entry = Borrow.objects.get(id=obj_id)
    return entry


def delete_entry(obj_id):
    book = Borrow.objects.get(id=obj_id)
    book.delete()


def get_entry(obj_id):
    return Borrow.objects.get(id=obj_id)


def clean_borrow_entry(borrow_entry):
    borrow_data = dict()
    borrow_data["id"] = str(borrow_entry.id)
    borrow_data["isbn"] = borrow_entry.isbn
    borrow_data["user"] = borrow_entry.user
    borrow_data["borrow_date"] = datetime.datetime.strftime(borrow_entry.borrow_date, "%d/%m/%Y  %H:%M:%S")
    borrow_data["return_date"] = datetime.datetime.strftime(borrow_entry.return_date, "%d/%m/%Y  %H:%M:%S")
    borrow_data["status"] = borrow_entry.status
    borrow_data["year_published"] = datetime.datetime.strftime(borrow_entry.borrow_date, "%d/%m/%Y")
    return borrow_data


def get_all_entries():
    return Borrow.objects()


def clean_all_entries(entries):
    return [clean_borrow_entry(entry) for entry in entries]


def borrow_book_copy(book, user):
    # create new entry in borrow collection
    borrow_model_data = map_borrow_data_with_borrow_model(book=book, user=user, status="B")
    try:
        decrement_copy_count(book)
    except Exception:
        raise InternalServerError("unable to update the entry")
    else:
        return add_entry(borrow_model_data)


def get_entry_id_from_book_snd_user(book, user):
    entries = Borrow.objects(book=book, user=user, status="B")
    valid_entry = entries[0]
    # To-Do Validate entry to update
    return valid_entry


def remove_book_copy(book, user):
    # update entry in borrow collection
    today = datetime.datetime.now()
    entry_to_update = get_entry_id_from_book_snd_user(book, user)
    try:
        increment_copy_count(book)
    except Exception:
        raise InternalServerError("unable to update the entry")
    else:
        borrow_model_data = map_borrow_data_with_borrow_model(book=book, user=user,
                                                              borrow_date=entry_to_update.borrow_date, status="R", return_date=today)
        entry_to_update.update(**borrow_model_data)


def book_borrowed_by_user(user_id):
    user = get_user(user_id)
    borrowed_entries = Borrow.objects(user=user, status="B")
    borrowed_books = list()
    for entry in borrowed_entries:
        borrowed_book = dict()
        borrowed_book["book_id"] = str(entry.book.id)
        borrowed_book["title"] = entry.book.title
        borrowed_book["borrow_date"] = datetime.datetime.strftime(entry.borrow_date, "%d/%m/%Y")
        borrowed_book["return_date"] = datetime.datetime.strftime(entry.return_date, "%d/%m/%Y")
        borrowed_books.append(borrowed_book)
    return borrowed_books
