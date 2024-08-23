from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.config import database
from app.services import api

from app.services.auth import (
    models as models_auth
)
from app.services.tasks import (
    models as models_tasks
)

models_auth.Base.metadata.create_all(bind=database.engine)
models_tasks.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)