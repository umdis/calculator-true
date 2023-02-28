from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules import boolean_algebra
from classes.operation import Operation

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"response": "Welcome to use free Algebra boolean calculator"}


@app.post("/formula")
def read_item(operation: Operation):
    response = boolean_algebra.writeTruthTable(operation.formula)
    return { "response": response }
