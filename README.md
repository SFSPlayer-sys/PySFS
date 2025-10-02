# PySFS - Python SFS Control Library

A Python library for controlling Spaceflight Simulator (SFS) through the SFSControl mod API.

## Features

- **Complete SFS Control**: Control rockets, staging, throttle, rotation, and more
- **Information Retrieval**: Get rocket status, orbital data, planet information
- **Value Extraction**: Direct access to altitude, longitude, velocity, and other parameters  
- **Calculation Tools**: Built-in trajectory prediction, impact point calculation
- **Multi-Rocket Support**: Control multiple rockets simultaneously
- **Type Safety**: Full type annotations for better development experience

## Installation

Currently, this package is not yet published to PyPI. You can install it locally:

```bash
# Clone or download the PySFS directory
# Navigate to the PySFS directory
cd path/to/PySFS

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

Alternatively, you can copy the PySFS folder to your project and import it directly:

```python
# If PySFS folder is in your project directory
from PySFS import SFSClient
```

## Requirements

- Spaceflight Simulator with SFSControl mod installed
- Python 3.7+
- `requests` library (automatically installed)

## Quick Start

```python
from PySFS import SFSClient

# Connect to SFS
sfs = SFSClient()

# Basic rocket control
sfs.set_throttle(1.0)           # Full throttle
sfs.rotate("Prograde")          # Point prograde
sfs.stage()                     # Stage separation
sfs.set_main_engine_on(True)    # Engine on

# Get rocket information
altitude = sfs.values_api.rocket_altitude()
longitude = sfs.values_api.rocket_longitude()
velocity = sfs.calc_api.rocket_velocity_magnitude()

print(f"Altitude: {altitude}m")
print(f"Longitude: {longitude}°")
print(f"Velocity: {velocity}m/s")
```

### Simple Example: Get Rocket Longitude

```python
from PySFS import SFSClient
sfs = SFSClient()
lon = sfs.values_api.rocket_longitude()
print(lon)
```

## API Structure

### Core Components

- **`SFSClient`**: Main client class combining all functionality
- **`HttpClient`**: Low-level HTTP communication
- **`ControlAPI`**: Rocket control commands
- **`InfoAPI`**: Information retrieval endpoints
- **`ValuesAPI`**: Direct value extraction
- **`CalcAPI`**: Calculation and prediction tools

### Control Commands

```python
# Rotation Control
sfs.rotate("Prograde")          # Prograde direction
sfs.rotate("Surface")           # Radial direction  
sfs.rotate("Target")            # Point to target
sfs.rotate(90.0)                # Custom angle (degrees)
sfs.rotate("Prograde", 180.0)   # Retrograde (prograde + 180°)

# Engine Control
sfs.set_throttle(0.75)          # 75% throttle
sfs.set_main_engine_on(True)    # Engine on/off
sfs.set_rcs(True)               # RCS on/off

# Staging & Parts
sfs.stage()                     # Next stage
sfs.use_part(part_id)           # Activate specific part

# Navigation
sfs.set_target("Moon")          # Set target
sfs.clear_target()              # Clear target
```

### Information Retrieval

```python
# Rocket Data
rocket_data = sfs.info_api.rocket_sim()        # Simulation data
rocket_save = sfs.info_api.rocket_save()       # Save data
rockets = sfs.info_api.rockets()               # All rockets

# Planet Data  
planet = sfs.info_api.planet("Earth")          # Specific planet
planets = sfs.info_api.planets()               # All planets

# Mission Data
mission = sfs.info_api.mission()               # Mission info
version = sfs.info_api.version()               # Mod version (returns {"name": "SFSControl", "version": "1.2"})
```

### Direct Value Access

```python
# Position & Motion
altitude = sfs.values_api.rocket_altitude()
longitude = sfs.values_api.rocket_longitude()
position = sfs.values_api.rocket_position()
rotation = sfs.values_api.rocket_rotation()

