from fastapi import FastAPI
from .routes import process

app = FastAPI()

# Inclui as rotas
app.include_router(process.router)
