"""
HumanMouse - Human-like Mouse Movement API

A Python package for simulating realistic mouse movements using recorded human movement patterns.
"""

from .core import (
    HumanMouseMover,
    MouseMovementError,
    create_mover,
    generate_random_points
)

__version__ = "1.0.0"
__author__ = "HumanMouse Team"
__email__ = "contact@humanmouse.com"
__description__ = "Human-like mouse movement simulation using recorded patterns"

__all__ = [
    "HumanMouseMover",
    "MouseMovementError", 
    "create_mover",
    "generate_random_points"
]
