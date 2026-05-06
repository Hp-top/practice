from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, projects, tasks

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title="hp-top API", version="1.0.0")

# CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки, в продакшене задать конкретные
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "hp-top API is running. See /docs for interactive documentation."}