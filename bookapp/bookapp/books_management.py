from json import dumps, loads

def add_book(title, author, publisher, pages, image):
    books = get_books()
    new_book = {
        'title': title,
        'author': author,
        'publisher': publisher,
        'pages': pages,
        'image': image
    }
    books[len(books)] = new_book

    with open('books.json', 'wt') as f:
        f.write(dumps(books, indent=4))

    return len(books) - 1

def get_books():
    try:
        with open('books.json', 'rt') as f:
            books = loads(f.read())
            return books
    except FileNotFoundError:
        return {}
