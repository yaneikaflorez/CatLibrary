from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean
from config.db import meta, engine

books = Table ("books", meta,
                Column("id", Integer, primary_key = True, autoincrement= True),
                Column("name", String(255)),
                Column("isbn", String(255)),
                Column("editorial", String(255)),
                Column("autor", String(255)),
                Column("disponible", Boolean, default=True))  # Nueva columna

users = Table ("users", meta,
               Column("id", Integer, primary_key = True, autoincrement= True),
               Column("username", String(12)),
               Column("password", String(255)))

prestamos = Table("prestamos", meta,
                Column("libro_id", Integer, ForeignKey("books.id"), primary_key=True),
                Column("usuario_id", Integer, ForeignKey("users.id"), primary_key=True),
                Column("prestado_en", Date),
                # fecha en formato YYYY-MM-DD
                Column("devolver_en", Date)) 

meta.create_all(engine)