"""
Dream Cycle Demo - Demonstrates memory consolidation and insight generation in BlackwallV2

This demo showcases the dream cycle functionality for the BlackwallV2 architecture,
simulating memory fragmentation, triggering dream cycles, and generating insights.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime
import importlib
import random
import json

# Import standardized logging
from demo_logging import setup_demo_logger, print_and_log, DemoLogger

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
    Body = importlib.import_module('body').Body
    DreamManager = importlib.import_module('dream_manager').DreamManager
    Brainstem = importlib.import_module('brainstem').Brainstem
    
    # Try to import optional modules
    try:
        Lungs = importlib.import_module('lungs').Lungs
        ShortTermMemory = importlib.import_module('Left_Hemisphere').ShortTermMemory
        LongTermMemory = importlib.import_module('Right_Hemisphere').LongTermMemory
    except ImportError:
        print("Note: Some optional modules could not be imported")
    
    print("\nCore modules imported successfully\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Using imported DemoLogger and print_and_log from demo_logging.py


def create_sample_memories(count=20):
    """Create sample memories for testing"""
    topics = ["math", "language", "history", "science", "art"]
    
    memories = []
    for i in range(1, count + 1):
        topic = random.choice(topics)
        
        # Create content based on topic
        if topic == "math":
            content_options = [
                "The formula for the area of a circle is πr²",
                "The Pythagorean theorem states that a² + b² = c²",
                "The sum of integers from 1 to n is n(n+1)/2",
                "The quadratic formula is x = (-b ± √(b² - 4ac))/2a",
                "Euler's identity is e^(iπ) + 1 = 0"
            ]
        elif topic == "language":
            content_options = [
                "English has Germanic roots with Latin influence",
                "Spanish is a Romance language derived from Latin",
                "Mandarin Chinese is the most spoken language globally",
                "The English alphabet has 26 letters",
                "Sanskrit is one of the oldest languages still in use"
            ]
        elif topic == "history":
            content_options = [
                "The Roman Empire fell in 476 CE",
                "The American Declaration of Independence was signed in 1776",
                "World War II ended in 1945",
                "The Byzantine Empire lasted until 1453",
                "The Industrial Revolution began in the late 18th century"
            ]
        elif topic == "science":
            content_options = [
                "The speed of light is approximately 299,792,458 meters per second",
                "Water's chemical formula is H₂O",
                "DNA has a double-helix structure",
                "The Earth orbits the Sun at an average distance of 93 million miles",
                "Quantum mechanics describes nature at the atomic scale"
            ]
        else:  # art
            content_options = [
                "The Mona Lisa was painted by Leonardo da Vinci",
                "Impressionism began in the late 19th century",
                "Vincent van Gogh painted 'Starry Night'",
                "Pablo Picasso co-founded the Cubist movement",
                "The Louvre is the world's most visited art museum"
            ]
            
        content = random.choice(content_options)
        
        memory = {
            'id': i,
            'type': 'memory',
            'tag': topic,
            'timestamp': (datetime.now().replace(
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )).isoformat(),
            'content': content,
            'source': 'demo'
        }
        
        memories.append(memory)
        
    return memories


def run_dream_cycle_demo():
    """Run the dream cycle demonstration"""
    # Set up logging using standardized logger
    logger = DemoLogger(demo_name="Dream Cycle Demo")
    
    print_and_log(logger, "Starting Dream Cycle Demo", "INFO")
    print_and_log(logger, "=" * 50)
    
    # Create core components
    print_and_log(logger, "Creating system components...")
    
    heart = Heart()
    queue_mgr = QueueManager()
    heart.queue_manager = queue_mgr
    
    # Create body for signaling
    body = Body()
    
    # Create memory components
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    
    # Create brainstem
    brainstem = Brainstem()
    
    # Ensure memory is initialized properly
    if not hasattr(ltm, 'memory') or ltm.memory is None:
        ltm.memory = []
    
    # Create dream manager
    dream_manager = DreamManager(
        long_term_memory=ltm,
        heart=heart,
        body=body,
        logger=logger
    )    
    
    # Register with body
    body.register_module("heart", heart)
    body.register_module("ltm", ltm)
    body.register_module("dream_manager", dream_manager)
    body.register_module("brainstem", brainstem)
    
    print_and_log(logger, "System components initialized")
      # Phase 1: Create some initial memories
    print_and_log(logger, "\nPhase 1: Creating initial memories...")
    initial_memories = create_sample_memories(5)
    
    # Ensure memory is initialized properly
    if not hasattr(ltm, 'memory'):
        ltm.memory = []
    
    # Add memories directly to memory list since add_memory might not exist
    for mem in initial_memories:
        if hasattr(ltm, 'add_memory'):
            ltm.add_memory(mem)
        else:
            ltm.memory.append(mem)
        print_and_log(logger, f"Added memory: {mem['tag']} - {mem['content'][:40]}...")
        
    # Check dream conditions
    should_sleep, conditions = dream_manager.check_sleep_conditions()
    print_and_log(logger, f"\nInitial dream check: Should sleep = {should_sleep}")
    for key, value in conditions.items():
        print_and_log(logger, f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Phase 2: Add more memories to increase fragmentation
    print_and_log(logger, "\nPhase 2: Adding more memories to increase fragmentation...")
    time.sleep(1)  # Pause for effect
      # Add many memories of same topics to create fragmentation
    more_memories = create_sample_memories(15)
    for mem in more_memories:
        if hasattr(ltm, 'add_memory'):
            ltm.add_memory(mem)
        else:
            ltm.memory.append(mem)
    
    print_and_log(logger, f"Added {len(more_memories)} more memories")
    print_and_log(logger, f"Current memory count: {len(ltm.memory)}")
    
    # Count memories by topic
    topics = {}
    for mem in ltm.memory:
        if isinstance(mem, dict) and 'tag' in mem:
            topics[mem['tag']] = topics.get(mem['tag'], 0) + 1
    
    print_and_log(logger, "Memory distribution by topic:")
    for topic, count in topics.items():
        print_and_log(logger, f"  {topic}: {count} memories")
    
    # Check dream conditions again
    should_sleep, conditions = dream_manager.check_sleep_conditions()
    print_and_log(logger, f"\nAfter adding memories: Should sleep = {should_sleep}")
    for key, value in conditions.items():
        print_and_log(logger, f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    
    # Phase 3: Force dream cycle if needed
    print_and_log(logger, "\nPhase 3: Initiating dream cycle...")
    time.sleep(1)  # Pause for effect
    
    if not should_sleep:
        print_and_log(logger, "Forcing dream cycle for demonstration...", "WARNING")
        dream_manager.last_dream_time = 0  # Reset timer to allow immediate dreaming
    
    # Enter dream cycle
    print_and_log(logger, "Entering dream cycle...", "INFO")
    success = dream_manager.enter_dream_cycle()
    
    if success:
        print_and_log(logger, "Dream cycle completed successfully", "SUCCESS")
    else:
        print_and_log(logger, "Dream cycle failed", "ERROR")
    
    # Phase 4: Examine results
    print_and_log(logger, "\nPhase 4: Examining dream cycle results...")
    time.sleep(1)  # Pause for effect
    
    # Check for consolidated memories
    consolidated = [m for m in ltm.memory if isinstance(m, dict) and 
                   m.get('type') == 'consolidated_memory']
    
    insights = [m for m in ltm.memory if isinstance(m, dict) and 
               m.get('type') == 'dream_insight']
    
    print_and_log(logger, f"Found {len(consolidated)} consolidated memories")
    print_and_log(logger, f"Generated {len(insights)} insights")
    
    # Display some examples
    if consolidated:
        print_and_log(logger, "\nSample consolidated memory:")
        sample = consolidated[0]
        print_and_log(logger, f"  Tag: {sample.get('tag')}")
        print_and_log(logger, f"  Source count: {sample.get('source_count')}")
        content = sample.get('content', '')
        print_and_log(logger, f"  Content: {content[:100]}..." if len(content) > 100 else f"  Content: {content}")
    
    if insights:
        print_and_log(logger, "\nSample insight:")
        sample = insights[0]
        print_and_log(logger, f"  Content: {sample.get('content')}")
    
    # Phase 5: Check dream stats
    print_and_log(logger, "\nPhase 5: Dream cycle statistics...")
    stats = dream_manager.consolidation_stats
    
    print_and_log(logger, "Dream cycle statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print_and_log(logger, f"  {key}: {value:.2f}")
        else:
            print_and_log(logger, f"  {key}: {value}")
    
    print_and_log(logger, "\nDream Cycle Demo completed", "SUCCESS")
    print_and_log(logger, "Check dream_log.txt for detailed dream activity")
    print_and_log(logger, "=" * 50)


if __name__ == "__main__":
    run_dream_cycle_demo()
