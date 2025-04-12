from fastapi import APIRouter, HTTPException
# from typing import Literal, List
from typing import Literal, List, Union, Tuple, Dict
from pydantic import BaseModel, PositiveFloat, PositiveInt
from thermo import Chemical, Mixture

import app.utils.utilities as utils
from app.utils.validators import check_positive

P_default = 101325  # in Pa (abs)
T_default = 298.15  # in K

class BaseConditions(BaseModel):
    P: Union[Tuple[PositiveFloat, PositiveFloat, PositiveInt], PositiveFloat] = P_default
    T: Union[Tuple[PositiveFloat, PositiveFloat, PositiveInt], PositiveFloat] = T_default
    # T: PositiveFloat = 298.15  # in K
    # P: PositiveFloat = 101325  # in Pa (abs)
    addprops: List[str|None] = []

    # positive = validator('P', 'T', allow_reuse=True)(check_positive)

class PureComponent(BaseConditions):
    name: str

class MixedComponent(BaseConditions):
    basis: Literal['mole', 'mass', 'volgas', 'volliq']
    composition: Dict[str, PositiveFloat]


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
    properties = []
    warnings = []
        
    # check if fluid exists
    try:
        pure = Chemical(ID=fluid.name, T=T_default, P=P_default)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # initial property check
    prop_list = utils.get_prop_list(pure, fluid.addprops, warnings)
    
    # create data space
    design_space = utils.get_design_space(fluid.P, fluid.T)

    # run property estimate
    for (p,t) in design_space:
        pure = Chemical(ID=fluid.name, T=t, P=p)
        prop_data = utils.get_prop_data(pure, prop_list, warnings)
        properties.append(prop_data)        

    # response_body['properties'] = utils.get_properties(pure, fluid.addprops, warnings)

    if len(warnings) > 0:
        response_body['warnings'] = warnings
        
    response_body['properties'] = properties
    
    return response_body

@router.post("/mixture")
async def get_properties_mixture(fluid: MixedComponent):
    """
    Returns combined fluid properties of a mixture of components
    Refer to https://thermo.readthedocs.io/thermo.mixture.html

    """
    response_body = {}
    properties = []
    warnings = []

    comp_dict = {
        "mole": fluid.composition if fluid.basis == 'mole' else None,
        "mass": fluid.composition if fluid.basis == 'mass' else None,
        "volgas": fluid.composition if fluid.basis == 'volgas' else None,
        "volliq": fluid.composition if fluid.basis == 'volliq' else None
    }

    # check if fluid exists
    try:
        mixture = Mixture(ws=comp_dict["mass"], zs=comp_dict["mole"], Vfgs=comp_dict["volgas"], Vfls=comp_dict["volliq"], T=T_default, P=P_default)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # initial property check
    prop_list = utils.get_prop_list(mixture, fluid.addprops, warnings)
    
    # create data space
    design_space = utils.get_design_space(fluid.P, fluid.T)

    # run property estimate
    for (p, t) in design_space:
        mixture = Mixture(ws=comp_dict["mass"], zs=comp_dict["mole"], Vfgs=comp_dict["volgas"], Vfls=comp_dict["volliq"], T=t, P=p)
        prop_data = utils.get_prop_data(mixture, prop_list, warnings)
        properties.append(prop_data)        

    # mixture = Mixture(ws=comp_dict["mass"], zs=comp_dict["mole"], Vfgs=comp_dict["volgas"], Vfls=comp_dict["volliq"], T=fluid.T, P=fluid.P)
    # response_body['properties'] = utils.get_prop_data(mixture, fluid.addprops, warnings)
    
    if len(warnings) > 0:
        response_body['warnings'] = warnings

    response_body['properties'] = properties

    return response_body