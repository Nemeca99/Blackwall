"""
BlackwallV2 Simple Queue-Driven Demo

A simplified version of the Queue-Driven Demo that fixes the import and syntax errors.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import importlib
import random
import hashlib
import json

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

class DemoLogger:
    """Simple logger for the demo application"""
    def __init__(self, log_path):
        self.log_path = log_path
        # Create/clear the log file
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== BlackwallV2 Demo Log - {datetime.now()} ===\n\n")
    
    def log(self, message):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")

class Brainstem:
    """Central processing component for the biomimetic system"""
    def __init__(self, body=None, queue_manager=None, logger=None):
        self.body = body
        self.queue_manager = queue_manager
        self.logger = logger
        self.processing_delay = 0.3  # Simulate processing time
        print("[Brainstem] Initialized")
    
    def process_input(self, item):
        text_input = item.content.get('text', '')
        self.logger.log(f"[Brainstem] Processing: {text_input}")
        
        # Simulate processing delay
        time.sleep(self.processing_delay)
        
        # Handle empty input
        if not text_input.strip():
            response = "I notice you sent an empty input. How can I help you today?"
        # Simple decision tree based on input content
        elif "identity" in text_input.lower():
            response = "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in text_input.lower():
            response = "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        elif "how" in text_input.lower():
            response = "I process information through a heartbeat-driven, queue-managed system with controlled concurrency."
        else:
            # Split only if there is content
            first_word = text_input.split()[0] if text_input.split() else "this topic"
            response = f"I've processed your input about {first_word} through my biomimetic architecture."
        
        # Add response to item
        item.add_response("brainstem", response)
        
        # Update stage for next processing
        item.update_stage("response_filtering")
        return True
    
    def filter_response(self, item):
        response = item.responses.get("brainstem", "")
        self.logger.log(f"[Brainstem] Filtering response: {response[:30]}...")
        
        # Simulate processing delay
        time.sleep(self.processing_delay / 2)
        
        # In a real system, this would apply safety filters, etc.
        filtered_response = response
        
        item.add_response("filter", filtered_response)
        
        # Update stage for next processing
        item.update_stage("prepare_output")
        return True
    
    def prepare_output(self, item):
        response = item.responses.get("filter", "")
        self.logger.log(f"[Brainstem] Preparing output: {response[:30]}...")
        
        # Simulate processing delay
        time.sleep(self.processing_delay / 3)
        
        # In a real system, this would format the response for the output channel
        item.complete(final_response=response)
        return True
    
    def pulse(self, beat_count):
        """Handle system pulse."""
        if beat_count % 10 == 0:
            print(f"[Brainstem] System pulse {beat_count}")
    
    def register_processors(self):
        """Register processing functions with the queue manager."""
        if not self.queue_manager:
            print("[Brainstem] No queue manager available")
            return False
        
        # Register processors for different stages
        self.queue_manager.register_processor("input_processing", self.process_input)
        self.queue_manager.register_processor("response_filtering", self.filter_response)
        self.queue_manager.register_processor("prepare_output", self.prepare_output)
        
        # Register completion callback
        self.queue_manager.register_completion_callback(self.on_item_completion)
        
        print("[Brainstem] Registered processors with queue manager")
        return True
    
    def on_item_completion(self, item, success=True):
        if success and item.final_response:
            self.logger.log(f"[Brainstem] Item {item.item_id} completed with response: {item.final_response}")
            if self.body:
                self.body.route_signal(
                    source="brainstem",
                    target="mouth",
                    payload={
                        "type": "speak",
                        "data": {"response": item.final_response}
                    }
                )
    
    def receive_signal(self, source, payload):
        message_type = payload.get("type", "")
        
        if message_type == "process_input":
            user_input = payload.get("data", {}).get("input", "")
            
            # Create and queue the processing item
            if self.queue_manager:
                item_id = self.queue_manager.process_user_input(user_input)
                print(f"[Brainstem] Queued input with ID: {item_id}")
                
        return True
    
    def register_with_router(self, router):
        return {
            "name": "Brainstem",
            "type": "processor",
            "capabilities": ["input_processing", "response_filtering", "prepare_output"]
        }
    
    def ping(self):
        # Simulate a real health check (could add logic here)
        print("[Brainstem] Ping received.")
        return True

class Ears:
    """Input component for the biomimetic system"""
    def __init__(self, body=None, logger=None):
        self.body = body
        self.logger = logger
        print("[Ears] Input system initialized")
    
    def receive(self, input_text):
        """Receive user input and route it to the brainstem."""
        if self.logger:
            self.logger.log(f"[Ears] Received: {input_text}")
        
        if self.body:
            # Route the input to the brainstem
            self.body.route_signal(
                source="ears",
                target="brainstem",
                payload={
                    "type": "process_input",
                    "data": {"input": input_text}
                }
            )
    
    def register_with_router(self, router):
        return {"name": "Ears", "type": "input", "capabilities": ["receive"]}
    
    def ping(self):
        print("[Ears] Ping received.")
        return True

class Mouth:
    """Output component for the biomimetic system"""
    def __init__(self, logger=None):
        self.logger = logger
        self.available = True  # Availability flag for health checks
        print("[Mouth] Output system initialized")
    
    def speak(self, message):
        """Output a message to the user."""
        if self.logger:
            self.logger.log(f"[Mouth] Speaking: {message}")
        print(f"\n[System] {message}\n")
    
    def receive_signal(self, source, payload):
        """Handle signals from other components."""
        message_type = payload.get("type", "")
        
        if message_type == "speak":
            response = payload.get("data", {}).get("response", "")
            self.speak(response)
        
        return True
    
    def register_with_router(self, router):
        return {"name": "Mouth", "type": "output", "capabilities": ["speak"]}
    
    def ping(self):
        print("[Mouth] Ping received and " + ("responding!" if self.available else "NOT responding!"))
        return self.available
    
    def process(self, prompt):
        response = f"Mouth response to: {prompt}"
        self.speak(response)
        return response

class BackupMouth:
    """Backup output component"""
    def __init__(self, logger=None):
        self.logger = logger
        self.available = True
        print("[BackupMouth] Output system initialized")
        
    def speak(self, message):
        if self.logger:
            self.logger.log(f"[BackupMouth] Speaking: {message}")
        print(f"[BackupMouth] {message}")
    
    def register_with_router(self, router):
        return {"name": "BackupMouth", "type": "output", "capabilities": ["speak"]}
    
    def ping(self):
        print("[BackupMouth] Ping received and " + ("responding!" if self.available else "NOT responding!"))
        return self.available
    
    def process(self, prompt):
        response = f"BackupMouth response to: {prompt}"
        self.speak(response)
        return response

class MathOrgan:
    """Specialized component for math processing"""
    def __init__(self, logger=None):
        self.logger = logger
        if logger:
            logger.log("[MathOrgan] Math processing organ initialized")
    
    def register_with_router(self, router):
        return {"name": "MathOrgan", "type": "processor", "capabilities": ["math", "calculate"]}
    
    def ping(self):
        if self.logger:
            self.logger.log("[MathOrgan] Ping received")
        return True
    
    def process(self, prompt):
        if self.logger:
            self.logger.log(f"[MathOrgan] Processing math request: {prompt}")
          # Simple math operations
        import re
        if "+" in prompt or "add" in prompt.lower() or "sum" in prompt.lower():
            nums = re.findall(r'\d+', prompt)
            if len(nums) >= 2:
                result = int(nums[0]) + int(nums[1])
                return f"Math result: {nums[0]} + {nums[1]} = {result}"
        elif "solve" in prompt.lower() and "x^2" in prompt:
            return "Math result: x = 2 or x = -2"
        elif "derivative" in prompt.lower() and "sin" in prompt:
            return "Math result: The derivative of sin(x) is cos(x)"
        elif "integrate" in prompt.lower() and "x^2" in prompt:
            return "Math result: The integral of x^2 from 0 to 1 is 1/3"
        
        return f"Math result: Processed '{prompt}' but no specific calculation performed"

class LanguageOrgan:
    """Specialized component for language processing"""
    def __init__(self, logger=None):
        self.logger = logger
        if logger:
            logger.log("[LanguageOrgan] Language processing organ initialized")
    
    def register_with_router(self, router):
        return {"name": "LanguageOrgan", "type": "processor", "capabilities": ["language", "translate"]}
    
    def ping(self):
        if self.logger:
            self.logger.log("[LanguageOrgan] Ping received")
        return True
    
    def process(self, prompt):
        if self.logger:
            self.logger.log(f"[LanguageOrgan] Processing language request: {prompt}")
        
        # Simple translations
        prompt_lower = prompt.lower()
        if "hello" in prompt_lower:
            if "spanish" in prompt_lower:
                return "Language result: 'hello' in Spanish is 'hola'"
            elif "french" in prompt_lower:
                return "Language result: 'hello' in French is 'bonjour'"
            elif "german" in prompt_lower:
                return "Language result: 'hello' in German is 'hallo'"
        elif "goodbye" in prompt_lower:
            if "spanish" in prompt_lower:
                return "Language result: 'goodbye' in Spanish is 'adiós'"
            elif "french" in prompt_lower:
                return "Language result: 'goodbye' in French is 'au revoir'"
            elif "german" in prompt_lower:
                return "Language result: 'goodbye' in German is 'auf Wiedersehen'"
        elif "cat" in prompt_lower:
            if "spanish" in prompt_lower:
                return "Language result: 'cat' in Spanish is 'gato'"
            elif "french" in prompt_lower:
                return "Language result: 'cat' in French is 'chat'"
            elif "german" in prompt_lower:
                return "Language result: 'cat' in German is 'Katze'"
        
        return f"Language result: Processed '{prompt}' but no specific translation performed"

class MemoryOrgan:
    """Specialized component for memory operations"""
    def __init__(self, logger=None):
        self.logger = logger
        self.memory = []
        if logger:
            logger.log("[MemoryOrgan] Memory organ initialized")
    
    def register_with_router(self, router):
        return {"name": "MemoryOrgan", "type": "processor", "capabilities": ["memory", "recall", "remember"]}
    
    def ping(self):
        if self.logger:
            self.logger.log("[MemoryOrgan] Ping received")
        return True
    
    def process(self, prompt):
        if self.logger:
            self.logger.log(f"[MemoryOrgan] Processing memory request: {prompt}")
        
        prompt_lower = prompt.lower()
        if "remember" in prompt_lower:
            # Store the content after "remember" or "remember this:"
            if ":" in prompt_lower:
                content = prompt.split(":", 1)[1].strip()
            else:
                content = prompt
            self.memory.append(content)
            return f"Memory result: Remembered '{content}'"
        
        elif "recall" in prompt_lower or "last" in prompt_lower:
            if not self.memory:
                return "Memory result: No memories stored yet"
            return f"Memory result: Last memory was '{self.memory[-1]}'"
        
        return f"Memory result: Processed '{prompt}' but no specific memory operation performed"

def print_and_log(message, logger=None):
    """Print to console and log to file if logger is provided"""
    print(message)
    if logger:
        with open(logger.log_path, 'a', encoding='utf-8') as f:
            f.write(str(message) + "\n")

def main():
    """Main function to run the demo"""
    # Set up demo logger
    demo_log_path = str(root_dir / "demo_run_log.txt")
    logger = DemoLogger(demo_log_path)
    logger.log("[Demo] Starting new demo run.")
    print_and_log("\nInitializing BlackwallV2 Queue-Driven Architecture\n", logger)
    
    # Create the body (central nervous system)
    body = Body()
    
    # Create the router
    router = Router()
    
    # Create the queue manager
    routing_table_path = str(root_dir / "routing_table.json")
    queue_manager = QueueManager(pulse_capacity=3, routing_table_path=routing_table_path)
    
    # Create central orchestrator
    brainstem = Brainstem(body=body, queue_manager=queue_manager, logger=logger)
    
    # Create input/output components
    ears = Ears(body=body, logger=logger)
    mouth = Mouth(logger=logger)
    backup_mouth = BackupMouth(logger=logger)
    
    # Register components with the body
    body.register_module("brainstem", brainstem)
    body.register_module("ears", ears)
    body.register_module("mouth", mouth)
    body.register_module("backup_mouth", backup_mouth)
    
    # Register organs with the router
    organs = [brainstem, ears, mouth, backup_mouth]
    router.broadcast_registration_request(organs)
    
    # Output routing table status
    logger.log("[Router] Routing table after registration:")
    logger.log(str(router.get_routing_table()))
    
    # Output routing table to a text file for demo
    routing_table_file = str(root_dir / "dynamic_routing_table.txt")
    router.write_routing_table_to_file(routing_table_file)
    
    # Health check
    router.print_status()
    router.ping_organs()
    
    # Register router with body
    body.register_module("router", router)
    
    # Initialize heart for pulse-based processing
    heart = Heart(brainstem=brainstem, queue_manager=queue_manager)
    body.register_module("heart", heart)
      # Connect heart to queue manager
    heart.set_queue_manager(queue_manager)
    
    # Register processors
    brainstem.register_processors()
    
    print_and_log("All components initialized and connected.", logger)
    
    # Start the heart (1 beat per second)
    heart.set_rate(1.0)
    heart.start()
    
    print_and_log("\nSimulating user interaction with queue-driven processing...\n", logger)
    
    # Simulate basic user interaction
    basic_inputs = [
        "Tell me about your identity",
        "What is your purpose",
        "How do you process information",
        "Can you handle multiple requests",
        "What is the T.R.E.E.S. framework"
    ]
    
    logger.log("[Demo] Sending demo inputs...")
    for user_input in basic_inputs:
        logger.log(f"[Demo] User: {user_input}")
        ears.receive(user_input)
        time.sleep(1)  # Small delay between inputs
    
    # Add specialized inputs for testing error handling
    logger.log("[Demo] User: [EMPTY INPUT]")
    ears.receive("")
    time.sleep(1)
    
    # Simulate rapid-fire inputs
    logger.log("\n[Demo] Sending rapid-fire inputs...")
    for i in range(1, 6):
        input_text = f"Rapid input {i}"
        logger.log(f"[Demo] User: {input_text}")
        ears.receive(input_text)
        time.sleep(0.1)  # Very small delay
    
    # Let the system process all queued items
    print_and_log("\nLetting the system process all queued items...", logger)
    time.sleep(10)
    
    # Show queue stats
    print_and_log("\nQueue stats: " + str(queue_manager.get_stats()), logger)
      # Test context-aware routing
    print_and_log("\n=== Context-Aware and Prompt-Driven Routing Demo ===", logger)
    logger.log("\n[Context Routing Demo] Starting context-aware and prompt-driven routing...")
    
    # Create and register specialized organs
    math_organ = MathOrgan(logger)
    language_organ = LanguageOrgan(logger)
    memory_organ = MemoryOrgan(logger)
    
    # Register with the router
    router.register_organ(math_organ, math_organ.register_with_router(router))
    router.register_organ(language_organ, language_organ.register_with_router(router))
    router.register_organ(memory_organ, memory_organ.register_with_router(router))
    
    print_and_log("[Context Routing Demo] Registered specialized organs:", logger)
    print_and_log(f"  - MathOrgan: {math_organ.register_with_router(router)['capabilities']}", logger)
    print_and_log(f"  - LanguageOrgan: {language_organ.register_with_router(router)['capabilities']}", logger)
    print_and_log(f"  - MemoryOrgan: {memory_organ.register_with_router(router)['capabilities']}", logger)
    
    # Test routing with different context prompts
    advanced_prompts = [
        "Integrate x^2 from 0 to 1",
        "Translate 'hello' to French",
        "Recall last input",
        "What is the derivative of sin(x)?",
        "Say 'hello' in Spanish",
        "Remember this: The sky is blue.",
        "Recall last input",
        "Add 42 and 58"
    ]
    
    print_and_log("\nTesting context-aware routing with specialized prompts:", logger)
    for prompt in advanced_prompts:
        print_and_log(f"\n[Context Routing Demo] User: {prompt}", logger)
        organ_id, reason = router.route_by_context(prompt, logger)
        organ = router.get_organ_by_id(organ_id) if organ_id else None
        if organ and hasattr(organ, 'process'):
            response = organ.process(prompt)
            print_and_log(f"[Context Routing Demo] Routed to {router.routing_table[organ_id]['name']} (reason: {reason})", logger)
            print_and_log(f"[Context Routing Demo] Response: {response}", logger)
        else:
            print_and_log(f"[Context Routing Demo] No suitable organ found for: {prompt}", logger)
        time.sleep(0.3)
    
    # Cleanup and finish
    print_and_log("\nStopping the system...", logger)
    heart.stop()
    
    print_and_log("\nDemo complete.", logger)
    logger.log("[Context Routing Demo] Complete.\n")

if __name__ == "__main__":
    main()
