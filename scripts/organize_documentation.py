"""
Script to organize documentation (.md) files into appropriate subdirectories.
"""

import os
import shutil
import re

def categorize_md_file(filename):
    """Categorize a markdown file based on its name."""
    filename_lower = filename.lower()
    
    # Skip README files
    if filename_lower.startswith('readme'):
        return None
        
    # Media documentation
    if any(term in filename_lower for term in ['media', 'audio', 'video', 'image']):
        return 'media'
        
    # Optimization documentation
    if any(term in filename_lower for term in ['optim', 'performance', 'benchmark']):
        return 'optimization'
        
    # Integration documentation
    if any(term in filename_lower for term in ['integrat', 'component', 'system', 'fragment']):
        return 'integration'
        
    # Development documentation
    if any(term in filename_lower for term in ['dev', 'guide', 'implementation', 'plan', 'status']):
        return 'development'
        
    # Default to development
    return 'development'

def organize_documentation():
    """Move documentation files to appropriate directories."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(root_dir, 'docs')
    
    # Ensure docs directories exist
    for subdir in ['media', 'optimization', 'integration', 'development']:
        os.makedirs(os.path.join(docs_dir, subdir), exist_ok=True)
    
    # Find all .md files in the root directory (excluding README.md)
    md_files = [f for f in os.listdir(root_dir) if f.endswith('.md') and not f.startswith('README')]
    
    print(f"Found {len(md_files)} documentation files to organize:")
    
    # Move each file
    for file in md_files:
        source = os.path.join(root_dir, file)
        
        # Determine the appropriate category
        category = categorize_md_file(file)
        if category is None:
            print(f"Skipping {file} (README file)")
            continue
            
        destination = os.path.join(docs_dir, category, file)
        
        # Skip if already in docs dir
        if os.path.dirname(source).startswith(docs_dir):
            continue
            
        print(f"Moving {file} to {category}/")
        shutil.move(source, destination)
    
    print("Complete! Documentation files organized.")

if __name__ == "__main__":
    organize_documentation()
