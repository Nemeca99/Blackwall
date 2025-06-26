"""
Memory Monitoring Demo for BlackwallV2

This script demonstrates the memory monitoring capabilities added to the
Dream Manager component of BlackwallV2. It will:

1. Initialize a DreamManager 
2. Generate synthetic memory entries
3. Trigger a dream cycle
4. Generate a memory usage report and visualization
"""

import os
import sys
import time
import json
import random
from datetime import datetime
from pathlib import Path
import importlib.util
import logging

# Add the parent directory to path so we can import the modules
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Function to safely import modules to avoid circular imports
def safe_import(module_name, class_name):
    try:
        # Try direct import first
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    except (ImportError, AttributeError):
        # If that fails, try loading the module from file path
        try:
            module_path = os.path.join(parent_dir, module_name.replace('.', os.path.sep) + '.py')
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, class_name)
        except Exception as e:
            print(f"Error importing {class_name} from {module_name}: {e}")
            raise

# Import BlackwallV2 components
DreamManager = safe_import('root.dream_manager', 'DreamManager')
LongTermMemory = safe_import('root.Right_Hemisphere', 'LongTermMemory')
Body = safe_import('root.body', 'Body')
Heart = safe_import('root.heart', 'Heart')

# Configure logging
from demo_logging import setup_demo_logger
logger = setup_demo_logger("MemoryMonitoringDemo")

def generate_synthetic_memories(count: int = 100):
    """Generate synthetic memory entries for testing."""
    logger.info(f"Generating {count} synthetic memory entries...")
    
    # Create topics/tags
    topics = ["math", "science", "history", "programming", "art", "music", "philosophy", "physics"]
    
    memories = []
    for i in range(count):
        tag = random.choice(topics)
        memory = {
            "id": f"mem_{i}_{random.randint(1000, 9999)}",
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "content": f"This is a synthetic memory about {tag} with index {i}. " + 
                       f"It contains some random text to simulate a real memory entry. " +
                       f"{''.join(random.choice('abcdefghijklmnopqrstuvwxyz ') for _ in range(random.randint(50, 200)))}",
            "source": "synthetic_generator",
            "metadata": {
                "importance": random.uniform(0.1, 1.0),
                "emotional_valence": random.uniform(-1.0, 1.0)
            }
        }
        memories.append(memory)
    
    return memories

def main():
    logger.info("Starting Memory Monitoring Demo")
    
    # Create necessary directories
    os.makedirs(os.path.join(parent_dir, "memlong"), exist_ok=True)
    os.makedirs(os.path.join(parent_dir, "log"), exist_ok=True)
    
    # Initialize BlackwallV2 components
    body = Body()
    heart = Heart(body=body)
    body.register_module(heart)
    
    # Initialize LTM with synthetic memories
    ltm = LongTermMemory()
    synthetic_memories = generate_synthetic_memories(250)
    ltm.memory = synthetic_memories
    
    # Initialize DreamManager
    dream_manager = DreamManager(
        long_term_memory=ltm,
        heart=heart,
        body=body,
        logger=logger
    )
    body.register_module(dream_manager)
    
    # Register with body
    ltm.register_with_body(body)
    dream_manager.register_with_body(body)
    
    logger.info("System initialized")
    logger.info(f"LTM contains {len(ltm.memory)} memories")
    
    # Let's get a baseline memory usage report
    try:
        logger.info("Generating baseline memory usage report...")
        baseline_report = dream_manager.generate_memory_usage_report()
        logger.info(f"Baseline RSS memory usage: {baseline_report['memory_metrics']['current_usage']['process_memory_info']['rss']:.2f} MB")
        logger.info(f"LTM object size: {baseline_report['memory_metrics']['current_usage']['blackwall_memory']['ltm_object_size']:.2f} MB")
    except ImportError:
        logger.error("Memory monitoring requires psutil package. Install with 'pip install psutil'")
        logger.info("Continuing demo without memory monitoring...")
    except Exception as e:
        logger.error(f"Error generating memory report: {e}")
    
    # Now trigger a dream cycle
    logger.info("Triggering dream cycle...")
    start_time = time.time()
    
    dream_success = dream_manager.enter_dream_cycle()
    
    logger.info(f"Dream cycle completed in {time.time() - start_time:.2f} seconds")
    logger.info(f"Dream cycle success: {dream_success}")
    logger.info(f"LTM now contains {len(ltm.memory)} memories")
    
    # Generate a visualization
    try:
        logger.info("Generating memory usage visualization...")
        report_path = dream_manager.generate_memory_visualization()
        logger.info(f"Memory usage visualization created at: {report_path}")
        logger.info(f"Open this file in your web browser to view the visualization")
    except ImportError:
        logger.error("Visualization requires additional packages. Install from requirements.txt")
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
    
    # Display memory savings summary if available
    try:
        report = dream_manager.generate_memory_usage_report()
        if 'consolidation_efficiency' in report:
            logger.info("Memory Consolidation Efficiency:")
            logger.info(f"  Average Entry Reduction: {report['consolidation_efficiency']['average_entry_reduction_percent']:.2f}%")
            logger.info(f"  Average Size Reduction: {report['consolidation_efficiency']['average_size_reduction_percent']:.2f}%")
    except Exception as e:
        logger.error(f"Error displaying consolidation efficiency: {e}")
    
    logger.info("Memory Monitoring Demo completed")

if __name__ == "__main__":
    main()
