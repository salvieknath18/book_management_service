import datetime

from models.borrow import Borrow


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
    return entry.id


def update_entry(obj_id, entry_data):
    Borrow.objects.get(id=obj_id).update(**entry_data)
    return Borrow.objects.get(id=obj_id).to_json()


def delete_entry(obj_id):
    book = Borrow.objects.get(id=obj_id)
    book.delete()


def get_entry(obj_id):
    return Borrow.objects.get(id=obj_id).to_json()


def get_all_entries():
    return Borrow.objects().to_json()


def borrow_book_copy(isbn, user):
    # create new entry in borrow collection
    borrow_model_data = map_borrow_data_with_borrow_model(isbn, user=user)
    add_entry(borrow_model_data)


def get_entry_id_from_isbn_snd_user(isbn, user):
    entries = Borrow.objects.get(isbn=isbn, user=user)
    valid_entry = entries[0]
    return valid_entry


def remove_book_copy(isbn, user):
    # update entry in borrow collection
    borrow_model_data = map_borrow_data_with_borrow_model(isbn, user=user, return_date=datetime.datetime.now())
    entry_to_update = get_entry_id_from_isbn_snd_user(borrow_model_data['isbn'], borrow_model_data['user'])
    entry_to_update.update(**borrow_model_data)
