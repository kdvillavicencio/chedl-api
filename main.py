from fastapi import FastAPI
from pydantic import BaseModel
from thermo.chemical import Chemical

class Input(BaseModel):
    name: str
    T = 298.15
    P = 101325

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/properties/")
async def get_properties(input: Input):
    item = Chemical(input.name)
    item.calculate(T=input.T, P=input.P)
    properties = {
        "rho": item.rho,
        "mu": item.mu,
        "Cp": item.Cp,
    }
    return properties