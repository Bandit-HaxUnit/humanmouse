"""
Human-like Mouse Movement API

A Python package for simulating realistic mouse movements using recorded human movement patterns.
This module provides a clean API for generating human-like mouse trajectories with authentic timing.
"""

import json
import math
import random
import time
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any, Union
from pynput.mouse import Button


try:
    from pynput.mouse import Controller
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    Controller = None

__version__ = "1.0.0"
__all__ = ["SmartMouse", "MouseMovementError"]


class MouseMovementError(Exception):
    """Custom exception for mouse movement related errors."""
    pass


class SmartMouse:
    """
    A class for generating human-like mouse movements using recorded movement patterns.
    
    This class loads pre-recorded mouse movement data and uses it to generate
    realistic mouse movements with authentic timing patterns.
    """
    
    # Default distance thresholds for movement categorization
    DEFAULT_DISTANCE_THRESHOLDS = [12, 18, 26, 39, 58, 87, 130, 190, 260, 360, 500]
    
    # Default timing fallback for old data format (in seconds)
    DEFAULT_TIMING_INTERVAL = 0.008
    
    def __init__(self, 
                 mouse_data_file: Optional[Union[str, Path]] = None,
                 mouse_data: Optional[Dict[str, Any]] = None,
                 distance_thresholds: Optional[List[int]] = None,
                 enable_mouse_control: bool = True):
        """
        Initialize the HumanMouseMover.
        
        Args:
            mouse_data_file: Path to JSON file containing mouse movement data (optional - uses built-in data if not provided)
            mouse_data: Dict containing mouse movement data (alternative to file)
            distance_thresholds: Custom distance thresholds for movement categorization
            enable_mouse_control: Whether to actually control the mouse (False for testing)
        
        Raises:
            MouseMovementError: If pynput is not available and mouse control is enabled
            MouseMovementError: If mouse data cannot be loaded
        """
        if enable_mouse_control and not PYNPUT_AVAILABLE:
            raise MouseMovementError(
                "pynput is required for mouse control. Install with: pip install pynput"
            )
        
        self.enable_mouse_control = enable_mouse_control
        self.mouse = Controller() if (enable_mouse_control and PYNPUT_AVAILABLE) else None
        self.distance_thresholds = distance_thresholds or self.DEFAULT_DISTANCE_THRESHOLDS
        
        # Load mouse movement data
        if mouse_data is not None:
            self.mouse_data = mouse_data
        elif mouse_data_file is not None:
            self.mouse_data = self._load_mouse_data(mouse_data_file)
        else:
            # Use built-in mousedata.json from the package
            default_data_path = Path(__file__).parent / "mousedata.json"
            self.mouse_data = self._load_mouse_data(default_data_path)
    
    def _load_mouse_data(self, mouse_data_file: Union[str, Path]) -> Dict[str, Any]:
        """
        Load mouse movement data from a JSON file.
        
        Args:
            mouse_data_file: Path to the JSON file
            
        Returns:
            Dict containing the mouse movement data
            
        Raises:
            MouseMovementError: If file cannot be loaded or parsed
        """
        try:
            file_path = Path(mouse_data_file)
            if not file_path.exists():
                raise MouseMovementError(f"Mouse data file not found: {mouse_data_file}")
            
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise MouseMovementError(f"Invalid JSON in mouse data file: {e}")
        except Exception as e:
            raise MouseMovementError(f"Error loading mouse data: {e}")
    
    @staticmethod
    def get_path_distance_bucket(distance: float, 
                               thresholds: Optional[List[int]] = None) -> str:
        """
        Find the appropriate distance bucket for a given distance.
        
        Args:
            distance: The distance to categorize
            thresholds: Distance thresholds to use (uses default if None)
            
        Returns:
            String representation of the distance bucket
        """
        if thresholds is None:
            thresholds = SmartMouse.DEFAULT_DISTANCE_THRESHOLDS
            
        for threshold in thresholds:
            if distance <= threshold:
                return str(threshold)
        return str(thresholds[-1])
    
    @staticmethod
    def angle_to_direction(angle_deg: float) -> str:
        """
        Convert an angle in degrees to one of 8 cardinal directions.
        
        Args:
            angle_deg: Angle in degrees
            
        Returns:
            Direction string (E, NE, N, NW, W, SW, S, SE)
        """
        directions = ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
        index = round(((angle_deg % 360) + 22.5) / 45) % 8
        return directions[index]
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Get the current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
            
        Raises:
            MouseMovementError: If mouse control is not enabled
        """
        if not self.mouse:
            raise MouseMovementError("Mouse control is not enabled")
        return self.mouse.position
    
    def set_position(self, x: int, y: int):
        """
        Set the mouse position directly (instant jump).
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
        """
        if self.mouse:
            self.mouse.position = (x, y)
    
    def move_to(self, 
                target_x: int, 
                target_y: int, 
                start_x: Optional[int] = None, 
                start_y: Optional[int] = None,
                callback: Optional[callable] = None) -> List[Tuple[float, float]]:
        """
        Move the mouse from current position (or specified start) to target position.
        
        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
            start_x: Starting X coordinate (uses current position if None)
            start_y: Starting Y coordinate (uses current position if None)
            callback: Optional callback function called for each position (x, y, step_index)
            
        Returns:
            List of (x, y) coordinates representing the movement path
            
        Raises:
            MouseMovementError: If mouse control is enabled but not available
        """
        # Determine starting position
        if start_x is None or start_y is None:
            if self.mouse:
                start_x, start_y = self.mouse.position
            else:
                raise MouseMovementError(
                    "start_x and start_y must be provided when mouse control is disabled"
                )
        
        distance = math.hypot(target_x - start_x, target_y - start_y)
        
        # No movement needed for very small distances
        if distance < 1:
            return [(target_x, target_y)]
        
        # Get movement path and timing
        angle = math.degrees(math.atan2(target_y - start_y, target_x - start_x))
        direction = self.angle_to_direction(angle)
        path_profile = self._pick_path_profile(distance, direction)
        
        if not path_profile:
            # No suitable path found, do direct movement
            if self.mouse:
                self.mouse.position = (target_x, target_y)
            if callback:
                callback(target_x, target_y, 0)
            return [(target_x, target_y)]
        
        # Reconstruct the full path
        x_offsets, y_offsets, time_deltas = path_profile
        path = self._reconstruct_path(start_x, start_y, target_x, target_y, x_offsets, y_offsets)
        
        # Execute the movement
        for i, (px, py) in enumerate(path):
            if self.mouse:
                self.mouse.position = (px, py)
            
            if callback:
                callback(px, py, i)
            
            # Apply timing delay
            if i < len(time_deltas):
                sleep_duration = max(0.001, time_deltas[i])
                time.sleep(sleep_duration)
        
        # Ensure final position is exact
        if self.mouse:
            self.mouse.position = (target_x, target_y)
        
        return path
    
    def generate_path(self, 
                     start_x: int, 
                     start_y: int, 
                     target_x: int, 
                     target_y: int) -> Tuple[List[Tuple[float, float]], List[float]]:
        """
        Generate a movement path without executing it.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            target_x: Target X coordinate
            target_y: Target Y coordinate
            
        Returns:
            Tuple of (path_coordinates, timing_deltas)
            path_coordinates: List of (x, y) tuples
            timing_deltas: List of timing delays in seconds
        """
        distance = math.hypot(target_x - start_x, target_y - start_y)
        
        if distance < 1:
            return [(target_x, target_y)], [0.0]
        
        angle = math.degrees(math.atan2(target_y - start_y, target_x - start_x))
        direction = self.angle_to_direction(angle)
        path_profile = self._pick_path_profile(distance, direction)
        
        if not path_profile:
            return [(target_x, target_y)], [0.0]
        
        x_offsets, y_offsets, time_deltas = path_profile
        path = self._reconstruct_path(start_x, start_y, target_x, target_y, x_offsets, y_offsets)
        
        return path, time_deltas
    
    def move_along_path(self, 
                       points: List[Tuple[int, int]], 
                       pause_range: Tuple[float, float] = (0.3, 0.8),
                       callback: Optional[callable] = None) -> List[List[Tuple[float, float]]]:
        """
        Move the mouse along a series of points.
        
        Args:
            points: List of (x, y) coordinates to visit
            pause_range: Range for random pauses between movements (min, max) in seconds
            callback: Optional callback function called for each position
            
        Returns:
            List of paths (each path is a list of coordinates)
        """
        all_paths = []
        
        for i, (target_x, target_y) in enumerate(points):
            path = self.move_to(target_x, target_y, callback=callback)
            all_paths.append(path)
            
            # Add pause between movements (except after the last point)
            if i < len(points) - 1:
                pause_duration = random.uniform(pause_range[0], pause_range[1])
                time.sleep(pause_duration)
        
        return all_paths
    
    def _pick_path_profile(self, distance: float, direction: str) -> Optional[Tuple[List[int], List[int], List[float]]]:
        """
        Pick a random path profile from the loaded data.
        
        Args:
            distance: Movement distance
            direction: Movement direction
            
        Returns:
            Tuple of (x_offsets, y_offsets, time_deltas) or None if not found
        """
        dist_bucket = self.get_path_distance_bucket(distance, self.distance_thresholds)
        paths_in_bucket = self.mouse_data.get(dist_bucket, {})
        available_paths = paths_in_bucket.get(direction, [])
        
        if not available_paths:
            return None
        
        selected_path = random.choice(available_paths)
        
        # Handle backward compatibility
        if len(selected_path) == 2:
            # Old format: only position offsets
            x_offsets, y_offsets = selected_path
            time_deltas = [self.DEFAULT_TIMING_INTERVAL] * len(x_offsets)
            return x_offsets, y_offsets, time_deltas
        elif len(selected_path) == 3:
            # New format: includes timing data
            x_offsets, y_offsets, time_deltas = selected_path
            # Convert from milliseconds to seconds
            time_deltas_sec = [dt / 1000.0 for dt in time_deltas]
            return x_offsets, y_offsets, time_deltas_sec
        else:
            return None
    
    @staticmethod
    def _reconstruct_path(start_x: int, 
                         start_y: int, 
                         target_x: int, 
                         target_y: int, 
                         x_offsets: List[int], 
                         y_offsets: List[int]) -> List[Tuple[float, float]]:
        """
        Reconstruct the absolute coordinate path from offset data.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            target_x: Target X coordinate
            target_y: Target Y coordinate
            x_offsets: List of X coordinate offsets
            y_offsets: List of Y coordinate offsets
            
        Returns:
            List of (x, y) coordinate tuples representing the path
        """
        path_len = min(len(x_offsets), len(y_offsets))
        if not path_len:
            return [(target_x, target_y)]
        
        total_offset_x = sum(x_offsets)
        total_offset_y = sum(y_offsets)
        
        # Calculate the linear distance that needs to be covered
        linear_dx = target_x - start_x - total_offset_x
        linear_dy = target_y - start_y - total_offset_y
        
        path = []
        for i in range(path_len):
            progress = (i + 1) / path_len
            
            # Linear interpolation
            current_linear_x = start_x + linear_dx * progress
            current_linear_y = start_y + linear_dy * progress
            
            # Add cumulative offsets
            cumulative_offset_x = sum(x_offsets[:i + 1])
            cumulative_offset_y = sum(y_offsets[:i + 1])
            
            new_x = current_linear_x + cumulative_offset_x
            new_y = current_linear_y + cumulative_offset_y
            path.append((new_x, new_y))
        
        return path
    
    def get_available_directions(self, distance: float) -> List[str]:
        """
        Get available movement directions for a given distance.
        
        Args:
            distance: Movement distance
            
        Returns:
            List of available direction strings
        """
        dist_bucket = self.get_path_distance_bucket(distance, self.distance_thresholds)
        paths_in_bucket = self.mouse_data.get(dist_bucket, {})
        return list(paths_in_bucket.keys())
    
    def get_available_distances(self) -> List[str]:
        """
        Get all available distance buckets in the loaded data.
        
        Returns:
            List of distance bucket strings
        """
        return list(self.mouse_data.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the loaded mouse movement data.
        
        Returns:
            Dictionary containing data statistics
        """
        stats = {
            "distance_buckets": len(self.mouse_data),
            "total_paths": 0,
            "directions_per_distance": {},
            "paths_per_direction": {}
        }
        
        for dist_bucket, directions in self.mouse_data.items():
            direction_count = len(directions)
            path_counts = {}
            total_paths_in_bucket = 0
            
            for direction, paths in directions.items():
                path_count = len(paths)
                path_counts[direction] = path_count
                total_paths_in_bucket += path_count
            
            stats["directions_per_distance"][dist_bucket] = direction_count
            stats["paths_per_direction"][dist_bucket] = path_counts
            stats["total_paths"] += total_paths_in_bucket
        
        return stats
    
    def click(self, button: Button = Button.left, n: int = 1, **kwargs):
        """
        Click the mouse button.
        """
        self.mouse.click(button, n, **kwargs)


# Utility functions for package users
def create_mover(mouse_data_file: Optional[Union[str, Path]] = None, **kwargs) -> SmartMouse:
    """
    Convenience function to create a SmartMouse instance.
    
    Args:
        mouse_data_file: Path to mouse movement data file (optional - uses built-in data if not provided)
        **kwargs: Additional arguments passed to SmartMouse
        
    Returns:
        SmartMouse instance
    """
    return SmartMouse(mouse_data_file=mouse_data_file, **kwargs)


def generate_random_points(num_points: int, 
                         screen_width: int, 
                         screen_height: int,
                         padding: int = 100) -> List[Tuple[int, int]]:
    """
    Generate random points within screen bounds.
    
    Args:
        num_points: Number of points to generate
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
        padding: Padding from screen edges in pixels
        
    Returns:
        List of (x, y) coordinate tuples
    """
    return [
        (
            random.randint(padding, screen_width - padding),
            random.randint(padding, screen_height - padding)
        )
        for _ in range(num_points)
    ]