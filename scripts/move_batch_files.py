"""
Script to move all batch (.bat) files from the root directory to the batch directory.
"""

import os
import shutil

def move_batch_files():
    """Move all .bat files from root to batch folder."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    batch_dir = os.path.join(root_dir, 'batch')
    
    # Ensure batch directory exists
    os.makedirs(batch_dir, exist_ok=True)
    
    # Find all .bat files in the root directory
    batch_files = [f for f in os.listdir(root_dir) if f.endswith('.bat')]
    
    print(f"Found {len(batch_files)} batch files to move:")
    
    # Move each file
    for file in batch_files:
        source = os.path.join(root_dir, file)
        destination = os.path.join(batch_dir, file)
        
        # Skip if already in batch dir
        if os.path.dirname(source) == batch_dir:
            continue
            
        print(f"Moving {file}...")
        shutil.move(source, destination)
    
    print("Complete! All batch files moved to the batch directory.")

if __name__ == "__main__":
    move_batch_files()
