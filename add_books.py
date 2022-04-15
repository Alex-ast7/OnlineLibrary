import requests
from data import db_session
from isbn_books import books
from data.books import Books

db_session.global_init('db/onlineLibrary.db')

dbsess = db_session.create_session()

for i in books:
    try:
        data = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={i}').json()
        title = data['items'][0]['volumeInfo']['title']
        description = data['items'][0]['volumeInfo']['description']
        author = ', '.join(data['items'][0]['volumeInfo']['authors'])
        isbn_13 = data['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
        isbn_10 = data['items'][0]['volumeInfo']['industryIdentifiers'][1]['identifier']
        genre = ', '.join(data['items'][0]['volumeInfo']['categories'])
        image_link = data['items'][0]['volumeInfo']['imageLinks']['thumbnail']
        language = data['items'][0]['volumeInfo']['language']
        add = Books(title=title, author=author, description=description, isbn_13=isbn_13, isbn_10=isbn_10, genre=genre, image_link=image_link, language=language)
        dbsess.add(add)
        dbsess.commit()
    except Exception:
        pass