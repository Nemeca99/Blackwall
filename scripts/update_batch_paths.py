"""
Script to update batch file paths to reference files moved during reorganization.
"""

import os
import re

def update_batch_files():
    """Update batch file paths to reference files moved during reorganization."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    batch_dir = os.path.join(root_dir, 'batch')
    
    # Ensure batch directory exists
    if not os.path.exists(batch_dir):
        print("Error: Batch directory does not exist.")
        return
    
    # Find all .bat files in the batch directory
    batch_files = [f for f in os.listdir(batch_dir) if f.endswith('.bat')]
    
    print(f"Found {len(batch_files)} batch files to update:")
    
    # File path mapping (old -> new)
    path_mapping = {
        # Demo files
        'heart_optimization_demo.py': 'demo\\heart_optimization_demo.py',
        'media_integration_demo.py': 'demo\\media_integration_demo.py',
        'standalone_media_demo.py': 'demo\\standalone_media_demo.py',
        'optimize_algorithms.py': 'demo\\optimize_algorithms.py',
        'profile_script.py': 'demo\\profile_script.py',
        'profile_script_simplified.py': 'demo\\profile_script_simplified.py',
        'run_llm_demo.py': 'demo\\run_llm_demo.py',
        'simple_profiler.py': 'demo\\simple_profiler.py',
        'test_integration.py': 'demo\\test_integration.py',
        'test_optimized_integration.py': 'demo\\test_optimized_integration.py',
        'benchmark_fragment_routing.py': 'demo\\benchmark_fragment_routing.py',
        'benchmark_heart_timing.py': 'demo\\benchmark_heart_timing.py',
        'benchmark_hemisphere_optimization.py': 'demo\\benchmark_hemisphere_optimization.py',
        'benchmark_optimization.py': 'demo\\benchmark_optimization.py',
        
        # Other paths that might need updating
        '.\\': '..\\',  # Update relative paths
    }
    
    # Update each file
    for file in batch_files:
        file_path = os.path.join(batch_dir, file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Make replacements
            modified = False
            for old_path, new_path in path_mapping.items():
                if old_path in content:
                    content = content.replace(old_path, new_path)
                    modified = True
            
            if modified:
                print(f"Updating {file}...")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"No changes needed for {file}")
                
        except Exception as e:
            print(f"Error updating {file}: {e}")
    
    print("Complete! Batch files updated to reference new file locations.")

if __name__ == "__main__":
    update_batch_files()
