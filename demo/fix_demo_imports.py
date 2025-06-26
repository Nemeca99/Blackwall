"""
Fix imports in queue_driven_demo.py
"""
import os
import sys
import importlib.util

def fix_demo_file():
    """Fix the imports in queue_driven_demo.py"""
    # Read the current content
    with open("queue_driven_demo.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create a backup
    with open("queue_driven_demo.py.bak", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Create a fixed version with proper imports
    fixed_content = """\"\"\"
BlackwallV2 Queue-Driven Demo

This script demonstrates the integration of the heart module with the queue manager,
showing the heartbeat-driven, pulse-limited concurrent processing architecture.
\"\"\"

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import importlib

# Set up the necessary paths
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"

sys.path.insert(0, str(implementation_dir))
sys.path.insert(0, str(root_dir))

# Import core modules
try:
    Heart = importlib.import_module('heart').Heart
    QueueManager = importlib.import_module('queue_manager').QueueManager
    ProcessingItem = importlib.import_module('queue_manager').ProcessingItem
    Router = importlib.import_module('router').Router
    
    print("\\nHeart, QueueManager, and Router modules imported successfully\\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)
    
class DemoLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        # Create/clear the log file
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== BlackwallV2 Demo Log - {datetime.now()} ===\\n\\n")
    
    def log(self, message):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(f"{message}\\n")

"""
    
    # Add rest of the original content, skipping the import section
    skip_start = content.find('class DemoLogger:')
    if skip_start != -1:
        fixed_content += content[skip_start:]
    else:
        # If not found, add whole content after imports
        skip_start = content.find('except ImportError as e:')
        if skip_start != -1:
            # Find the end of this section
            next_line_start = content.find('\n', skip_start)
            if next_line_start != -1:
                fixed_content += content[next_line_start:]
    
    # Write the fixed content
    with open("queue_driven_demo_fixed.py", "w", encoding="utf-8") as f:
        f.write(fixed_content)
    
    print("Fixed demo file created as 'queue_driven_demo_fixed.py'")

if __name__ == "__main__":
    fix_demo_file()
