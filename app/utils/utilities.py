from typing import List, Tuple
from numpy import linspace

def normalize(comp: dict):
    compsum = sum(comp.values())
    factor = 1/compsum
    updated_values = list(map(lambda x: x*factor, comp.values()))
    return dict(zip(comp.keys(), updated_values))

def get_design_space(p, t) -> List[Tuple[float, float]]:
    if isinstance(p, tuple):    
        plist = linspace(p[0], p[1], p[2])
    elif isinstance(p, float|int):
        plist = [p]
    else:
        return 'Error'

    if isinstance(t, tuple):
        tlist = linspace(t[0], t[1], t[2])
    elif isinstance(t, float|int):
        tlist = [t]
    else:
        return 'Error'

    return [(x, y) for x in plist for y in tlist]

def get_prop_list(fluid, addprops, warnings):
    props = ['rho', 'mu', 'Cp']
    
    for prop in addprops:
        try: 
            getattr(fluid, prop)
            props.append(prop)
        except:
            warnings.append(f"Property '{prop}' does not exist.")

    return props

def get_prop_data(fluid, addprops, warnings):
    properties = {}
    DEFAULT_PROPS = ['T', 'P', 'rho', 'mu', 'Cp']

    for prop in DEFAULT_PROPS:
        properties[prop] = getattr(fluid, prop)
    
    for prop in addprops:
        try: 
            properties[prop] = getattr(fluid, prop)
        except:
            warnings.append(f"Property '{prop}' does not exist.")

    return properties
