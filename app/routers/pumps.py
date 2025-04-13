from fastapi import APIRouter
from typing import Literal
from pydantic import BaseModel, PositiveFloat, field_validator
from fluids import VFD_efficiency

# DOCS: https://fluids.readthedocs.io/index.html

class VFDData(BaseModel):
    power: PositiveFloat  # in W
    load: int = 1  # dimensionless

    # positive = validator('power', allow_reuse=True)(check_positive)
    # normalized = validator('load', allow_reuse=True)(check_normalized)    
    
    @field_validator('load')
    def check_normalized(cls, v):
        if v < 0 or v > 1:
            raise ValueError(f"Load should be between 0 and 1.")
        return v

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
