from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

import auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def status():
    return {"message": "Vote Service API is Working"}