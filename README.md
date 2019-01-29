# Fluid Mechanics API

### Endpoints:
* GET **/health** <br>
     Check API health, example:
     ```bash
     curl -X GET localhost:5000/health
     ```

     Response:
     ```json
     {"status": "everything is ok :)"}
     ```

* POST **/calculate/headloss** <br>
    Calculate headloss in pipe, json structure required:

    ```json
    {
        "fluid": "string",
        "temperature": "integer",
        "nominal_diameter": "integer",
        "material": "string",
        "flow": "float",
        "flow_unit": "string",
        "length": "integer",
        "roughness": "float",
        "local_loss_coefficient": "float",
        "headloss_unit": "string"
    }
    ```
    * fluid: available fluids are listed below
    * temperature: fluid temperature, integer between 0 and 370
    * nominal_diameter: nominal diameter depends on material
    * material: available materials: steel
    * flow: float, volume flow rate
    * flow_unit: flow unit e.g.: [m3/h], [m3/s]
    * length: length of duct or pipe in meters [m]
    * roughness: optional, roughness of pipe in [mm]
    * local_loss_coefficient: optional, by default = 0
    * headloss_unit: optional, output headloss unit, by default = Pa

    Example request json:
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

* POST **/calculate/pipes** <br>
    Calculate headloss in pipe in various dimensions, responds headloss in Pa/m, json structure required:

    ```json
    {
        "fluid": "string",
        "temperature": "integer",
        "material": "string",
        "flow": "float",
        "flow_unit": "string",
        "roughness": "float"
    }
    ```
    * fluid: available fluids are listed below
    * temperature: fluid temperature, integer between 0 and 370
    * material: available materials are listed below
    * flow: float, volume flow rate
    * flow_unit: flow unit e.g.: [m3/h], [m3/s]
    * roughness: optional, roughness of pipe in [mm]

    Example request json:
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

### Available fluids:
1. water

### Available pipe materials:
1. steel
