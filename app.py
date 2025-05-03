from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.books import book_router
from routes.users import user_router
from routes.prestamos import prestamos_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://127.0.0.1:5500",  # Otra posible dirección local
    "http://localhost:8000",  # Si necesitas permitir el mismo backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista de orígenes permitidos
    allow_credentials=True,  # Permitir cookies o credenciales
    allow_methods=["*"],  # Métodos HTTP permitidos (GET, POST, etc.)
    allow_headers=["*"],  # Encabezados permitidos
)

# Rutas
app.include_router(book_router)
app.include_router(user_router)
app.include_router(prestamos_router)