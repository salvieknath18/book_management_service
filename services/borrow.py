from models.borrow import Borrow


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


def borrow_book_copy(copy_id):
    pass


def remove_book_copy(copy_id):
    pass
