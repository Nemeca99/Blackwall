"""
Demo script to test LLM integration with BlackwallV2

This script demonstrates how to use the Enhanced Brainstem with LLM integration
to generate responses and test the overall functionality. It supports both
interactive mode and batch processing for performance evaluation.

Inspired by the Blackwall pipeline, this demo incorporates:
1. LLM API integration
2. Text formatting and cleaning
3. Batch processing capabilities
4. Performance metrics logging
"""

import os
import sys
import time
import argparse

# Add parent directory to path for importing siblings
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the EnhancedBrainstem
try:
    from llm_integration.enhanced_brainstem import EnhancedBrainstem
except ImportError:
    print("Failed to import EnhancedBrainstem. Make sure the path is correct.")
    sys.exit(1)

def print_colored(text, color="green"):
    """Print colored text to console"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['reset']}")

def interactive_demo():
    """Run an interactive demo of the LLM integration"""
    print_colored("\n===== BlackwallV2 LLM Integration Demo =====\n", "cyan")
    print_colored("Initializing Enhanced Brainstem with LLM integration...", "yellow")
    
    # Initialize the brainstem
    config_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "llm_integration",
        "config.json"
    )
    
    if not os.path.exists(config_path):
        print_colored(f"Config file not found at {config_path}", "red")
        print_colored("Using default configuration", "yellow")
        config_path = None
    
    brain = EnhancedBrainstem(config_path)
    print_colored("Initialization complete!", "green")
    print_colored("\nYou can now interact with the LLM-enhanced BlackwallV2 system.", "cyan")
    print_colored("Type 'exit', 'quit', or 'q' to end the demo.\n", "yellow")
    
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print_colored("Exiting demo.", "cyan")
                break
            
            print_colored("Thinking...", "yellow")
            start_time = time.time()
            response = brain.generate_response(user_input)
            elapsed_time = time.time() - start_time
            
            print_colored(f"\n[Response ({elapsed_time:.2f}s)]:", "magenta")
            print(response)
            print()
            
        except KeyboardInterrupt:
            print_colored("\nInterrupted by user. Exiting demo.", "red")
            break
        except Exception as e:
            print_colored(f"An error occurred: {e}", "red")

def test_llm_connection():
    """Test the LLM connection with a simple query"""
    print_colored("\n===== Testing LLM Connection =====\n", "cyan")
    
    try:
        from llm_integration.llm_interface import LLMInterface
        
        print_colored("Initializing LLM Interface...", "yellow")
        llm = LLMInterface()
        
        print_colored("Sending test query...", "yellow")
        start_time = time.time()
        response = llm.generate_response("Hello, please respond with a brief greeting to confirm the connection is working.")
        elapsed_time = time.time() - start_time
        
        print_colored(f"\n[Response ({elapsed_time:.2f}s)]:", "magenta")
        print(response)
        print()
        
        print_colored("Test complete!", "green")
        return True
    except Exception as e:
        print_colored(f"Test failed: {e}", "red")
        return False

def batch_demo():
    """Run a batch processing demo using test prompts"""
    print_colored("\n===== BlackwallV2 LLM Batch Processing Demo =====\n", "cyan")
    
    try:
        # Import batch processor
        try:
            from llm_integration.batch_processor import BatchProcessor, SAMPLE_TEST_PROMPTS
        except ImportError as e:
            print_colored(f"Failed to import BatchProcessor: {e}", "red")
            return False
        
        print_colored("Initializing Enhanced Brainstem for batch processing...", "yellow")
        
        # Initialize the brainstem
        config_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "llm_integration",
            "config.json"
        )
        
        if not os.path.exists(config_path):
            print_colored(f"Config file not found at {config_path}", "red")
            print_colored("Using default configuration", "yellow")
            config_path = None
        
        from llm_integration.enhanced_brainstem import EnhancedBrainstem
        brain = EnhancedBrainstem(config_path)
        
        print_colored("Initialization complete! Starting batch processing...", "green")
        
        # Initialize batch processor
        processor = BatchProcessor(brain=brain)
        
        # Run a short batch demo
        processor.run_continuous(
            SAMPLE_TEST_PROMPTS,
            num_cycles=2,
            batch_size=3,
            verbose=True
        )
        
        print_colored("\nBatch processing complete!", "green")
        return True
        
    except Exception as e:
        print_colored(f"Batch processing failed: {e}", "red")
        return False

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="BlackwallV2 LLM Integration Demo")
    parser.add_argument("--batch", action="store_true", help="Run batch processing demo")
    parser.add_argument("--interactive", action="store_true", help="Run interactive demo (default)")
    parser.add_argument("--test", action="store_true", help="Only test the LLM connection")
    args = parser.parse_args()
    
    # Default to interactive if nothing is specified
    if not (args.batch or args.interactive or args.test):
        args.interactive = True
    
    # Test LLM connection if requested or required for other modes
    if args.test or args.interactive:
        connection_success = test_llm_connection()
    else:
        connection_success = True
    
    # Run the specified demo mode
    if args.test:
        # Already ran the test, no need to do anything else
        pass
    elif args.batch:
        batch_demo()
    elif args.interactive and connection_success:
        print_colored("\nLLM connection successful! Starting interactive demo...", "green")
        interactive_demo()
    elif args.interactive:
        print_colored("\nLLM connection failed. Please check your configuration.", "red")
        print_colored("Make sure you have set up the LLM provider correctly.", "yellow")
        print_colored("For local LLM servers, ensure the server is running at the configured URL.", "yellow")
