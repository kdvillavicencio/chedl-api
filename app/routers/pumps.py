from fastapi import APIRouter
from typing import Literal
from pydantic import BaseModel, validator
from fluids import VFD_efficiency

from app.utils.validators import check_positive, check_normalized

# DOCS: https://fluids.readthedocs.io/index.html

class VFDData(BaseModel):
    power: int  # in W
    load: int = 1  # dimensionless

    positive = validator('power', allow_reuse=True)(check_positive)
    normalized = validator('load', allow_reuse=True)(check_normalized)    
    

router = APIRouter(
    prefix="/pumps"
)

@router.get("/")
async def pump_fn():
    return { "message":"Hello pumps!" }

@router.post("/vfd_eff")
async def get_vfd_perf(data: VFDData):
    """
    Returns VFD pump efficiency
    Refer to https://thermo.readthedocs.io/thermo.chemical.html

    """
    vfd_eff = VFD_efficiency(data.power, data.load)
    
    return { "efficiency":vfd_eff }
