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

# Take screenshot
screenshot_data = sfs.screenshot()  # Returns bytes

# Draw visualization
sfs.draw_api.clear()  # Clear previous drawings
sfs.draw_api.circle(center=(0, 0), radius=100, color=[1.0, 0.0, 0.0, 1.0])  # Red circle
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
- **`DrawAPI`**: Drawing and visualization tools

### Control Commands

```python
# Basic Control
sfs.set_throttle(0.75)                    # Set throttle (0.0-1.0)
sfs.set_main_engine_on(True)              # Engine on/off
sfs.set_rcs(True)                         # RCS on/off
sfs.stage()                               # Next stage
sfs.use_part(part_id)                     # Activate specific part

# Rotation Control
sfs.rotate("Prograde")                    # Prograde direction
sfs.rotate("Surface")                     # Radial direction  
sfs.rotate("Target")                      # Point to target
sfs.rotate("None")                        # Disable rotation control
sfs.rotate("Default")                     # Disable SAS
sfs.rotate(90.0)                          # Custom angle (degrees)
sfs.rotate("Prograde", 180.0)             # Retrograde (prograde + 180°)
sfs.stop_rotate()                         # Stop rotation
sfs.set_rotation(45.0)                    # Set rotation angle
sfs.rcs_thrust("up", 2.0)                 # RCS thrust in direction for seconds

# Navigation & Targets
sfs.set_target("Moon")                    # Set target
sfs.clear_target()                        # Clear target

# Rocket Management
sfs.launch()                              # Launch rocket
sfs.switch_rocket("Rocket1")              # Switch to rocket
sfs.rename_rocket("Rocket1", "NewName")   # Rename rocket
sfs.delete_rocket("Rocket1")              # Delete rocket
sfs.create_rocket("Earth", blueprint_json, "RocketName", x, y, vx, vy, vr)

# Scene Management
sfs.build(blueprint_info)                 # Build from blueprint
sfs.clear_blueprint()                     # Clear blueprint
sfs.switch_to_build()                     # Switch to build scene
sfs.clear_debris()                        # Clear debris

# Advanced Control
sfs.add_stage(index, part_ids)            # Add stage
sfs.remove_stage(index)                   # Remove stage
sfs.set_orbit(radius, eccentricity, true_anomaly, counterclockwise, planet_code)
sfs.set_state(x, y, vx, vy, angular_velocity, blueprint_json)

# Fuel Management
sfs.transfer_fuel(from_tank_id, to_tank_id)  # Transfer fuel between tanks
sfs.stop_fuel_transfer()                     # Stop fuel transfer

# Vehicle Control
sfs.wheel_control(enable=True, turn_axis=0.5)  # Control wheels

# Time & Map Control
sfs.set_timewarp(speed=5.0, realtime_physics=False, show_message=True)  # Set time warp
sfs.timewarp_plus()                          # Increase time warp
sfs.timewarp_minus()                         # Decrease time warp
sfs.switch_map_view(on=True)                 # Switch map view
sfs.track("Moon")                            # Track object
sfs.unfocus()                                # Stop tracking

# Game Management
sfs.set_cheat("InfiniteFuel", True)          # Enable/disable cheats
sfs.revert("Launch")                         # Revert to launch/VAB
sfs.complete_challenge("challenge_id")       # Complete challenge
sfs.wait_for_window("Apoapsis", 100.0)       # Wait for orbital window
sfs.show_toast("Message")                    # Show toast notification
sfs.log_message("Info", "Log message")       # Log message
sfs.quicksave_manager("Save", "SaveName")    # Manage quicksaves
sfs.set_map_icon_color("#FF0000")            # Set rocket map icon color

# Information Queries
sfs.get_rocket_info()                        # Get rocket information
sfs.get_rocket_list()                        # Get list of rockets
sfs.get_world_info()                         # Get world information

# Custom Commands
sfs.control("MethodName", arg1, arg2)        # Direct method call
sfs.call("MethodName", [arg1, arg2])         # Call with args list
sfs.custom("MethodName", arg1, arg2)         # Custom method call
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

# Other Data
other = sfs.info_api.other()                   # Miscellaneous info
mission = sfs.info_api.mission()               # Mission info
debug_log = sfs.info_api.debug_log()           # Debug log
version = sfs.info_api.version()               # Mod version (returns {"name": "SFSControl", "version": "1.2"})
```

### Direct Value Access

