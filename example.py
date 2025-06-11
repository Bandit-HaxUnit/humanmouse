#!/usr/bin/env python3
"""
HumanMouse Example Usage

This script demonstrates how to use the HumanMouse package for human-like mouse movements.
"""

import time
from human_mouse import HumanMouseMover, create_mover, generate_random_points


def basic_example():
    """Basic usage example."""
    print("=== Basic Example ===")
    
    # Create a mover (uses built-in movement data)
    mover = HumanMouseMover(enable_mouse_control=False)  # Set to True to actually move mouse
    
    # Move to a specific coordinate
    print("Moving to (500, 300)...")
    path = mover.move_to(500, 300, start_x=100, start_y=100)
    print(f"Movement completed with {len(path)} steps")
    
    # Get some stats about the movement data
    stats = mover.get_stats()
    print(f"Total movement patterns available: {stats['total_paths']}")
    print(f"Distance buckets: {len(stats['distance_buckets'])}")


def advanced_example():
    """Advanced usage example."""
    print("\n=== Advanced Example ===")
    
    # Create mover with simplified API
    mover = create_mover(enable_mouse_control=False)
    
    # Generate some random points to visit
    screen_width, screen_height = 1920, 1080
    random_points = generate_random_points(5, screen_width, screen_height, padding=50)
    print(f"Generated random points: {random_points}")
    
    # Move through the points with custom timing
    print("Moving through random points...")
    all_paths = mover.move_along_path(random_points, pause_range=(0.1, 0.3))
    print(f"Completed {len(all_paths)} movements")
    
    # Show available movement directions for different distances
    for distance in [50, 100, 200]:
        directions = mover.get_available_directions(distance)
        print(f"Available directions for {distance}px: {directions}")


def callback_example():
    """Example with movement callback."""
    print("\n=== Callback Example ===")
    
    mover = HumanMouseMover(enable_mouse_control=False)
    
    def movement_callback(x, y, step_index):
        """Callback function called for each movement step."""
        print(f"  Step {step_index:2d}: ({x:6.1f}, {y:6.1f})")
    
    print("Moving with callback monitoring...")
    path = mover.move_to(400, 300, start_x=100, start_y=50, callback=movement_callback)
    print(f"Movement completed!")


def path_generation_example():
    """Example of generating paths without actually moving."""
    print("\n=== Path Generation Example ===")
    
    mover = HumanMouseMover(enable_mouse_control=False)
    
    # Generate a path without moving
    start_x, start_y = 100, 100
    target_x, target_y = 500, 400
    
    path, timings = mover.generate_path(start_x, start_y, target_x, target_y)
    
    print(f"Generated path from ({start_x}, {start_y}) to ({target_x}, {target_y})")
    print(f"Path has {len(path)} points with timings")
    print(f"First few points: {path[:3]}")
    print(f"Total movement time: {sum(timings):.3f} seconds")


if __name__ == "__main__":
    print("HumanMouse Example Script")
    print("=" * 40)
    
    try:
        basic_example()
        advanced_example()
        callback_example()
        path_generation_example()
        
        print("\n" + "=" * 40)
        print("All examples completed successfully!")
        print("\nTo actually move the mouse, set enable_mouse_control=True")
        print("Note: You'll need 'pip install pynput' for actual mouse control")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have installed the humanmouse package:")
        print("  pip install humanmouse") 