# ChEDL-api
API Implementation of Chemical Engineering Design Library (ChEDL)

This project aims build a REST API Microservice to enable the use of ChEDL python library to languages outside python.

## API Documentation
#### POST: `/properties/pure`
Returns properties of pure components

| key | type | description |
|---|---|---|
| name | str | valid component names |
| T | float | (optional) temperature in K, defaults to 298.15K |
| P | float | (optional) pressure in Pa, defautls to 101325Pa |
| addprops | list | (optional) list of additional properties to be returned |

***Example***
```rest
POST http://localhost:8000/properties/pure
content-type: application/json

{
  "name": "toluene",
  "T": 360,
  "P": 200000
}
```
#### POST: `/properties/mixture`
Returns properties of component mixture.

| key | type | description |
|---|---|---|
| basis | * | * -> ['mole', 'mass', 'volgas', 'volliq'] |
| comp | dict | dict of component fractions where k:v -> name<str>: fraction<float> |
| T | float | (optional) temperature in K, defaults to 298.15K |
| P | float | (optional) pressure in Pa, defautls to 101325Pa |
| addprops | list | (optional) list of additional properties to be returned |

***Example***
```rest
POST http://localhost:8000/properties/mixture
content-type: application/json

{
  "addprops": ["SG"],
  "basis": "volliq",
  "comp": {
    "methane": 1.96522, 
    "nitrogen": 0.00259, 
    "carbon dioxide": 0.00596, 
    "ethane": 0.01819, 
    "propane": 0.0046, 
    "isobutane": 0.00098, 
    "butane": 0.00101, 
    "2-methylbutane": 0.00047, 
    "pentane": 0.00032, 
    "hexane": 0.00066
  },
  "T": 360,
  "P": 200000
}
```

## Server Usage
To start the server, run
```bash
uvicorn main:app --reload
```


## References
- [ChEDL Thermo](https://github.com/CalebBell/thermo)
- [ChEDL Chemicals](https://github.com/CalebBell/chemicals)