```python
# Basic Rocket Info
name = sfs.values_api.rocket_name()                  # Rocket name
rocket_id = sfs.values_api.rocket_id()               # Rocket ID

# Position & Motion
altitude = sfs.values_api.rocket_altitude()          # Altitude above surface
longitude = sfs.values_api.rocket_longitude()        # Longitude (0-360°)
position = sfs.values_api.rocket_position()          # Position {x, y}
rotation = sfs.values_api.rocket_rotation()          # Rotation angle
angular_velocity = sfs.values_api.rocket_angular_velocity()  # Angular velocity

# Control Status
throttle = sfs.values_api.rocket_throttle()          # Throttle (0.0-1.0)
rcs_status = sfs.values_api.rocket_rcs_on()          # RCS on/off

# Orbital Elements
orbit = sfs.values_api.rocket_orbit()                # Full orbit data
apoapsis = sfs.values_api.rocket_orbit_apoapsis()    # Apoapsis altitude
periapsis = sfs.values_api.rocket_orbit_periapsis()  # Periapsis altitude
period = sfs.values_api.rocket_orbit_period()        # Orbital period
true_anomaly = sfs.values_api.rocket_orbit_true_anomaly()  # True anomaly
parent_planet = sfs.values_api.rocket_parent_planet_code()  # Current planet

# Other Rocket Data
target_angle = sfs.values_api.other_target_angle()   # Target angle
quicksaves = sfs.values_api.other_quicksaves()       # Quicksave list
nav_target = sfs.values_api.other_nav_target()       # Navigation target
timewarp_speed = sfs.values_api.other_timewarp_speed()  # Time warp speed
world_time = sfs.values_api.other_world_time()       # World time
scene_name = sfs.values_api.other_scene_name()       # Current scene
mass = sfs.values_api.other_mass()                   # Rocket mass
thrust = sfs.values_api.other_thrust()               # Current thrust
max_thrust = sfs.values_api.other_max_thrust()       # Maximum thrust
twr = sfs.values_api.other_twr()                     # Thrust-to-weight ratio
dist_to_apoapsis = sfs.values_api.other_dist_to_apoapsis()    # Distance to apoapsis
dist_to_periapsis = sfs.values_api.other_dist_to_periapsis()  # Distance to periapsis
time_to_apoapsis = sfs.values_api.other_time_to_apoapsis()    # Time to apoapsis
time_to_periapsis = sfs.values_api.other_time_to_periapsis()  # Time to periapsis
transfer_window_delta_v = sfs.values_api.other_transfer_window_delta_v()  # Transfer window ΔV
mission_status = sfs.values_api.other_mission_status()        # Mission status
inertia_info = sfs.values_api.other_inertia_info()           # Inertia information

# Planet Properties
planet_radius = sfs.values_api.planet_radius("Earth")        # Planet radius
planet_gravity = sfs.values_api.planet_gravity("Earth")      # Surface gravity
planet_soi = sfs.values_api.planet_soi("Earth")              # Sphere of influence
has_atmosphere = sfs.values_api.planet_has_atmosphere("Earth")  # Has atmosphere
atmosphere_height = sfs.values_api.planet_atmosphere_height("Earth")  # Atmosphere height
planet_parent = sfs.values_api.planet_parent("Moon")         # Parent planet
planet_orbit = sfs.values_api.planet_orbit("Earth")          # Planet orbit data
planet_eccentricity = sfs.values_api.planet_orbit_eccentricity("Earth")  # Orbit eccentricity
planet_semi_major_axis = sfs.values_api.planet_orbit_semi_major_axis("Earth")  # Semi-major axis
planet_argument_of_periapsis = sfs.values_api.planet_orbit_argument_of_periapsis("Earth")  # Argument of periapsis
planet_current_true_anomaly = sfs.values_api.planet_orbit_current_true_anomaly("Earth")  # Current true anomaly
planet_current_radius = sfs.values_api.planet_orbit_current_radius("Earth")  # Current orbital radius
planet_current_velocity = sfs.values_api.planet_orbit_current_velocity("Earth")  # Current orbital velocity

# Mod Information
mod_version = sfs.values_api.sfscontrol_version()     # "1.2"
mod_name = sfs.values_api.sfscontrol_name()           # "SFSControl"
mod_full_info = sfs.values_api.sfscontrol_full_info() # Full version info
```

### Calculations

