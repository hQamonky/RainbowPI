#RainbowPI
This document describes the endpoints of the RainbowPI API.  
RainbowPI is a python web API that exposes commands to control an LED strip with a Raspberry PI.  
# Endpoints
All requests are `GET requests`.  
The values always go from 0 to 255.  
## Here is the list of endpoints  
### Display this document
- `/`  

### Turn on
- `/on`  

#### GET request  
Turn the LED strip on. The color will be the last color that was set. If the last color was 0,0,0 nothing will happen.    
*response*  
``` json
{
    "red": "255",
    "green": "255",
    "blue": "255"
}
```

### Turn off
- `/off`  

#### GET request  
Turn the LED strip off.  

### Handle RGB color using json
- `/rgb`  

#### GET request  
Get color as RGB.  
*response*  
``` json
{
    "red": "255",
    "green": "255",
    "blue": "255"
}
```

#### POST request  
Set color as RGB.  
*Body*  
``` json
{
    "red": "255",
    "green": "255",
    "blue": "255"
}
```
## Get color value  
These are all `GET` requests.  
- `/red` 
- `/green` 
- `/blue`   

## Set color value  
These are all `GET` requests, `value` can go from 0 to 255.  
- `/red/<value>` 
- `/green/<value>` 
- `/blue/<value>` 
