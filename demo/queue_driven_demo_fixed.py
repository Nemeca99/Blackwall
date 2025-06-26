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
import importlib

# Set up the necessary paths
current_dir = Path(__file__).resolve().parent
implementation_dir = current_dir.parent
root_dir = implementation_dir / "root"

sys.path.insert(0, str(implementation_dir))
sys.path.insert(0, str(root_dir))

# Import core modules
try:    Heart = importlib.import_module('heart').Heart
    QueueManager = importlib.import_module('queue_manager').QueueManager
    ProcessingItem = importlib.import_module('queue_manager').ProcessingItem
    Router = importlib.import_module('router').Router
    Body = importlib.import_module('body').Body
    
    print("\nHeart, QueueManager, and Router modules imported successfully\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)
    
class DemoLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        # Create/clear the log file
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"=== BlackwallV2 Demo Log - {datetime.now()} ===\n\n")
    
    def log(self, message):
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(f"{message}\n")

class DemoLogger:
    def __init__(self, log_path):
        self.log_path = log_path
        with open(self.log_path, 'w', encoding='utf-8') as f:
            f.write("Demo Log\n=======\n")
    def log(self, message):
        print(message)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(str(message) + "\n")

def print_and_log(message, logger=None):
    print(message)
    if logger:
        with open(logger.log_path, 'a', encoding='utf-8') as f:
            f.write(str(message) + "\n")

def main():
    # Set up demo logger first
    demo_log_path = str(root_dir / "demo_run_log.txt")
    logger = DemoLogger(demo_log_path)
    print_and_log("\nInitializing BlackwallV2 Queue-Driven Architecture\n", logger)
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
    
    print_and_log("\nAll components initialized and connected.\n", logger)
    
    # Start the heart with faster rate for the demo
    heart.set_rate(1.0)
    heart.start()  # Start in background
    
    print_and_log("\nSimulating user interaction with queue-driven processing...\n", logger)
    
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
    print_and_log("\nLetting the system process all queued items...", logger)
    time.sleep(10)
    
    print_and_log("\nQueue stats: " + str(queue_manager.get_stats()), logger)
    
    # Send a few more inputs with more delay
    additional_inputs = [
        "How many items per heartbeat can you process",
        "What happens if the queue is full",
        "How does the heart control the flow of information"
    ]
    
    print_and_log("\nSending a few more inputs with delay...", logger)
    for user_input in additional_inputs:
        print(f"\nUser: {user_input}")
        ears.receive(user_input)
        time.sleep(3)  # More delay to show processing in real time
    
    # Let the system run a bit longer to show heart cycles
    print_and_log("\nLetting the system continue to run for a while...", logger)
    time.sleep(5)
    
    print_and_log("\nFinal queue stats: " + str(queue_manager.get_stats()), logger)
    
    # Stop the heart
    print_and_log("\nStopping the system...", logger)
    heart.stop()
    
    print_and_log("\nDemo complete.", logger)

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

    # Import and instantiate additional core organs
    import importlib
    heart_mod = importlib.import_module('heart')
    lungs_mod = importlib.import_module('lungs')
    left_mod = importlib.import_module('Left_Hemisphere')
    right_mod = importlib.import_module('Right_Hemisphere')
    HeartReal = heart_mod.Heart
    Lungs = lungs_mod.Lungs
    ShortTermMemory = left_mod.ShortTermMemory
    LongTermMemory = right_mod.LongTermMemory
    # Instantiate and register
    real_heart = HeartReal(brainstem=brainstem, body=body, queue_manager=queue_manager)
    lungs = Lungs()
    stm = ShortTermMemory()
    ltm = LongTermMemory()
    body.register_module("real_heart", real_heart)
    body.register_module("lungs", lungs)
    body.register_module("stm", stm)
    body.register_module("ltm", ltm)
    logger.log("[Demo] Registered Heart, Lungs, STM, and LTM with Body.")
    # Demonstrate routing a signal to each
    body.route_signal("demo", "real_heart", {"type": "set_rate", "data": {"rate": 2.0}})
    body.route_signal("demo", "lungs", {"type": "log", "data": {"entry": "Test log entry from demo."}})
    body.route_signal("demo", "stm", {"type": "store", "data": {"item": {"role": "demo", "content": "STM test entry"}}})
    body.route_signal("demo", "ltm", {"type": "store", "data": {"summary": {"summary": "LTM test summary", "entries": []}}})
    logger.log("[Demo] Sent test signals to Heart, Lungs, STM, and LTM via Body.")
    
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
    
    print_and_log("\n=== Final Demo complete ===", logger)    # === Context-Aware and Prompt-Driven Routing Demo ===
    logger.log("\n[Context Routing Demo] Starting context-aware and prompt-driven routing...")
    
    # Create and register specialized organs
    math_organ = MathOrgan(logger)
    language_organ = LanguageOrgan(logger)
    memory_organ = MemoryOrgan(logger)
    
    # Register with the router
    router.register_organ(math_organ, math_organ.register_with_router(router))
    router.register_organ(language_organ, language_organ.register_with_router(router))
    router.register_organ(memory_organ, memory_organ.register_with_router(router))
    
    logger.log("[Context Routing Demo] Registered specialized organs:")
    logger.log(f"  - {math_organ.__class__.__name__}: {math_organ.register_with_router(router)['capabilities']}")
    logger.log(f"  - {language_organ.__class__.__name__}: {language_organ.register_with_router(router)['capabilities']}")
    logger.log(f"  - {memory_organ.__class__.__name__}: {memory_organ.register_with_router(router)['capabilities']}")
    
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
