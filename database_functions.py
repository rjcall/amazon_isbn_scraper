
import sqlite3
from get_all_isbns import get_isbns
import json

# sql function
def push_book(book):
    conn = sqlite3.connect('books.db')
    command = "INSERT INTO books VALUES ('%s','%s','%s','%s','%s')" %(book['title'].replace("'",""), book['price'], book['isbn'], book['url'], book['date'])
    conn.execute(command)
    conn.commit()
    conn.close()

def create_json(u):
    u = get_isbns()
    isbns = {}
    for s in u:
        isbns[s] = []
    with open('books.json', 'w') as file:
        j = json.dumps(isbns)
        file.write(j)

    print('json written')

def load_json():
    with open('books.json', 'r') as file:
        isbns = json.load(file)
        print(isbns)
    return isbns



def add_price(book, book_dict):
    book_dict[book['isbn']].append(book)
    print(book_dict)