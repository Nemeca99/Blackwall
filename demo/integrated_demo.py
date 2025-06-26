"""
BlackwallV2 Integrated Demo with Dream Cycle and Fragment Integration

This script demonstrates the enhanced BlackwallV2 biomimetic AI system with
integrated Dream Cycle and Fragment-Aware Routing. It supports both
demonstration mode and production mode with real-time processing.
"""

import os
import sys
import time
import argparse
from datetime import datetime
from pathlib import Path
import threading
import json

# Parse command line arguments
parser = argparse.ArgumentParser(description='BlackwallV2 Integrated Runtime')
parser.add_argument('--production', action='store_true', help='Run in production mode')
parser.add_argument('--realtime', action='store_true', help='Enable real-time processing')
parser.add_argument('--memory-path', type=str, help='Path to LTM memory file')
parser.add_argument('--log-level', type=str, default='INFO', 
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                    help='Logging level')
args = parser.parse_args()

# Add parent directories to path for imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "root"))

# Import core components - use absolute imports
sys.path.insert(0, str(root_dir))
try:
    from root.body import Body
    from root.brainstem import Brainstem
    from root.router import Router
    from root.heart import Heart
    from root.queue_manager import QueueManager
    from root.dream_manager import DreamManager
    from root.fragment_manager import FragmentManager
    from root.Left_Hemisphere import ShortTermMemory
    from root.Right_Hemisphere import LongTermMemory
    
    print("Core modules imported successfully")
except ImportError as e:
    print(f"Error importing core modules: {e}")
    sys.exit(1)