```python
# Velocity Analysis
velocity_magnitude = sfs.calc_api.rocket_velocity_magnitude()     # Speed (m/s)
velocity_direction = sfs.calc_api.rocket_velocity_direction()     # Direction (degrees)
velocity_components = sfs.calc_api.rocket_velocity_components()   # {vx, vy}
velocity_info = sfs.calc_api.rocket_velocity_info()              # Complete velocity info

# Orbital Calculations
orbit_period = sfs.calc_api.rocket_orbit_period()                # Orbital period (seconds)
orbit_info = sfs.calc_api.rocket_orbit_info()                    # Complete orbital info

# Angle Calculations
normal_angle = sfs.calc_api.rocket_normal_angle()                # Normal angle (degrees)
position_angle = sfs.calc_api.rocket_position_angle()            # Position angle (degrees)
angle_info = sfs.calc_api.rocket_angle_info()                    # Complete angle info

# Trajectory Prediction
impact_point = sfs.calc_api.impact_point(
    rocket_x=x, rocket_y=y,        # Current position
    vel_x=vx, vel_y=vy,            # Current velocity
    planet_radius=radius,          # Planet radius
    gravity=gravity,               # Surface gravity
    dt=0.02,                       # Time step (optional)
    max_steps=100000               # Max simulation steps (optional)
)  # Returns {"x": impact_x, "y": impact_y} or None
```

### Drawing API

The DrawAPI provides powerful visualization capabilities for drawing geometric shapes and lines in the SFS world. All coordinates are in world coordinates (not screen coordinates), and colors are specified as [r,g,b,a] with values from 0.0 to 1.0.

```python
# Access the drawing API
draw = sfs.draw_api

# Clear all drawn objects
draw.clear()

# Basic Drawing Functions

# Draw a line between two points
draw.line(
    start=(100, 200),              # Start point (x, y) or (x, y, z)
    end=(300, 400),                # End point (x, y) or (x, y, z)
    color=[1.0, 0.0, 0.0, 1.0],   # Red color [r,g,b,a]
    width=2.0,                     # Line width (optional)
    sorting=0.0,                   # Drawing order (optional)
    layer=0.0                      # Layer depth (optional)
)

# Draw a circle (outline only)
draw.circle(
    center=(500, 300),             # Center point (x, y)
    radius=50.0,                   # Circle radius
    color=[0.0, 1.0, 0.0, 1.0],   # Green color [r,g,b,a]
    resolution=32,                 # Circle smoothness (min 8, optional)
    sorting=0.0,                   # Drawing order (optional)
    layer=0.0                      # Layer depth (optional)
)

# Draw a regular polygon (outline)
draw.regular_polygon(
    center=(200, 200),             # Center point (x, y)
    radius=75.0,                   # Polygon radius
    sides=6,                       # Number of sides (triangle=3, square=4, etc.)
    color=[0.0, 0.0, 1.0, 1.0],   # Blue color [r,g,b,a]
    width=3.0,                     # Line width (optional)
    sorting=0.0,                   # Drawing order (optional)
    layer=0.0,                     # Layer depth (optional)
    rotation_deg=45.0              # Rotation in degrees (optional)
)

# Draw a rectangle (outline or filled)
draw.rect(
    p0=(100, 100),                 # First corner (x, y) or (x, y, z)
    p1=(200, 200),                 # Opposite corner (x, y) or (x, y, z)
    color=[1.0, 1.0, 0.0, 1.0],   # Yellow color [r,g,b,a]
    sorting=0.0,                   # Drawing order (optional)
    layer=0.0,                     # Layer depth (optional)
    filled=False,                  # True for filled, False for outline
    fill_axis="x"                  # Fill direction: "x" or "y" (for filled=True)
)

# Draw a rectangle outline (alternative method)
draw.rect_outline(
    p0=(300, 300),                 # First corner (x, y) or (x, y, z)
    p1=(400, 400),                 # Opposite corner (x, y) or (x, y, z)
    color=[1.0, 0.0, 1.0, 1.0],   # Magenta color [r,g,b,a]
    width=2.0,                     # Line width (optional)
    sorting=0.0,                   # Drawing order (optional)
    layer=0.0                      # Layer depth (optional)
)
```

#### Drawing API Examples

