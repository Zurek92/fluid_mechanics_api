# Fluid Mechanics API

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
        "velocity": 0.48,
        "velocity_unit": "m/s",
        "headloss": 4.335,
        "headloss_unit": "kPa"
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
        "local_loss_coefficient": 15,
    }
    ```
    Example response json:
    ```json
    {
        "headloss": 363.0,
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
        "velocity_unit": "m/s",
        "results": [
            {"nominal_diameter": 8, "headloss": 16561320, "velocity": 45.67},
            {"nominal_diameter": 10, "headloss": 2312644, "velocity": 22.64},
            {"nominal_diameter": 15, "headloss": 583861, "velocity": 13.82},
            {"nominal_diameter": 20, "headloss": 111520, "velocity": 7.58},
            {"nominal_diameter": 25, "headloss": 31444, "velocity": 4.78},
            {"nominal_diameter": 32, "headloss": 6889, "velocity": 2.74},
            {"nominal_diameter": 40, "headloss": 3021, "velocity": 2.02},
            {"nominal_diameter": 50, "headloss": 837, "velocity": 1.26},
            {"nominal_diameter": 65, "headloss": 204, "velocity": 0.75},
            {"nominal_diameter": 80, "headloss": 85, "velocity": 0.54},
            {"nominal_diameter": 100, "headloss": 21, "velocity": 0.32},
            {"nominal_diameter": 125, "headloss": 7, "velocity": 0.21},
            {"nominal_diameter": 150, "headloss": 3, "velocity": 0.15}
        ]
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
        "velocity_unit": "m/s",
        "results": [
            {"headloss": 270966.0, "nominal_diameter": 8, "velocity": 6.68},
            {"headloss": 38673.0, "nominal_diameter": 10, "velocity": 3.31},
            {"headloss": 9877.0, "nominal_diameter": 15, "velocity": 2.02},
            {"headloss": 1930.0, "nominal_diameter": 20, "velocity": 1.11},
            {"headloss": 548.0, "nominal_diameter": 25, "velocity": 0.7},
            {"headloss": 120.0, "nominal_diameter": 32, "velocity": 0.4},
            {"headloss": 55.0, "nominal_diameter": 40, "velocity": 0.3},
            {"headloss": 14.0, "nominal_diameter": 50, "velocity": 0.18},
            {"headloss": 4.0, "nominal_diameter": 65, "velocity": 0.11},
            {"headloss": 2.0, "nominal_diameter": 80, "velocity": 0.08},
            {"headloss": 0.0, "nominal_diameter": 100, "velocity": 0.05},
            {"headloss": 0.0, "nominal_diameter": 125, "velocity": 0.03},
            {"headloss": 0.0, "nominal_diameter": 150, "velocity": 0.02},
        ],
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
