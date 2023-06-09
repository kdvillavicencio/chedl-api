def normalize(comp: dict):
    compsum = sum(comp.values())
    factor = 1/compsum
    updated_values = list(map(lambda x: x*factor, comp.values()))
    return dict(zip(comp.keys(), updated_values))

def get_properties(class_props, fluid, addprops, warnings):
    print(fluid)
    properties = {}
    DEFAULT_PROPS = ['rho', 'mu', 'Cp']

    for prop in DEFAULT_PROPS:
        properties[prop] = getattr(fluid, prop)
    
    for prop in addprops:
        if prop in class_props:
            properties[prop] = getattr(fluid, prop)
        else:
            warnings.append(f"Property '{prop}' does not exist.")

    return properties
