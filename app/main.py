from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="RIPIS Backend")

app.include_router(endpoints.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "RIPIS Backend is running"}
