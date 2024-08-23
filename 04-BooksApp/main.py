# This APP is just for learning purpose
# all the business logics may not be correct.
# Applied Crud Operations using in-Memory


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id : UUID
    title : str = Field(min_length= 1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)


Books = []


@app.get("/")
def read_api():
    return {'Welcome': 'Eric'}


@app.post("/books")
def create_book(book: Book):
    Books.append(book)
    return book


@app.get("/books")
def get_books():
    return Books


@app.get("/{book_id}")
def get_books(book_id: UUID):

    for book in Books:
        if book.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : Does not exist"
    )


@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):

    for _ in Books:
        if _.id == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : Does not exist"
    )


@app.delete("/{book_id}")
def delete_book(book_id : UUID):

    for book in Books:
        if book.id == book_id:
            return "item is deleted"

    raise HTTPException(
        status_code=404,
        detail=f"ID {book_id} : Does not exist"
    )


