from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.sql import select
from config.db import conn
from models.model import prestamos, books, users
from config.jwt import verify_access_token
from datetime import date

prestamos_router = APIRouter()


@prestamos_router.get("/prestamos", tags=["prestamos"], dependencies=[Depends(verify_access_token)])
def get_prestamos():
    result = conn.execute(prestamos.select()).fetchall()
    return [dict(row._mapping) for row in result]

@prestamos_router.post("/prestamos", tags=["prestamos"], dependencies=[Depends(verify_access_token)])
def create_prestamo(libro_id: int, usuario_id: int, devolver_en: date):
    # Verificar si el libro existe
    libro = conn.execute(select(books).where(books.c.id == libro_id)).first()
    if not libro:
        raise HTTPException(status_code=404, detail="El libro no existe")

    # Verificar si el usuario existe
    usuario = conn.execute(select(users).where(users.c.id == usuario_id)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    # Verificar si el libro está disponible
    if libro.disponible == 0:
        raise HTTPException(status_code=400, detail="El libro no está disponible")

    # Verificar que la fecha de devolución sea válida
    if devolver_en <= date.today():
        raise HTTPException(status_code=400, detail="La fecha de devolución debe ser posterior a la fecha actual")

    # Crear el préstamo
    conn.execute(prestamos.insert().values(
        libro_id=libro_id,
        usuario_id=usuario_id,
        prestado_en=date.today(),
        devolver_en=devolver_en
    ))

    # Marcar el libro como no disponible
    conn.execute(books.update().values(disponible=0).where(books.c.id == libro_id))

    return {"message": "Préstamo creado exitosamente"}

@prestamos_router.delete("/prestamos", tags=["prestamos"], dependencies=[Depends(verify_access_token)])
def delete_prestamo(libro_id: int, usuario_id: int):
    # Eliminar el préstamo
    conn.execute(prestamos.delete().where(
        (prestamos.c.libro_id == libro_id) & (prestamos.c.usuario_id == usuario_id)
    ))

    # Marcar el libro como disponible
    conn.execute(books.update().values(disponible=1).where(books.c.id == libro_id))

    return {"message": "Préstamo eliminado exitosamente"}