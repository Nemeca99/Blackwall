"""
Script to move standalone demo files from the root directory to the demo directory.
"""

import os
import shutil

def move_demo_files():
    """Move demo-related Python files from root to demo folder."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    demo_dir = os.path.join(root_dir, 'demo')
    
    # Ensure demo directory exists
    os.makedirs(demo_dir, exist_ok=True)
    
    # List of demo files in the root directory
    demo_files = [
        'heart_optimization_demo.py',
        'media_integration_demo.py',
        'optimize_algorithms.py',
        'profile_script.py',
        'profile_script_simplified.py',
        'run_llm_demo.py',
        'simple_profiler.py',
        'standalone_media_demo.py',
        'test_integration.py',
        'test_optimized_integration.py'
    ]
    
    # Add any files with "demo" or "benchmark" in their name
    for filename in os.listdir(root_dir):
        if filename.endswith('.py') and ('demo' in filename.lower() or 'benchmark' in filename.lower()):
            if filename not in demo_files:
                demo_files.append(filename)
    
    print(f"Found {len(demo_files)} demo files to move:")
    
    # Move each file
    for file in demo_files:
        source = os.path.join(root_dir, file)
        
        # Skip if file doesn't exist
        if not os.path.exists(source):
            print(f"Skipping {file} (not found)")
            continue
            
        destination = os.path.join(demo_dir, file)
        
        # Skip if already in demo dir
        if os.path.dirname(source) == demo_dir:
            continue
            
        print(f"Moving {file}...")
        shutil.move(source, destination)
    
    print("Complete! All demo files moved to the demo directory.")

if __name__ == "__main__":
    move_demo_files()
