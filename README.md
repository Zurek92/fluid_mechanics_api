# Fluid Mechanics API

### Run API in developer mode:
1. Developer config is required with structure similar to api/config/config_prod.py, example:
    ```python
    #!/usr/bin/env python3
    """Developer config."""
    class API:
        IP = "0.0.0.0"
        PORT = 12000
        CORS_ORIGIN = 'http://localhost:13000'
    ```
2. Run API (use one of):
    * With Docker:
    ```cd docker && docker-compose up```
    * With virtualenv: ```make venv && make run```


### Endpoints:
---
* GET **/health** <br>
     Check API health, example:
     ```bash
     curl -X GET localhost:5000/health
     ```

     Response:
     ```json
     {"status": "everything is ok :)"}
     ```

---
* POST **/calculate/headloss** <br>
    Calculate headloss in pipe, json structure required:

    ```json
    {
        "fluid": "string",
        "temperature": "integer",
        "temperature_supply": "integer",
        "temperature_return": "integer",
        "nominal_diameter": "integer",
        "material": "string",
        "flow": "float",
        "flow_unit": "string",
        "power": "float",
        "power_unit": "string",
        "length": "integer",
        "roughness": "float",
        "local_loss_coefficient": "float",
        "headloss_unit": "string"
    }
    ```
    * fluid: available fluids are listed below
    * temperature: fluid temperature, integer between 0 and 370 (only if flow is send)
    * temperature_supply: temperature supply, integer between 0 and 370 (only if power is send)
    * temperature_return: temperature return, integer between 0 and 370 (only if power is send)
    * nominal_diameter: nominal diameter depends on material
    * material: available materials: steel
    * flow: float, volume flow rate (requires: flow_unit, temperature)
    * flow_unit: flow unit e.g.: [m3/h], [m3/s] (only if flow is send)
    * power: power in heating or cooling installation (requires: temperature_supply, temperature_return, power_unit)
    * power_unit: power unit e.g.: [W], [kW], [kcal/h] (only if flow is send)
    * length: length of duct or pipe in meters [m]
    * roughness: optional, roughness of pipe in [mm]
    * local_loss_coefficient: optional, by default = 0
    * headloss_unit: optional, output headloss unit, by default = Pa

    Example request json, with flow:
    ```json
    {
        "fluid": "water",
        "temperature": 30,
        "nominal_diameter": 25,
        "material": "steel",
        "flow": 1,
        "flow_unit": "m3/h",
        "length": 10,
        "roughness": 1,
        "local_loss_coefficient": 15,
        "headloss_unit": "kPa"
    }
    ```
    Example response json:
    ```json
    {
      "headloss": 4.2991,
      "headloss_unit": "kPa",
      "velocity": 0.478,
      "velocity_unit": "m/s"
    }
    ```
    Example request json, with power:
    ```json
    {
        "fluid": "water",
        "temperature_supply": 80,
        "temperature_return": 50,
        "nominal_diameter": 25,
        "material": "steel",
        "power": 10,
        "power_unit": "kW",
        "length": 10,
        "roughness": 1,
        "local_loss_coefficient": 15
    }
    ```
    Example response json:
    ```json
    {
      "headloss": 363.16,
      "headloss_unit": "Pa",
      "velocity": 0.14,
      "velocity_unit": "m/s"
    }
    ```

