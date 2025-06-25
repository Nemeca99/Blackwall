"""
BlackwallV2 Queue-Driven Demo

This script demonstrates the integration of the heart module with the queue manager,
showing the heartbeat-driven, pulse-limited concurrent processing architecture.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Set up the necessary paths
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"

sys.path.insert(0, str(implementation_dir))
sys.path.insert(0, str(root_dir))

# Import the heart and queue_manager modules
try:
    # Using importlib to load the modules from file path
    import importlib.util
    
    # Import heart module
    heart_spec = importlib.util.spec_from_file_location("heart", root_dir / "heart.py")
    if heart_spec is None:
        raise ImportError(f"Could not find heart module at {root_dir / 'heart.py'}")
    
    heart_module = importlib.util.module_from_spec(heart_spec)
    sys.modules["heart"] = heart_module
    heart_spec.loader.exec_module(heart_module)
    Heart = heart_module.Heart
    
    # Import queue manager module
    qm_spec = importlib.util.spec_from_file_location("queue_manager", root_dir / "queue_manager.py")
    if qm_spec is None:
        raise ImportError(f"Could not find queue manager module at {root_dir / 'queue_manager.py'}")
    
    qm_module = importlib.util.module_from_spec(qm_spec)
    sys.modules["queue_manager"] = qm_module
    qm_spec.loader.exec_module(qm_module)
    QueueManager = qm_module.QueueManager
    ProcessingItem = qm_module.ProcessingItem
    
    # Import router module
    router_spec = importlib.util.spec_from_file_location("router", root_dir / "router.py")
    if router_spec is None:
        raise ImportError(f"Could not find router module at {root_dir / 'router.py'}")
    router_module = importlib.util.module_from_spec(router_spec)
    sys.modules["router"] = router_module
    router_spec.loader.exec_module(router_module)
    Router = router_module.Router
    
    print("\nHeart, QueueManager, and Router modules imported successfully\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Simple component classes for the demo
class Body:
    def __init__(self):
        self.modules = {}
        self.event_handlers = {}
        print("[Body] Initialized")
    
    def register_module(self, name, module):
        self.modules[name] = module
        print(f"[Body] Registered module: {name}")
        return True
    
    def register_handler(self, event_name, module_name, callback):
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append((module_name, callback))
        print(f"[Body] Registered handler for event '{event_name}' from {module_name}")
        return True
    
    def emit_event(self, event_name, data=None):
        if event_name not in self.event_handlers:
            print(f"[Body] No handlers for event: {event_name}")
            return False
        
        print(f"[Body] Emitting event: {event_name}")
        for module_name, callback in self.event_handlers[event_name]:
            try:
                callback(data)
            except Exception as e:
                print(f"[Body] Error in {module_name} handler for {event_name}: {e}")
        
        return True
    
    def route_signal(self, source, target, payload):
        if target in self.modules:
            if hasattr(self.modules[target], "receive_signal"):
                print(f"[Body] Routing signal from {source} to {target}")
                self.modules[target].receive_signal(source, payload)
                return True
        print(f"[Body] Cannot route to {target}")
        return False

class Brainstem:
    def __init__(self, body=None, queue_manager=None, logger=None):
        self.body = body
        self.queue_manager = queue_manager
        self.logger = logger
        self.processing_delay = 0.3  # Simulate processing time
        print("[Brainstem] Initialized")
    
    def process_input(self, item):
        self.logger.log(f"[Brainstem] Processing: {item.content.get('text', '')}")
        
        # Simulate processing delay
        time.sleep(self.processing_delay)
        
        # Simple decision tree based on input content
        if "identity" in item.content.get("text", "").lower():
            response = "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in item.content.get("text", "").lower():
            response = "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        elif "how" in item.content.get("text", "").lower():
            response = "I process information through a heartbeat-driven, queue-managed system with controlled concurrency."
        else:
            response = f"I've processed your input about {item.content.get('text', '').split()[0]} through my biomimetic architecture."
        
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
    def __init__(self, body=None, logger=None):
        self.body = body
        self.logger = logger
        print("[Ears] Input system initialized")
    
    def receive(self, text):
        self.logger.log(f"[Ears] Received: {text}")
        
        # Route to brainstem for processing
        if self.body:
            self.body.route_signal(
                source="ears",
                target="brainstem",
                payload={
                    "type": "process_input",
                    "data": {"input": text}
                }
            )
        
        return True
    
    def register_with_router(self, router):
        return {
            "name": "Ears",
            "type": "input",
            "capabilities": ["receive"]
        }
    
    def ping(self):
        print("[Ears] Ping received.")
        return True

class Mouth:
    def __init__(self, logger=None):
        self.logger = logger
        self.available = True
        print("[Mouth] Output system initialized")
    def speak(self, text):
        self.logger.log(f"[Mouth] Speaking: {text}")
        return text
    
    def register_with_router(self, router):
        return {"name": "Mouth", "type": "output", "capabilities": ["speak"]}
    
    def ping(self):
        # Simulate Mouth being unavailable every other ping
        import random
        self.available = random.choice([True, False])
        status = "responding!" if self.available else "NOT responding!"
        self.logger.log(f"[Mouth] Ping received and {status}")
        return self.available

class BackupMouth:
    def __init__(self, logger=None):
        self.logger = logger
        self.available = True
    def speak(self, text):
        self.logger.log(f"[BackupMouth] Speaking: {text}")
        return text
    def register_with_router(self, router):
        return {"name": "BackupMouth", "type": "output", "capabilities": ["speak"]}
    def ping(self):
        self.logger.log("[BackupMouth] Ping received and responding!")
        return self.available

# Add a simple logger for the demo
class DemoLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write("Demo Log\n=======\n")
    def log(self, message):
        print(message)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(message + "\n")

def main():
    print("\nInitializing BlackwallV2 Queue-Driven Architecture\n")
    # Set up demo logger first
    demo_log_path = str(root_dir / "demo_run_log.txt")
    logger = DemoLogger(demo_log_path)
    logger.log("[Demo] Starting new demo run.")
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
    
    # Add a test organ to demonstrate dynamic registration
    class TestOrgan:
        def __init__(self, logger):
            self.logger = logger
        def register_with_router(self, router):
            return {"name": "TestOrgan", "type": "test", "capabilities": ["test_action"]}
        def ping(self):
            self.logger.log("[TestOrgan] Ping received.")
            return True
    test_organ = TestOrgan(logger)
    organs.append(test_organ)
    
    router.broadcast_registration_request(organs)
    logger.log("[Router] Routing table after registration:")
    logger.log(str(router.get_routing_table()))
    # Output routing table to a text file for demo
    routing_table_file = str(root_dir / "dynamic_routing_table.txt")
    router.write_routing_table_to_file(routing_table_file)
    # Demo: print organ status and health check
    router.print_status()
    logger.log("[Router] Health check results:")
    # Capture health check output
    import io, sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    router.ping_organs()
    health_output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    logger.log(health_output.strip())
    # Register the router with the body
    body.register_module("router", router)
    # Create the heart to drive the system
    heart = Heart(brainstem=brainstem, body=body, queue_manager=queue_manager)
    body.register_module("heart", heart)
    
    # Connect heart to queue manager for pulse-limited processing
    heart.set_queue_manager(queue_manager)
    
    # Register processors with the queue manager
    brainstem.register_processors()
    
    print("\nAll components initialized and connected.\n")
    
    # Start the heart with faster rate for the demo
    heart.set_rate(1.0)
    heart.start()  # Start in background
    
    print("\nSimulating user interaction with queue-driven processing...\n")
    
    # Give the heart a chance to start beating
    time.sleep(1)
    
    # Simulate multiple concurrent user inputs to demonstrate queue management
    inputs = [
        "Tell me about your identity",
        "What is your purpose",
        "How do you process information",
        "Can you handle multiple requests",
        "What is the T.R.E.E.S. framework",
        "How does your biomimetic architecture work",
        "Tell me about pulse capacity",
        "",  # Edge case: empty input
        "x" * 500,  # Edge case: very long input
    ]
    logger.log("[Demo] Sending demo inputs...")
    for user_input in inputs:
        logger.log(f"[Demo] User: {user_input if user_input else '[EMPTY INPUT]'}")
        ears.receive(user_input)
        time.sleep(0.5)
    
    # Rapid-fire inputs
    logger.log("[Demo] Sending rapid-fire inputs...")
    for i in range(5):
        user_input = f"Rapid input {i+1}"
        logger.log(f"[Demo] User: {user_input}")
        ears.receive(user_input)
    
    # Let the system process through the queue
    print("\nLetting the system process all queued items...")
    time.sleep(10)
    
    print("\nQueue stats:", queue_manager.get_stats())
    
    # Send a few more inputs with more delay
    additional_inputs = [
        "How many items per heartbeat can you process",
        "What happens if the queue is full",
        "How does the heart control the flow of information"
    ]
    
    print("\nSending a few more inputs with delay...")
    for user_input in additional_inputs:
        print(f"\nUser: {user_input}")
        ears.receive(user_input)
        time.sleep(3)  # More delay to show processing in real time
    
    # Let the system run a bit longer to show heart cycles
    print("\nLetting the system continue to run for a while...")
    time.sleep(5)
    
    print("\nFinal queue stats:", queue_manager.get_stats())
    
    # Stop the heart
    print("\nStopping the system...")
    heart.stop()
    
    print("\nDemo complete.")

    # === Advanced Demo Scenarios ===
    logger.log("\n[Advanced Demo] Starting advanced scenarios...")

    # 1. Dynamic Organ Removal/Addition
    logger.log("[Advanced Demo] Unregistering BackupMouth...")
    # Find BackupMouth's organ_id
    backup_mouth_id = None
    for oid, info in router.get_routing_table().items():
        if info['name'] == 'BackupMouth':
            backup_mouth_id = oid
            break
    if backup_mouth_id:
        router.unregister_organ(backup_mouth_id)
        logger.log(f"[Advanced Demo] BackupMouth unregistered (ID: {backup_mouth_id})")
    else:
        logger.log("[Advanced Demo] BackupMouth not found in routing table!")
    router.write_routing_table_to_file(routing_table_file)
    time.sleep(1)
    # Re-register BackupMouth
    logger.log("[Advanced Demo] Re-registering BackupMouth...")
    new_id = router.register_organ(backup_mouth, backup_mouth.register_with_router(router))
    logger.log(f"[Advanced Demo] BackupMouth re-registered (ID: {new_id})")
    router.write_routing_table_to_file(routing_table_file)
    time.sleep(1)

    # 2. Organ Capability Change
    logger.log("[Advanced Demo] Changing TestOrgan's capabilities at runtime...")
    # Find TestOrgan's organ_id
    test_organ_id = None
    for oid, info in router.get_routing_table().items():
        if info['name'] == 'TestOrgan':
            test_organ_id = oid
            break
    if test_organ_id:
        # Change capabilities
        router.routing_table[test_organ_id]['capabilities'] = ['test_action', 'dynamic_capability']
        logger.log(f"[Advanced Demo] TestOrgan capabilities updated: {router.routing_table[test_organ_id]['capabilities']}")
    else:
        logger.log("[Advanced Demo] TestOrgan not found in routing table!")
    router.write_routing_table_to_file(routing_table_file)
    time.sleep(1)

    # 3. Advanced Routing (Load Balancing)
    logger.log("[Advanced Demo] Registering ExtraMouth for load balancing...")
    class ExtraMouth:
        def __init__(self, logger):
            self.logger = logger
            self.available = True
        def speak(self, text):
            self.logger.log(f"[ExtraMouth] Speaking: {text}")
            return text
        def register_with_router(self, router):
            return {"name": "ExtraMouth", "type": "output", "capabilities": ["speak"]}
        def ping(self):
            self.logger.log("[ExtraMouth] Ping received and responding!")
            return self.available
    extra_mouth = ExtraMouth(logger)
    organs.append(extra_mouth)
    extra_mouth_id = router.register_organ(extra_mouth, extra_mouth.register_with_router(router))
    logger.log(f"[Advanced Demo] ExtraMouth registered (ID: {extra_mouth_id})")
    router.write_routing_table_to_file(routing_table_file)
    time.sleep(1)
    # Simulate load balancing by routing to all output organs in round-robin
    output_organs = router.find_organs_by_capability('speak')
    logger.log(f"[Advanced Demo] Output organs for load balancing: {output_organs}")
    for i in range(6):
        oid = output_organs[i % len(output_organs)]
        organ = router.get_organ_by_id(oid)
        logger.log(f"[Advanced Demo] Routing output to {router.routing_table[oid]['name']} (ID: {oid})")
        if hasattr(organ, 'speak'):
            organ.speak(f"Load balancing test message {i+1}")
        time.sleep(0.2)

    # 4. Health Check Failure/Recovery
    logger.log("[Advanced Demo] Simulating health check failure and recovery...")
    # Simulate ExtraMouth becoming unavailable
    extra_mouth.available = False
    router.ping_organs()
    logger.log("[Advanced Demo] ExtraMouth set to unavailable. Health check performed.")
    time.sleep(1)
    # Recover ExtraMouth
    extra_mouth.available = True
    router.ping_organs()
    logger.log("[Advanced Demo] ExtraMouth recovered. Health check performed.")
    time.sleep(1)

    # 5. Stress Test: Rapid organ changes and high task volume
    logger.log("[Advanced Demo] Stress test: rapid organ registration/unregistration and high input volume...")
    for i in range(3):
        temp_organ = ExtraMouth(logger)
        temp_id = router.register_organ(temp_organ, temp_organ.register_with_router(router))
        logger.log(f"[Advanced Demo] Temp organ registered (ID: {temp_id})")
        time.sleep(0.1)
        router.unregister_organ(temp_id)
        logger.log(f"[Advanced Demo] Temp organ unregistered (ID: {temp_id})")
    # Rapid-fire inputs
    for i in range(10):
        user_input = f"Stress input {i+1}"
        logger.log(f"[Advanced Demo] User: {user_input}")
        ears.receive(user_input)
        time.sleep(0.1)
    logger.log("[Advanced Demo] Stress test complete.\n")
    time.sleep(3)
    # Final routing table and health check
    router.write_routing_table_to_file(routing_table_file)
    router.ping_organs()
    logger.log("[Advanced Demo] Final routing table and health check complete.")
    # === End Advanced Demo ===

    # Add specialized organs for context-aware routing
    class MathOrgan:
        def __init__(self, logger):
            self.logger = logger
        def register_with_router(self, router):
            return {"name": "MathOrgan", "type": "processor", "capabilities": ["math"]}
        def ping(self):
            self.logger.log("[MathOrgan] Ping received.")
            return True
        def process(self, prompt):
            self.logger.log(f"[MathOrgan] Processing math: {prompt}")
            return f"[MathOrgan] (simulated) Math result for: {prompt}"
    class LanguageOrgan:
        def __init__(self, logger):
            self.logger = logger
        def register_with_router(self, router):
            return {"name": "LanguageOrgan", "type": "processor", "capabilities": ["language"]}
        def ping(self):
            self.logger.log("[LanguageOrgan] Ping received.")
            return True
        def process(self, prompt):
            self.logger.log(f"[LanguageOrgan] Processing language: {prompt}")
            return f"[LanguageOrgan] (simulated) Language result for: {prompt}"
    class MemoryOrgan:
        def __init__(self, logger):
            self.logger = logger
            self.memory = []
        def register_with_router(self, router):
            return {"name": "MemoryOrgan", "type": "processor", "capabilities": ["memory"]}
        def ping(self):
            self.logger.log("[MemoryOrgan] Ping received.")
            return True
        def process(self, prompt):
            if "recall" in prompt.lower() or "last input" in prompt.lower():
                result = self.memory[-1] if self.memory else "No memory."
                self.logger.log(f"[MemoryOrgan] Recalling: {result}")
                return f"[MemoryOrgan] Recall: {result}"
            else:
                self.memory.append(prompt)
                self.logger.log(f"[MemoryOrgan] Memorized: {prompt}")
                return f"[MemoryOrgan] Memorized: {prompt}"
    math_organ = MathOrgan(logger)
    language_organ = LanguageOrgan(logger)
    memory_organ = MemoryOrgan(logger)
    organs.extend([math_organ, language_organ, memory_organ])
    # Register with body for possible direct routing
    body.register_module("math_organ", math_organ)
    body.register_module("language_organ", language_organ)
    body.register_module("memory_organ", memory_organ)

    logger.log("\nAll components initialized and connected, including specialized organs.\n")
    
    # === Final Demo: Context-Aware Routing with Specialized Organs ===
    logger.log("\n[Final Demo] Simulating context-aware routing with specialized organs...\n")
    
    # Simulate user inputs for specialized tasks
    specialized_inputs = [
        "Calculate 2 + 2",
        "Translate 'hello' to Spanish",
        "Remember my last input",
        "What is the capital of France?",
        "Solve the equation x^2 - 4 = 0",
        "Who wrote 'To be, or not to be'?",
        "Recall my last input",
        "Define the term 'biomimetic'",
        "What is 5 * 6?",
        "Translate 'goodbye' to French"
    ]
    
    for user_input in specialized_inputs:
        logger.log(f"[User] {user_input}")
        ears.receive(user_input)
        time.sleep(1)
    
    # Let the system process
    logger.log("\n[Final Demo] Letting the system process specialized tasks...\n")
    time.sleep(10)
    
    # Final stats and routing table
    stats_str = str(queue_manager.get_stats())
    logger.log("\n[Final Demo] Queue stats: " + stats_str)
    router.write_routing_table_to_file(routing_table_file)
    logger.log("[Final Demo] Routing table written to file.")
    
    # Health check
    logger.log("\n[Final Demo] Performing health check on all organs...")
    router.ping_organs()
    logger.log("[Final Demo] Health check complete.")
    
    print("\n=== Final Demo complete ===")

    # === Context-Aware and Prompt-Driven Routing Demo ===
    logger.log("\n[Context Routing Demo] Starting context-aware and prompt-driven routing...")
    advanced_prompts = [
        "Integrate x^2 from 0 to 1",
        "Translate 'hello' to French",
        "Recall last input",
        "What is the derivative of sin(x)?",
        "Say 'hello' in Spanish",
        "Remember this: The sky is blue.",
        "Recall last input",
        "Add 42 and 58",
        "Translate 'cat' to German",
        "What is the sum of 7 and 8?",
        "What was my last message?"
    ]
    for prompt in advanced_prompts:
        logger.log(f"[Context Routing Demo] User: {prompt}")
        organ_id, reason = router.route_by_context(prompt, logger)
        organ = router.get_organ_by_id(organ_id) if organ_id else None
        if organ and hasattr(organ, 'process'):
            response = organ.process(prompt)
            logger.log(f"[Context Routing Demo] Routed to {router.routing_table[organ_id]['name']} (reason: {reason}). Response: {response}")
        else:
            logger.log(f"[Context Routing Demo] No suitable organ found for: {prompt}")
        time.sleep(0.3)
    logger.log("[Context Routing Demo] Complete.\n")

if __name__ == "__main__":
    main()
