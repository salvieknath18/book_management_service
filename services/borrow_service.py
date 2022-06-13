import datetime

from models.borrow import Borrow
from errors import InternalServerError
from services.book_service import increment_copy_count, decrement_copy_count


def map_borrow_data_with_borrow_model(isbn, user=None,
                                      status=None, borrow_date=None, return_date=None):
    # we can create meta pojo class for borrow model to get data
    borrow_model = dict()
    borrow_model['isbn'] = isbn
    borrow_model['user'] = user
    borrow_model['status'] = status
    borrow_model['borrow_date'] = borrow_date if borrow_date else datetime.datetime.now()
    borrow_model['return_date'] = return_date
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


def borrow_book_copy(isbn, user):
    # create new entry in borrow collection
    borrow_model_data = map_borrow_data_with_borrow_model(isbn, user=user)
    try:
        add_entry(borrow_model_data)
    except Exception:
        raise InternalServerError("unable to update the entry")
    else:
        decrement_copy_count(isbn)


def get_entry_id_from_isbn_snd_user(isbn, user):
    entries = Borrow.objects.get(isbn=isbn, user=user)
    valid_entry = entries[0]
    # To-Do Validate entry to update
    return valid_entry


def remove_book_copy(isbn, user):
    # update entry in borrow collection
    borrow_model_data = map_borrow_data_with_borrow_model(isbn, user=user, return_date=datetime.datetime.now())
    entry_to_update = get_entry_id_from_isbn_snd_user(borrow_model_data['isbn'], borrow_model_data['user'])
    try:
        entry_to_update.update(**borrow_model_data)
    except Exception:
        raise InternalServerError("unable to update the entry")
    else:
        increment_copy_count(isbn)
