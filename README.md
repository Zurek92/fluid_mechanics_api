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
        "headloss_unit": "string",
    }
    ```
    * fluid: available fluids: water
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
        "headloss_unit": "kPa",
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