---
* POST **/calculate/pipes** <br>
    Calculate headloss in pipe in various dimensions, responds headloss in Pa/m, json structure required:

    ```json
    {
        "fluid": "string",
        "temperature": "integer",
        "temperature_supply": "integer",
        "temperature_return": "integer",
        "material": "string",
        "flow": "float",
        "flow_unit": "string",
        "power": "float",
        "power_unit": "string",
        "roughness": "float"
    }
    ```
    * fluid: available fluids are listed below
    * temperature: fluid temperature, integer between 0 and 370 (only if flow is send)
    * temperature_supply: temperature supply, integer between 0 and 370 (only if power is send)
    * temperature_return: temperature return, integer between 0 and 370 (only if power is send)
    * material: available materials are listed below
    * flow: float, volume flow rate (requires: flow_unit, temperature)
    * flow_unit: flow unit e.g.: [m3/h], [m3/s] (only if flow is send)
    * power: power in heating or cooling installation (requires: temperature_supply, temperature_return, power_unit)
    * power_unit: power unit e.g.: [W], [kW], [kcal/h] (only if flow is send)
    * roughness: optional, roughness of pipe in [mm]

    Example request json, with flow:
    ```json
    {
        "fluid": "water",
        "temperature": 20,
        "material": "steel",
        "roughness": 1.5,
        "flow": 10,
        "flow_unit": "m3/h"
    }
    ```
    Example response json:
    ```json
    {
        "headloss_unit": "Pa/m",
        "results": [
            {"headloss": 16583000, "nominal_diameter": 8, "velocity": 45.7},
            {"headloss": 2304500, "nominal_diameter": 10, "velocity": 22.6},
            {"headloss": 582170, "nominal_diameter": 15, "velocity": 13.8},
            {"headloss": 111520, "nominal_diameter": 20, "velocity": 7.58},
            {"headloss": 31444, "nominal_diameter": 25, "velocity": 4.78},
            {"headloss": 6888.7, "nominal_diameter": 32, "velocity": 2.74},
            {"headloss": 3020.7, "nominal_diameter": 40, "velocity": 2.02},
            {"headloss": 837.22, "nominal_diameter": 50, "velocity": 1.26},
            {"headloss": 202.4, "nominal_diameter": 65, "velocity": 0.747},
            {"headloss": 85.285, "nominal_diameter": 80, "velocity": 0.542},
            {"headloss": 20.74, "nominal_diameter": 100, "velocity": 0.319},
            {"headloss": 6.7081, "nominal_diameter": 125, "velocity": 0.209},
            {"headloss": 2.5331, "nominal_diameter": 150, "velocity": 0.146},
        ],
        "velocity_unit": "m/s",
    }
    ```
    Example request json, with power:
    ```json
    {
        "fluid": "water",
        "temperature_supply": 80,
        "temperature_return": 50,
        "material": "steel",
        "roughness": 1,
        "power": 50,
        "power_unit": "kW"
    }
    ```
    Example response json:
    ```json
    {
        "headloss_unit": "Pa/m",
        "results": [
            {"headloss": 270970, "nominal_diameter": 8, "velocity": 6.68},
            {"headloss": 38673, "nominal_diameter": 10, "velocity": 3.31},
            {"headloss": 9877.1, "nominal_diameter": 15, "velocity": 2.02},
            {"headloss": 1929.6, "nominal_diameter": 20, "velocity": 1.11},
            {"headloss": 546.0, "nominal_diameter": 25, "velocity": 0.699},
            {"headloss": 120.77, "nominal_diameter": 32, "velocity": 0.401},
            {"headloss": 53.435, "nominal_diameter": 40, "velocity": 0.296},
            {"headloss": 15.032, "nominal_diameter": 50, "velocity": 0.184},
            {"headloss": 3.6404, "nominal_diameter": 65, "velocity": 0.109},
            {"headloss": 1.5644, "nominal_diameter": 80, "velocity": 0.0793},
            {"headloss": 0.37569, "nominal_diameter": 100, "velocity": 0.0467},
            {"headloss": 0.12359, "nominal_diameter": 125, "velocity": 0.0306},
            {"headloss": 0.047677, "nominal_diameter": 150, "velocity": 0.0214},
        ],
        "velocity_unit": "m/s",
    }
    ```

---
* POST **/calculate/gravity_flow** <br>
    Calculate gravity flow and velocity with manning equation, json structure required:

    ```json
    {
        "width": "float",
        "diameter": "float",
        "height": "float",
        "slope": "float",
        "manning_coefficient": "float"
    }
    ```
    * width: width of rectangular channel (only one width or diameter is required - XOR)
    * diameter: diameter of circular pipe (only one width or diameter is required - XOR)
    * height: height of water in open channel or pipe
    * slope: slope of the hydraulic grade line [-]
    * manning_coefficient: Gauckler–Manning coefficient

    Example request json:
    ```json
    {
        "diameter": 0.1,
        "height": 0.1,
        "slope": 0.05,
        "manning_coefficient": 0.013
    }
    ```
    Example response json:
    ```json
    {
        "velocity": 1.47,
        "velocity_unit": "m/s",
        "flow": 41.58,
        "flow_unit": "m3/h"
    }
    ```

---
### Available fluids:
1. water

### Available pipe materials:
1. steel
