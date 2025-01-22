from fastapi import FastAPI, Body

app = FastAPI()

books = [
    {'title': 'Fourth Wing', 'author': 'Rebecca Yaros', 'genre': 'Fantasy'},
    {'title': 'Iron Flame', 'author': 'Rebecca Yaros', 'genre': 'Fantasy'},
    {'title': 'Feel Good Food', 'author': 'Joe Wicks', 'genre': 'Food'},
    {'title': 'Didly Squat', 'author': 'Jeremy Clarkson', 'genre': 'Farming'},
    {'title': 'We Solve Murders', 'author': 'Richard Osman', 'genre': 'Murder'}
]

# for an overview of all the endpoints go to:
# http://127.0.0.1:8000/docs

# http://127.0.0.1:8000/books
@app.get(path="/books", description="returns all the books in the list")
async def get_books():
    return books

#   ----    ALWAYS MAKE SURE DYNAMIC PATHS COME AFTER FIXED PATHS   ----
# http://127.0.0.1:8000/books/Fourth%20Wing
@app.get(path="/books/Fourth Wing", description="returns Fourth Wing")
async def get_fourth_wing():
    return books[0]

#   ----    "%20" == " "   ----
# http://127.0.0.1:8000/books/Didly%20Squat
@app.get(path="/books/{book_title}",description="returns the specified book from {book_title}")
async def get_book(book_title: str = None):
    for book in books:
        if book_title == book['title']:
            return book
    return {
        "error": f"{book_title} not found, here is a list of available books:",
        "available_books": [book['title'] for book in books]
    }

#   ----    SEARCHES ARE CASE SENSITIVE, USING LOWERCASES WILL RETURN ERROR-CASE RESULTS   ----
# http://127.0.0.1:8000/books/search/?author=Rebecca%20Yaros
# http://127.0.0.1:8000/books/search/?category=Fantasy
@app.get(path="/books/search/", description="returns the book(s) that contain the same category OR author used in the search paramaters, ie {category} and {author}")
async def search_books_by_author_or_category(category: str = None, author: str = None):
    if category:
        books_to_return = [book for book in books if category == book['genre']]
        if not books_to_return:
            return {
                "error": f"Category '{category}' not found, here are the available categories:",
                "available_categories": list(set(book['genre'] for book in books))
            }
        return books_to_return
    
    if author:
        books_to_return = [book for book in books if author == book['author']]
        if not books_to_return:
            return {
                "error": f"Author '{author}' not found, here are the available authors:",
                "available_authors": list(set(book['author'] for book in books))
            }
        return books_to_return
    
    return {"error": "Please provide either a category or author parameter"}

# http://127.0.0.1:8000/books/search/Rebecca%20Yaros/?category=Fantasy
@app.get(path="/books/search/{book_author}/", description="returns the book(s) that contain the same category AND author used in the search paramaters, ie {category} and {book_author}")
async def search_books_by_author_and_category(category: str = None, book_author: str = None):
    if not category or not book_author:
        return {
            "error": "Please provide both category and author parameters",
            "available_categories": list(set(book['genre'] for book in books)),
            "available_authors": list(set(book['author'] for book in books))
        }
    
    books_to_return = [
        book for book in books 
        if category == book['genre'] and book_author == book['author']
    ]
    
    if books_to_return:
        return books_to_return
    return {
        "error": f"No books found with author '{book_author}' and category '{category}'",
        "available_combinations": list({
            f"{book['author']} - {book['genre']}"
            for book in books
        })
    }

# {"title": "A Brief History of Time", "author": "Stephen Hawking", "genre": "Science"}
@app.post(path="/books/create_book", description="creates a new book and adds this instance into the current list of books")
async def create_book(new_book=Body()):
    books.append(new_book)

@app.post(path="/books/update_book", description="used to update a book to the adjusted values, note the title must be the same")
async def update_book(updated_book=Body()):
    for i in range (len(books)):
        if books[i].get('title').casefold() == updated_book.get('title').casefold():
            books[i] = updated_book


    