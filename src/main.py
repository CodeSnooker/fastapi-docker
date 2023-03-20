
import os
import redis
import uvicorn

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from dotenv import load

from src.models import Author
from src.models import Author as ModelAuthor
from src.models import Book
from src.models import Book as ModelBook
from src.schema import Book as SchemaBook, Author as SchemaAuthor


load('.env')


app = FastAPI()
r = redis.Redis(host="redis", port=6379)
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

@app.get("/")
def read_root():
    return {"message": "Hello World! Gudss Change #10"}

@app.get("/hits")
def hits():
    r.incr("hits")
    return {"message": r.get("hits")}


@app.post('/books', response_model=SchemaBook)
def add_book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id=book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.post("/authors/", response_model=SchemaAuthor)
def add_author(author: SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get("/books/")
def get_books():
    books = db.session.query(Book).all()

    return books

@app.get("/authors/")
def get_authors():
    authors = db.session.query(Author).all()

    return authors

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)