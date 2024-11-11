from fastapi import FastAPI
from router_mahasiswa import router_mahasiswa

app = FastAPI()

@app.get("/")
async def hello() -> dict:
    return {"message": "Hello World"}

app.include_router(router_mahasiswa)
