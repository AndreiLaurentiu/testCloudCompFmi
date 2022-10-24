from flask import Flask, abort, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from os import path

import books_management

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['SECRET_KEY'] = '7e36e770-1b6b-4fb5-b768-2397f4df9cf3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book/new', methods=['GET'])
def new_book():
    return render_template('new_book.html')

@app.route('/books', methods=['GET', 'POST'])
def book_list():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']
        pages = request.form['pages']
        image = request.files['image']

        if not title or not author or not publisher or not pages or not image or not image.filename or not allowed_file(image.filename):
            return abort(422, description="Invalid data")

        image_filename = secure_filename(image.filename)
        image.save(path.join(app.config['UPLOAD_FOLDER'], image_filename))

        books_management.add_book(
            title=title,
            author=author,
            publisher=publisher,
            pages=pages,
            image=image_filename
        )

    books = books_management.get_books()
    return render_template('book_list.html', books=books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
