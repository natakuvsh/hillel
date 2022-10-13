import sqlite3
from flask import Flask, render_template, request
from models import Book, Author

app = Flask(__name__)


def sqlite_connect(func):
    def connect(*args, **kwargs):
        connection = sqlite3.connect('library_db.sqlite3')
        result = func(connection, *args, **kwargs)
        connection.commit()
        connection.close()
        return result
    return connect




@sqlite_connect
@app.route('/', methods=['get'])
def all_books(connection):
    cursor = connection.cursor()
    books = cursor.execute("SELECT Book.id, Book.name, author.name FROM Book LEFT JOIN author ON author.id=Book.author")
    context = {'books': books.fetchall()}
    return render_template("book_list.html", **context)



@app.route('/add/book', methods=['get', 'post'])
def book_add():
    # context = {'authors': []}
    # with sqlite3.connect('library_db.sqlite3') as connection:
    #     cursor = connection.cursor()
    #     authors = cursor.execute("SELECT id, name, pseudonim FROM author")
    #     context['authors'] = authors.fetchall()
    #
    # if request.method == 'POST':
    #     with sqlite3.connect('library_db.sqlite3') as connection:
    #         cursor = connection.cursor()
    #         cursor.execute(f"INSERT INTO Book(name, year, author) VALUES ('{request.form['name']}', {request.form['year']}, {request.form['author']})")
    #         connection.commit()

    context = {'authors': Author.select()}
    if request.method == 'POST':
        Book(
            name=request.form['name'],
            year=request.form['year'],
            author=request.form['author']
            # **request.form
        ).save()

    return render_template('add_book.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
