from fastapi import APIRouter, Depends
from fastapi import HTTPException
from config.db import conn 
from config.jwt import verify_access_token
from models.model import books
from schemas.schema import Book

book_router = APIRouter()

@book_router.get("/books", dependencies=[Depends(verify_access_token)], tags=["books"])
def get_books():
    all_books = conn.execute(books.select()).fetchall()
    books_list = [dict(book._mapping) for book in all_books]
    return books_list

@book_router.get("/books/{id}", dependencies=[Depends(verify_access_token)], tags=["books"])
def get_book(id: int):
    get_a_book = conn.execute(books.select().where(books.c.id == id)).first()
    if not get_a_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return dict(get_a_book._mapping)

@book_router.post("/books", dependencies=[Depends(verify_access_token)], tags=["books"])
def create_books(book: Book):
    new_book = book.dict()
    new_book.pop("id", None)
    
    # Se carga en la base de datos
    result = conn.execute(books.insert().values(new_book))
    
    # Validar que se cargó correctamente
    if not result.inserted_primary_key:
        return {"message": "Error al crear el libro"}
    
    # Retorna el libro creado
    created_book_id = result.inserted_primary_key[0]
    created_book = conn.execute(books.select().where(books.c.id == created_book_id)).first()

    if created_book is None:
        return {"message": "Error al recuperar el libro creado"}
    
    return dict(created_book._mapping)

@book_router.put("/books/{id}", dependencies=[Depends(verify_access_token)], tags=["books"])
def update_books(id: int, book: Book):
    existing_book = conn.execute(books.select().where(books.c.id == id)).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    conn.execute(books.update().values(
        name=book.name,
        isbn=book.isbn,
        editorial=book.editorial,
        autor=book.autor,
        disponible=book.disponible
    ).where(books.c.id == id))
    updated_book = conn.execute(books.select().where(books.c.id == id)).first()
    return dict(updated_book._mapping)

@book_router.delete("/books/{id}", dependencies=[Depends(verify_access_token)], tags=["books"])
def delete_books(id: int):
    # Obtener el libro antes de eliminarlo
    book_to_delete = conn.execute(books.select().where(books.c.id == id)).first()
    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # Convertir el libro a un diccionario
    deleted_book = dict(book_to_delete._mapping)

    # Eliminar el libro
    conn.execute(books.delete().where(books.c.id == id))

    # Retornar los datos del libro eliminado
    return deleted_book