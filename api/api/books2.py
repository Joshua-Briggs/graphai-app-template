from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

router = APIRouter()

class book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published: int

    def __init__(self, id, title, author, description, rating, published):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published = published


class book_request(BaseModel):
    id: Optional[int] = Field(description="ID is not required on creation", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=10, max_length=80)
    rating: int = Field(gt=-1, lt=6)
    published: int = Field(gt=1000, lt=2026)

    model_config = {
        "json_schema_extra":
        {
            "example":
            {
                "title":"title of the book",
                "author":"author of the book",
                "description":"description of the book",
                "rating": 5,
                "published":2025
            }

        }
    }

books = [
    book(id=1, title="Fourth Wing", author="Rebecca Yaros", description="Fantasy novel", rating=5, published=2023),
    book(id=2, title="Iron Flame", author="Rebecca Yaros", description="Fantasy sequel", rating=4, published=2023),
    book(id=3, title="Feel Good Food", author="Joe Wicks", description="Cookbook", rating=4, published=2022),
    book(id=4, title="Didly Squat", author="Jeremy Clarkson", description="Farming adventures", rating=3, published=2021),
    book(id=5, title="We Solve Murders", author="Richard Osman", description="Murder mystery", rating=5, published=2022)
]

@router.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_from_id(book_id: int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"Book with id: {book_id} not found")

@router.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_book_by_publish_date(published: int = Query(gt=1000, lt=2026)):
    books_to_return = []
    for book in books:
        if book.published == published:
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail=f"Book(s) with publish date: {published} not found")
    return books_to_return

@router.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(rating: int = Query(gt=-1, lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == rating:
            books_to_return.append(book)
    if not books_to_return:
        raise HTTPException(status_code=404, detail=f"Book(s) with rating: {rating} not found")
    return books_to_return

@router.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books

@router.post("/books/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: book_request):
    new_book = book(**book_request.model_dump())
    books.append(find_book_id(new_book))

def find_book_id(book: book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book

@router.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: book_request):
    book_changed = False
    for i in range(len(books)):
        if books[i].id == book_request.id:
            books[i] = book_request
            book_changed = True
    if book_changed == True:
        raise HTTPException(status_code=404, detail=f"Book(s) with ID: {book_request.id} not found")

@router.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            book_changed = True
            break
    if book_changed == True:
        raise HTTPException(status_code=404, detail=f"Book(s) with ID: {book_request.id} not found")