# Orbital Elements
orbit = sfs.values_api.rocket_orbit()
apoapsis = sfs.values_api.rocket_orbit_apoapsis()
periapsis = sfs.values_api.rocket_orbit_periapsis()
period = sfs.values_api.rocket_orbit_period()

# Control Status
throttle = sfs.values_api.rocket_throttle()
rcs_status = sfs.values_api.rocket_rcs_on()

# Planet Properties
planet_radius = sfs.values_api.planet_radius("Earth")
planet_gravity = sfs.values_api.planet_gravity("Earth")

# Mod Information
mod_version = sfs.values_api.sfscontrol_version()    # "1.2"
mod_name = sfs.values_api.sfscontrol_name()          # "SFSControl"
```

### Calculations

```python
# Velocity Analysis
velocity_info = sfs.calc_api.rocket_velocity_info()
velocity_magnitude = sfs.calc_api.rocket_velocity_magnitude()
velocity_direction = sfs.calc_api.rocket_velocity_direction()

# Trajectory Prediction
impact_point = sfs.calc_api.impact_point(
    rocket_x=x, rocket_y=y,
    vel_x=vx, vel_y=vy, 
    planet_radius=radius,
    gravity=gravity
)

# Orbital Mechanics
orbit_info = sfs.calc_api.rocket_orbit_info()
angle_info = sfs.calc_api.rocket_angle_info()
```


## Configuration

### Connection Settings

```python
# Default connection
sfs = SFSClient()  # localhost:27772

# Custom connection  
sfs = SFSClient(host="192.168.1.100", port=27772)

# Custom timeout
sfs = SFSClient(timeout_seconds=30.0)

# Custom session
import requests
session = requests.Session()
sfs = SFSClient(session=session)
```

### Multi-Rocket Control

```python
# Control specific rocket
sfs.set_throttle(1.0, rocket="Rocket1")
sfs.rotate("Prograde", rocket="Rocket1")

# Get data for specific rocket
altitude = sfs.values_api.rocket_altitude(rocket="Rocket1")
```

## Error Handling

```python
try:
    sfs = SFSClient()
    altitude = sfs.values_api.rocket_altitude()
    
except requests.ConnectionError:
    print("Cannot connect to SFS. Make sure SFSControl mod is running.")
    
except requests.Timeout:
    print("Request timed out. SFS may be unresponsive.")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## SFSControl Mod Setup

1. Install the SFSControl mod in Spaceflight Simulator
2. Launch SFS and load a world with rockets
3. The mod will start an HTTP server on `localhost:27772`
4. Use PySFS to connect and control your rockets

## Supported Rotation Modes

- `"Prograde"` - Velocity direction
- `"Surface"` - Radial direction (towards surface)
- `"Target"` - Point towards selected target  
- `"None"` - Disable rotation control
- `"Default"` - Disable SAS
- Custom angles: `90.0`, `180.0`, etc.

## Planet Codes

- `"Earth"` - Earth
- `"Moon"` - Moon  
- `"Mars"` - Mars
- `"Phobos"` - Phobos
- `"Deimos"` - Deimos
- And more...

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License.

## Acknowledgments

- SFSControl mod developers for providing the HTTP API
- Spaceflight Simulator community
- Contributors and testers

## Related Repositories

- **PySFS Library**: [https://github.com/SFSPlayer-sys/PySFS](https://github.com/SFSPlayer-sys/PySFS) - The main PySFS library repository
- **SFSControl Scripts**: [https://github.com/SFSPlayer-sys/SFSControl-_-Scripts](https://github.com/SFSPlayer-sys/SFSControl-_-Scripts) - Collection of scripts using PySFS
- **SFSControl Mod**: [https://github.com/SFSPlayer-sys/SFSControl](https://github.com/SFSPlayer-sys/SFSControl) - The SFSControl mod for Spaceflight Simulator

## Links

- [Spaceflight Simulator](https://spaceflight-simulator.fandom.com/)
- [SFS Community](https://www.reddit.com/r/SpaceflightSimulator/)