```python
# Example 1: Draw a trajectory path
def draw_trajectory(sfs, points, color=[1.0, 0.5, 0.0, 1.0]):
    """Draw a trajectory path connecting multiple points"""
    draw = sfs.draw_api
    for i in range(len(points) - 1):
        draw.line(
            start=points[i],
            end=points[i + 1],
            color=color,
            width=2.0
        )

# Example 2: Draw a landing zone indicator
def draw_landing_zone(sfs, center_x, center_y, radius=100):
    """Draw a circular landing zone indicator"""
    draw = sfs.draw_api
    # Outer circle (warning zone)
    draw.circle(
        center=(center_x, center_y),
        radius=radius,
        color=[1.0, 0.0, 0.0, 0.5],  # Semi-transparent red
        resolution=32
    )
    # Inner circle (safe zone)
    draw.circle(
        center=(center_x, center_y),
        radius=radius * 0.5,
        color=[0.0, 1.0, 0.0, 0.5],  # Semi-transparent green
        resolution=32
    )

# Example 3: Draw a grid for reference
def draw_reference_grid(sfs, center_x, center_y, size=1000, spacing=100):
    """Draw a reference grid around a center point"""
    draw = sfs.draw_api
    half_size = size // 2
    
    # Vertical lines
    for x in range(center_x - half_size, center_x + half_size + 1, spacing):
        draw.line(
            start=(x, center_y - half_size),
            end=(x, center_y + half_size),
            color=[0.5, 0.5, 0.5, 0.3],  # Semi-transparent gray
            width=1.0
        )
    
    # Horizontal lines
    for y in range(center_y - half_size, center_y + half_size + 1, spacing):
        draw.line(
            start=(center_x - half_size, y),
            end=(center_x + half_size, y),
            color=[0.5, 0.5, 0.5, 0.3],  # Semi-transparent gray
            width=1.0
        )

# Example 4: Draw orbital indicators
def draw_orbit_indicators(sfs, planet_center, orbit_radius):
    """Draw orbital indicators around a planet"""
    draw = sfs.draw_api
    
    # Main orbit circle
    draw.circle(
        center=planet_center,
        radius=orbit_radius,
        color=[0.0, 0.8, 1.0, 0.8],  # Cyan orbit line
        resolution=64,
        width=2.0
    )
    
    # Draw cardinal direction markers
    directions = [
        (orbit_radius, 0),      # East
        (-orbit_radius, 0),     # West
        (0, orbit_radius),      # North
        (0, -orbit_radius)      # South
    ]
    
    for dx, dy in directions:
        x, y = planet_center[0] + dx, planet_center[1] + dy
        draw.circle(
            center=(x, y),
            radius=10,
            color=[1.0, 1.0, 0.0, 1.0],  # Yellow markers
            resolution=16
        )

# Example 5: Clear and redraw based on rocket position
def update_rocket_trail(sfs):
    """Update rocket trail visualization"""
    draw = sfs.draw_api
    
    # Clear previous trail
    draw.clear()
    
    # Get current rocket position
    pos = sfs.values_api.rocket_position()
    x, y = pos["x"], pos["y"]
    
    # Draw current position marker
    draw.circle(
        center=(x, y),
        radius=20,
        color=[1.0, 0.0, 0.0, 1.0],  # Red current position
        resolution=16
    )
    
    # Draw velocity vector
    velocity = sfs.calc_api.rocket_velocity_components()
    vx, vy = velocity["vx"], velocity["vy"]
    
    # Scale velocity vector for visualization
    scale = 10.0
    end_x, end_y = x + vx * scale, y + vy * scale
    
    draw.line(
        start=(x, y),
        end=(end_x, end_y),
        color=[0.0, 1.0, 0.0, 1.0],  # Green velocity vector
        width=3.0
    )
```

#### Drawing API Notes

- **Coordinates**: All coordinates are in world coordinates (meters), not screen pixels
- **Colors**: Use RGBA format with values from 0.0 to 1.0 (e.g., `[1.0, 0.0, 0.0, 1.0]` for red)
- **Persistence**: Drawn objects remain visible until `clear()` is called
- **Performance**: Use appropriate `resolution` values for circles (higher = smoother but more expensive)
- **Layering**: Use `sorting` and `layer` parameters to control drawing order and depth
- **3D Support**: Most functions accept 3D coordinates `(x, y, z)`, but circles are 2D only
- **Filled Shapes**: The `rect()` function supports basic filling using thick lines


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

# Access connection properties
print(f"Host: {sfs.host}")
print(f"Port: {sfs.port}")
print(f"Base URL: {sfs.http.base_url}")

# Change connection settings
sfs.host = "192.168.1.200"
sfs.port = 27773
```

### HTTP Methods

```python
# Low-level HTTP access
data = sfs.http.get_json("/rocket_sim")                    # GET request
result = sfs.http.post_json("/control", {"method": "Stage"})  # POST request
screenshot_bytes = sfs.http.screenshot()                   # Get screenshot
screenshot_bytes = sfs.screenshot()                        # Shortcut method
```

### Multi-Rocket Control

```python
# Control specific rocket
sfs.set_throttle(1.0, rocket="Rocket1")
sfs.rotate("Prograde", rocket="Rocket2")

# Get data for specific rocket
altitude = sfs.values_api.rocket_altitude(rocket="Rocket1")
```

The Silkscreen font used in this library is copyrighted by The Silkscreen Project Authors in 2001. The font is licensed under the SIL Open Font License 1.1, details can be found at: https://openfontlicense.org
Server download link [SFSControl](https://github.com/SFSPlayer-sys/SFSControl).
Example script link [Scripts](https://github.com/SFSPlayer-sys/SFSControl-_-Scripts ).