# ChEDL Microservice
This project aims build a REST API Microservice to enable the use of ChEDL python library to languages outside python.

## API Documentation
### POST: `/properties/pure`
Returns properties of pure components

***Request Body***
| key | type | description |
|---|---|---|
| name | str | valid component names |
| T | float | (optional) temperature in K, defaults to 298.15K |
|  | array | (alternative) values of [min, max, #points] |
| P | float | (optional) pressure in Pa, defautls to 101325Pa |
|  | array | (alternative) values of [min, max, #points] |
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

POST http://localhost:8000/properties/pure
content-type: application/json
{
  "name": "hexane",
  "T": [100, 400, 8],
  "P": 200000
}
```

### POST: `/properties/mixture`
Returns properties of component mixture.

***Request Body***
| key | type | description |
|---|---|---|
| basis | * | * -> ['mole', 'mass', 'volgas', 'volliq'] |
| composition | dict | dict of component fractions where k:v -> name<str>: fraction<float> |
| T | float | (optional) temperature in K, defaults to 298.15K |
|  | array | (alternative) values of [min, max, #points] |
| P | float | (optional) pressure in Pa, defautls to 101325Pa |
|  | array | (alternative) values of [min, max, #points] |
| addprops | list | (optional) list of additional properties to be returned |

***Example***
```rest
POST http://localhost:8000/properties/mixture
content-type: application/json

{
  "T": 360,
  "P": 200000,
  "addprops": ["SG"],
  "basis": "volliq",
  "composition": {
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
  }
}
```

## Server Usage
To start the server using [uv](https://docs.astral.sh/uv/getting-started/installation/), run
```bash
uv run fastapi dev
```

To start the server using docker, run
```bash
docker compose up
```

The server is served on port 8000.

## References
- [ChEDL Thermo](https://github.com/CalebBell/thermo)
- [ChEDL Chemicals](https://github.com/CalebBell/chemicals)
