from fastapi import APIRouter
from typing import Literal
from pydantic import BaseModel, validator, root_validator
from thermo import Chemical, Mixture

import app.utils.utilities as utils
from app.utils.validators import check_positive

class BaseConditions(BaseModel):
    T = 298.15  # in K
    P = 101325  # in Pa (abs)
    addprops = []

    positive = validator('P', 'T', allow_reuse=True)(check_positive)

class PureComponent(BaseConditions):
    name: str

class MixedComponent(BaseConditions):
    basis: Literal['mole', 'mass', 'volgas', 'volliq']
    comp: dict


router = APIRouter(
    prefix="/properties"
)

@router.get("/")
async def pump_fn():
    return { "message":"Hello properties!" }

@router.post("/pure")
async def get_properties_pure(fluid: PureComponent):
    """
    Returns fluid properties of a pure componenet
    Refer to https://thermo.readthedocs.io/thermo.chemical.html

    """
    response_body = {}
    warnings = []

    pure = Chemical(ID=fluid.name, T=fluid.T, P=fluid.P)
    response_body['properties'] = utils.get_properties(dir(Chemical), pure, fluid.addprops, warnings)
    
    if len(warnings) > 0:
        response_body['warnings'] = warnings
    
    return response_body

@router.post("/mixture")
async def get_properties_mixture(fluid: MixedComponent):
    """
    Returns combined fluid properties of a mixture of components
    Refer to https://thermo.readthedocs.io/thermo.mixture.html

    """
    response_body = {}
    warnings = []

    comp_dict = {
        "mole": fluid.comp if fluid.basis == 'mole' else None,
        "mass": fluid.comp if fluid.basis == 'mass' else None,
        "volgas": fluid.comp if fluid.basis == 'volgas' else None,
        "volliq": fluid.comp if fluid.basis == 'volliq' else None
    }

    mixture = Mixture(ws=comp_dict["mass"], zs=comp_dict["mole"], Vfgs=comp_dict["volgas"], Vfls=comp_dict["volliq"], T=fluid.T, P=fluid.P)
    response_body['properties'] = utils.get_properties(dir(Mixture), mixture, fluid.addprops, warnings)
    
    if len(warnings) > 0:
        response_body['warnings'] = warnings

    return response_body