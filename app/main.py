from fastapi import FastAPI
from .routers import properties, pumps

app = FastAPI()

app.include_router(pumps.router)
app.include_router(properties.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}