class IntegratedDemoLogger:
    """Logger for the integrated demo."""
    def __init__(self, log_path):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        # Create/clear the log file
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"BlackwallV2 Integrated Demo Log - {datetime.now()}\n")
            f.write("=" * 60 + "\n\n")
    
    def log(self, message, level="INFO"):
        """Write message to log file and print to console."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {level}: {message}"
        
        # Write to log file
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_line + "\n")
            
        # Print to console with color based on level
        if level == "INFO":
            print(log_line)
        elif level == "WARNING":
            print(f"\033[93m{log_line}\033[0m")  # Yellow
        elif level == "ERROR":
            print(f"\033[91m{log_line}\033[0m")  # Red
        elif level == "SUCCESS":
            print(f"\033[92m{log_line}\033[0m")  # Green
        else:
            print(log_line)

def print_header():
    """Print the application header."""
    print("\n" + "=" * 60)
    print("       BlackwallV2 / Lyra Blackwall Integrated Demo")
    print(" Dream Cycle and Fragment-Aware Routing Implementation")
    print("=" * 60)
    print("\nThis demo showcases the enhanced features of BlackwallV2:")
    print("- Memory consolidation through biomimetic dream cycles")
    print("- Fragment-aware routing for personality-influenced processing")
    print("- Integration of both systems with the core architecture")
    print("\nEnter 'help' for available commands, 'exit' to quit")
    print("=" * 60 + "\n")

def create_test_memories(ltm, count=10):
    """Create sample memories for the long-term memory."""
    topics = ["math", "language", "history", "science", "art"]
    
    for i in range(1, count + 1):
        topic = topics[i % len(topics)]
        
        # Simple test memory
        memory = {
            'id': i,
            'type': 'memory',
            'tag': topic,
            'timestamp': datetime.now().isoformat(),
            'content': f"Test memory {i} about {topic}",
            'source': 'demo'
        }
        
        # Add to LTM
        if hasattr(ltm, 'add_memory'):
            ltm.add_memory(memory)
        else:
            ltm.memory.append(memory)
        
        print(f"Added memory: {topic} - {memory['content']}")

def print_commands():
    """Print available commands."""
    print("\nAvailable commands:")
    print("  help          - Show this help message")
    print("  status        - Show system status")
    print("  fragments     - Show current fragment activation levels")
    print("  memories      - Show current memory contents")
    print("  dream         - Force a dream cycle")
    print("  activate X Y  - Activate fragment X by amount Y")
    print("  exit          - Exit the demo")
    print("")

def load_real_memories(ltm, memory_path):
    """Load real memories from a JSON file into long-term memory."""
    if not os.path.exists(memory_path):
        print(f"Memory file not found: {memory_path}")
        return False
        
    try:
        with open(memory_path, 'r', encoding='utf-8') as f:
            memories = json.load(f)
            
        if isinstance(memories, list):
            for memory in memories:
                if hasattr(ltm, 'add_memory'):
                    ltm.add_memory(memory)
                else:
                    ltm.memory.append(memory)
            return True
        elif isinstance(memories, dict) and 'memories' in memories:
            for memory in memories['memories']:
                if hasattr(ltm, 'add_memory'):
                    ltm.add_memory(memory)
                else:
                    ltm.memory.append(memory)
            return True
        else:
            print("Invalid memory file format")
            return False
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading memories: {e}")
        return False

def run_integrated_demo():
    """Run the integrated BlackwallV2 demo."""
    # Set up logging
    log_path = os.path.join(root_dir, "log", "integrated_demo_log.txt")
    logger = IntegratedDemoLogger(log_path)
    logger.log(f"Starting {'Production' if args.production else 'Demo'} BlackwallV2 Runtime", "INFO")
    
    if not args.production:
        print_header()
    
    # Initialize core components
    logger.log("Initializing system components...")
    
    # Create the body (communication hub)
    body = Body()
    
    # Create memory components
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    # Ensure memory is initialized properly
    if not hasattr(ltm, 'memory') or ltm.memory is None:
        ltm.memory = []
    
    # Create heart and queue manager
    heart = Heart()
    queue_mgr = QueueManager()
    heart.queue_manager = queue_mgr
    
    # Create router
    router = Router()
    
    # Create dream manager with real-time setting
    dream_manager = DreamManager(
        long_term_memory=ltm,
        heart=heart,
        body=body,
        logger=logger
    )
    
    # Create fragment manager
    fragment_manager = FragmentManager(
        router=router,
        body=body,
        logger=logger
    )
      # Create brainstem to orchestrate everything
    brainstem = Brainstem()
    
    # Register with body
    body.register_module("heart", heart)
    body.register_module("ltm", ltm)
    body.register_module("stm", stm)
    body.register_module("dream_manager", dream_manager)
    body.register_module("fragment_manager", fragment_manager)
    body.register_module("brainstem", brainstem)
    
    # Initialize memories
    if args.memory_path and os.path.exists(args.memory_path):
        logger.log(f"Loading real memories from: {args.memory_path}", "INFO")
        success = load_real_memories(ltm, args.memory_path)
        if success:
            logger.log(f"Successfully loaded memories: {len(ltm.memory)} entries", "SUCCESS")
        else:
            logger.log("Failed to load external memories, using test data instead", "WARNING")
            create_test_memories(ltm, 15)
    else:
        # Initialize with some test memories
        logger.log("Using test memory data", "INFO")
        create_test_memories(ltm, 15)
    # Main interaction loop
    logger.log("System ready, entering command loop", "SUCCESS")
    running = True
    
    while running:
        try:
            # Get user input
            user_input = input("\nCommand or message> ")
            cmd = user_input.lower().strip()
            
            # Process commands
            if cmd == "exit" or cmd == "quit":
                logger.log("Exiting demo", "INFO")
                running = False
                
            elif cmd == "help":
                print_commands()
                
            elif cmd == "status":
                logger.log("System status:", "INFO")
                logger.log(f"  STM entries: {len(stm.memory)}", "INFO")
                logger.log(f"  LTM entries: {len(ltm.memory)}", "INFO")
                
                # Check dream conditions
                should_sleep, conditions = dream_manager.check_sleep_conditions()
                logger.log(f"  Dream cycle needed: {should_sleep}", "INFO")
                for key, value in conditions.items():
                    if isinstance(value, float):
                        logger.log(f"  - {key}: {value:.4f}", "INFO")
                    else:
                        logger.log(f"  - {key}: {value}", "INFO")
                
                # Get current dominant fragment
                dominant = fragment_manager.get_dominant_fragment()
                logger.log(f"  Dominant fragment: {dominant}", "INFO")
                
            elif cmd == "fragments":
                logger.log("Current fragment activation levels:", "INFO")
                for fragment, level in fragment_manager.get_activation_levels().items():
                    logger.log(f"  {fragment}: {level:.1f}", "INFO")
                    
            elif cmd == "memories":
                logger.log("Current memory contents:", "INFO")
                # Group by type
                types = {}
                for mem in ltm.memory:
                    if isinstance(mem, dict):
                        mem_type = mem.get('type', 'unknown')
                        if mem_type not in types:
                            types[mem_type] = 0
                        types[mem_type] += 1
                        
                    # Print memory count by type
                    for mem_type, count in types.items():
                        logger.log(f"  {mem_type}: {count} entries", "INFO")
                        
                # Print a few sample memories
                logger.log("Sample memories:", "INFO")
                for mem in ltm.memory[:3]:
                    if isinstance(mem, dict):
                        logger.log(f"  {mem.get('tag', 'unknown')}: {mem.get('content', 'No content')[:50]}...", "INFO")
                
            elif cmd == "dream":
                logger.log("Forcing dream cycle...", "INFO")
                success = dream_manager.enter_dream_cycle()
                if success:
                    logger.log("Dream cycle completed successfully", "SUCCESS")
                else:
                    logger.log("Dream cycle failed", "ERROR")
                
            elif cmd.startswith("activate "):
                # Parse fragment name and value
                parts = cmd.split()
                if len(parts) == 3:
                    fragment = parts[1].capitalize()
                    try:
                        amount = float(parts[2])
                        logger.log(f"Adjusting {fragment} by {amount}", "INFO")
                        fragment_manager.adjust_fragment_levels({fragment: amount})
                        logger.log("Fragment levels updated", "SUCCESS")
                    except ValueError:
                        logger.log("Invalid amount, must be a number", "ERROR")
                else:
                    logger.log("Usage: activate <fragment> <amount>", "ERROR")
            
            else:
                # Process as regular input
                logger.log(f"Processing input: {user_input}", "INFO")
                
                # Analyze for fragments
                adjustments = fragment_manager.analyze_input_for_fragments(user_input)
                if adjustments:
                    logger.log("Fragment adjustments from input:", "INFO")
                    for fragment, adj in adjustments.items():
                        logger.log(f"  {fragment}: {adj:+.1f}", "INFO")
                    fragment_manager.adjust_fragment_levels(adjustments)
                
                # For now, just echo with the dominant fragment
                dominant = fragment_manager.get_dominant_fragment()
                print(f"\n[{dominant}] {user_input}")
                
        except KeyboardInterrupt:
            logger.log("Demo terminated by user", "WARNING")
            running = False
        except Exception as e:
            logger.log(f"Error: {e}", "ERROR")
    
    logger.log("Demo session ended", "INFO")

if __name__ == "__main__":
    if args.production:
        print("=" * 60)
        print("BLACKWALLV2 PRODUCTION RUNTIME")
        print("Dream Cycle and Fragment Integration Enabled")
        print(f"Real-time Processing: {'Enabled' if args.realtime else 'Disabled'}")
        print("=" * 60)
    
    run_integrated_demo()
