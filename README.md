# SmartMouse 🖱️

[![PyPI version](https://badge.fury.io/py/smart-mouse.svg)](https://badge.fury.io/py/smart-mouse)
[![Python versions](https://img.shields.io/pypi/pyversions/smart-mouse.svg)](https://pypi.org/project/smart-mouse/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**SmartMouse** is a Python package that simulates realistic, human-like mouse movements using recorded movement patterns from real users. Unlike simple linear interpolation or basic curves, SmartMouse uses actual human movement data to create authentic mouse trajectories with realistic timing.

## 🌟 Features

- **Authentic Human Movement**: Uses real recorded mouse movement data
- **Multiple Movement Patterns**: Different patterns for various distances and directions  
- **Realistic Timing**: Includes authentic pause and movement timing
- **Easy Integration**: Simple API that works with existing automation tools
- **No External Data Required**: Comes with built-in movement patterns
- **Customizable**: Support for custom movement data and parameters
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Demo

https://github.com/user-attachments/assets/6de13f69-3785-4009-8a0e-3762ecce1ad4


## 📦 Installation

Install SmartMouse using pip:

```bash
pip install smart-mouse
```

Or install from source:

```bash
git clone https://github.com/Bandit-HaxUnit/humanmouse.git
cd humanmouse
pip install -e .
```

## 🚀 Quick Start

### Basic Usage

```python
from smart_mouse import SmartMouse

# Create a mover instance (uses built-in movement data)
mover = SmartMouse()

# Move to a specific coordinate
mover.move_to(500, 300)

# Move through multiple points
points = [(100, 100), (300, 200), (500, 400)]
mover.move_along_path(points)
```

### Simple API

```python
from smart_mouse import create_mover

# Even simpler way to create a mover
mover = create_mover()
mover.move_to(800, 600)
```

### Advanced Usage

```python
from smart_mouse import SmartMouse, generate_random_points

# Create mover with custom settings
mover = SmartMouse(
    enable_mouse_control=True,  # Set to False for testing
    distance_thresholds=[10, 20, 50, 100, 200, 500]  # Custom distance categories
)

# Generate random test points
screen_width, screen_height = 1920, 1080
random_points = generate_random_points(5, screen_width, screen_height, padding=100)

# Move through random points with custom pause timing
mover.move_along_path(random_points, pause_range=(0.5, 1.2))

# Get information about available movement patterns
print("Available distances:", mover.get_available_distances())
print("Movement data stats:", mover.get_stats())
```

### Custom Movement Data

```python
# Use your own movement data file
mover = SmartMouse(mouse_data_file="my_custom_movements.json")

# Or provide movement data directly
custom_data = {
    "50": {  # Distance bucket
        "N": [  # Direction (North)
            [
                [0, 1, 1, 0],      # X offsets
                [1, 1, 0, -1],     # Y offsets  
                [8.3, 4.1, 6.2, 12.1]  # Timing (milliseconds)
            ]
        ]
    }
}
mover = SmartMouse(mouse_data=custom_data)
```

### Callbacks and Monitoring

```python
def movement_callback(x, y, step_index):
    print(f"Step {step_index}: Moving to ({x:.1f}, {y:.1f})")

# Move with callback to monitor progress
path = mover.move_to(400, 300, callback=movement_callback)
print(f"Movement completed with {len(path)} steps")
```

## 📖 API Reference

### SmartMouse

The main class for generating human-like mouse movements.

#### Constructor

```python
SmartMouse(
    mouse_data_file=None,     # Optional path to movement data file
    mouse_data=None,          # Optional movement data dict
    distance_thresholds=None, # Custom distance buckets
    enable_mouse_control=True # Whether to actually move the mouse
)
```

#### Methods

- `move_to(target_x, target_y, start_x=None, start_y=None, callback=None)` - Move to coordinates
- `move_along_path(points, pause_range=(0.3, 0.8), callback=None)` - Move through multiple points
- `generate_path(start_x, start_y, target_x, target_y)` - Generate path without moving
- `get_current_position()` - Get current mouse position
- `set_position(x, y)` - Set mouse position instantly
- `get_available_directions(distance)` - Get available movement directions
- `get_available_distances()` - Get all distance buckets
- `get_stats()` - Get movement data statistics

### Utility Functions

- `create_mover(**kwargs)` - Convenience function to create a SmartMouse
- `generate_random_points(num_points, screen_width, screen_height, padding=100)` - Generate random coordinates

### Movement Data Format

The movement data uses this JSON structure:

```json
{
  "distance_bucket": {
    "direction": [
      [
        [x_offset_1, x_offset_2, ...],     // X coordinate offsets
        [y_offset_1, y_offset_2, ...],     // Y coordinate offsets  
        [time_1, time_2, ...]              // Timing in milliseconds
      ]
    ]
  }
}
```

Distance buckets are strings representing maximum pixel distances (e.g., "50", "100").
Directions are: "N", "NE", "E", "SE", "S", "SW", "W", "NW".

## 🔧 Development

### Setting Up Development Environment

```bash
git clone https://github.com/Bandit-HaxUnit/humanmouse.git
cd humanmouse
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black humanmouse/
flake8 humanmouse/
```

### Building and Publishing

```bash
# Build the package
python -m build

# Upload to PyPI (requires credentials)
python -m twine upload dist/*
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This package is intended for legitimate automation, testing, and accessibility purposes. Please ensure you comply with the terms of service of any applications you automate and respect user privacy and consent.

## 🙏 Acknowledgments

- Thanks to all the users who contributed their mouse movement data
- Inspired by the need for more realistic automation in testing and accessibility tools
- Built with love for the Python automation community

---

**Made with ❤️ by HaxUnit**
