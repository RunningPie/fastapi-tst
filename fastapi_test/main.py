from fastapi import FastAPI
from router_member import router_member

app = FastAPI()

@app.get("/")
async def hello() -> dict:
    return {"message": "Hello World",
            "guide": "go to fastapi-test-two.vercel.app/docs to see full documentation on what you can do with this simple fastapi app"}

app.include_router(router_member)
