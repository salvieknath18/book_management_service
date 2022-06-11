from services.book_service import get_book_by_genre


def get_genre_books(genre):
    return get_book_by_genre(genre)