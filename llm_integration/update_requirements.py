"""
Update BlackwallV2 requirements to include LLM integration dependencies
"""

import os
import sys

def update_requirements():
    """Update requirements.txt file with LLM integration dependencies"""
    
    # Define the path to requirements.txt
    trees_root = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..',
        '..',
        '..'
    ))
    
    requirements_path = os.path.join(trees_root, 'requirements.txt')
    
    # Define the new requirements
    new_requirements = [
        'openai>=1.3.0',     # OpenAI API
        'litellm>=1.7.0',    # Unified LLM API
        'python-dotenv>=1.0.0',  # For .env file support
        'requests>=2.31.0'   # HTTP requests for API calls
    ]
    
    # Read existing requirements
    existing_requirements = []
    try:
        with open(requirements_path, 'r', encoding='utf-8') as f:
            existing_requirements = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Requirements file not found at {requirements_path}")
        existing_requirements = []
    
    # Remove any duplicate requirements
    updated_requirements = existing_requirements.copy()
    for new_req in new_requirements:
        req_name = new_req.split('>=')[0].split('==')[0].strip()
        
        # Check if requirement already exists
        exists = False
        for i, existing_req in enumerate(existing_requirements):
            if existing_req.startswith(req_name):
                # Replace the existing requirement
                updated_requirements[i] = new_req
                exists = True
                break
        
        # If it doesn't exist, add it
        if not exists:
            updated_requirements.append(new_req)
    
    # Write updated requirements
    try:
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_requirements) + '\n')
        print(f"Updated {requirements_path} with LLM integration dependencies")
    except Exception as e:
        print(f"Error updating requirements.txt: {e}")

if __name__ == "__main__":
    update_requirements()
