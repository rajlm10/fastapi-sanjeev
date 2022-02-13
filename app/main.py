from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts,users,auth,votes
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Order of paths matters in case of conflict (FIFO)

@app.get("/")
def root():
    return {"message":"Welcome to the API service, go to https://rajsangani.xyz/docs to learn more"}


app.include_router(posts.router)

app.include_router(users.router)

app.include_router(auth.router)

app.include_router(votes.router)
