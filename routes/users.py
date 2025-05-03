from fastapi import APIRouter, HTTPException, Depends
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

from config.db import conn 
from config.jwt import create_access_token, verify_access_token
from models.model import users
from schemas.schema import User

user_router = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)

@user_router.post("/login", tags=["users"], description="Authenticate user and return JWT")
def login(username: str, password: str):
    user = conn.execute(users.select().where(users.c.username == username)).first()
    if not user or not f.decrypt(user.password.encode("utf-8")).decode("utf-8") == password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@user_router.get("/protected", tags=["users"], description="Protected route")
def protected_route(token: str = Depends(verify_access_token)):
    return {"message": "You have access to this route", "user": token}

@user_router.get("/users", tags=["users"], response_model=List[User], description="Get a list of all users", dependencies=[Depends(verify_access_token)])
def get_users():
    return conn.execute(users.select()).fetchall()

@user_router.get("/users/{id}", tags=["users"], response_model=User, description="Get a single user by Id", dependencies=[Depends(verify_access_token)])
def get_user(id: int):
    get_an_user = conn.execute(users.select().where(users.c.id == id)).first()
    if not get_an_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(get_an_user._mapping)

@user_router.post("/", tags=["users"], response_model=User, description="Create a new user")
def create_user(user: User):
    # Verificar si el username ya existe
    existing_user = conn.execute(users.select().where(users.c.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    # Crear un nuevo usuario
    new_user = {"username": user.username}
    new_user["password"] = f.encrypt(user.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    
    # Retornar el usuario creado
    created_user = conn.execute(users.select().where(users.c.id == result.lastrowid)).first()
    return dict(created_user._mapping)

@user_router.put("/users/{id}", tags=["users"], response_model=User, description="Update a User by Id", dependencies=[Depends(verify_access_token)])
def update_user(user: User, id: int):
    existing_user = conn.execute(users.select().where(users.c.id == id)).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Encriptar la contraseña
    user_password = user.password
    user_password_encrypted = f.encrypt(user_password.encode("utf-8"))
    
    # Actualizar el usuario
    result = conn.execute(
        users.update()
        .values(username=user.username, password=user_password_encrypted)
        .where(users.c.id == id)
    )
    
    # Verificar si se actualizó algún registro
    if result.rowcount == 0:
        return {"message": "Usuario no encontrado"}
    
    # Obtener el usuario actualizado
    updated_user = conn.execute(users.select().where(users.c.id == id)).first()
    if not updated_user:
        return {"message": "Error al recuperar el usuario actualizado"}
    
    return dict(updated_user._mapping)

@user_router.delete("/{id}", tags=["users"], status_code=HTTP_204_NO_CONTENT, dependencies=[Depends(verify_access_token)])
def delete_user(id: int):
    user_to_delete = conn.execute(users.select().where(users.c.id == id)).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    conn.execute(users.delete().where(users.c.id == id))
    return