"""
Batch processing for the BlackwallV2 LLM integration.

This module provides utilities for running batch tests with the LLM integration,
gathering performance metrics, and logging results.
"""

import os
import time
import json
import random
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

# Import LLM integration components
try:
    from llm_integration.llm_interface import LLMInterface
    from llm_integration.enhanced_brainstem import EnhancedBrainstem
    from llm_integration.text_utils import clean_text
except ImportError as e:
    print(f"Error importing LLM integration: {e}")
    # Create placeholder classes for type annotations
    class LLMInterface: pass
    class EnhancedBrainstem: pass
    
# Constants
DEFAULT_LOG_DIR = "logs"
DEFAULT_PERFORMANCE_LOG = "llm_performance.log"
DEFAULT_BATCH_SIZE = 5

class BatchProcessor:
    """Process LLM requests in batches and collect metrics"""
    
    def __init__(self, 
                 brain: Optional[EnhancedBrainstem] = None,
                 log_dir: str = DEFAULT_LOG_DIR,
                 fragment_weights_path: Optional[str] = None):
        """
        Initialize the batch processor
        
        Args:
            brain: EnhancedBrainstem instance to use for processing
            log_dir: Directory to store logs
            fragment_weights_path: Path to fragment weights file
        """
        self.brain = brain or EnhancedBrainstem()
        self.log_dir = log_dir
        self.fragment_weights_path = fragment_weights_path
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize performance metrics
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_time": 0,
            "average_time": 0,
            "min_time": float('inf'),
            "max_time": 0,
            "request_times": [],
        }
    
    def run_batch(self, prompts: List[str], 
                  system_prompt: Optional[str] = None, 
                  verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run a batch of prompts through the LLM
        
        Args:
            prompts: List of prompts to process
            system_prompt: Optional system prompt to use for all requests
            verbose: Whether to print progress
            
        Returns:
            List of results with metrics
        """
        if verbose:
            print(f"\n[BatchProcessor] Running batch of {len(prompts)} prompts")
        
        results = []
        batch_start_time = time.time()
        
        for i, prompt in enumerate(prompts):
            if verbose:
                print(f"\n[{i+1}/{len(prompts)}] Processing: {prompt[:50]}...")
            
            try:
                # Process the prompt and track performance
                start_time = time.time()
                response = self.brain.generate_response(prompt, system_prompt)
                elapsed_time = time.time() - start_time
                
                # Update metrics
                self.metrics["total_requests"] += 1
                self.metrics["successful_requests"] += 1
                self.metrics["total_time"] += elapsed_time
                self.metrics["min_time"] = min(self.metrics["min_time"], elapsed_time)
                self.metrics["max_time"] = max(self.metrics["max_time"], elapsed_time)
                self.metrics["request_times"].append(elapsed_time)
                self.metrics["average_time"] = self.metrics["total_time"] / self.metrics["successful_requests"]
                
                result = {
                    "prompt": prompt,
                    "response": response,
                    "time": elapsed_time,
                    "status": "success"
                }
                
                if verbose:
                    print(f"Response (in {elapsed_time:.2f}s):")
                    print(f"---\n{response}\n---")
            
            except Exception as e:
                # Handle errors gracefully
                self.metrics["total_requests"] += 1
                self.metrics["failed_requests"] += 1
                
                result = {
                    "prompt": prompt,
                    "error": str(e),
                    "status": "error"
                }
                
                if verbose:
                    print(f"Error: {e}")
            
            results.append(result)
        
        # Calculate batch metrics
        batch_time = time.time() - batch_start_time
        
        if verbose:
            print(f"\n[BatchProcessor] Batch completed in {batch_time:.2f}s")
            print(f"Average response time: {self.metrics['average_time']:.2f}s")
            print(f"Success rate: {self.metrics['successful_requests']}/{self.metrics['total_requests']}")
        
        # Log the results
        self._log_batch_results(results)
        
        return results
    
    def run_continuous(self, 
                      prompts: List[str], 
                      num_cycles: int = 5, 
                      batch_size: int = DEFAULT_BATCH_SIZE,
                      system_prompt: Optional[str] = None,
                      sleep_between_batches: float = 5.0,
                      verbose: bool = True) -> None:
        """
        Run continuous batch processing for learning and evaluation
        
        Args:
            prompts: List of prompts to sample from
            num_cycles: Number of batch cycles to run
            batch_size: Number of prompts per batch
            system_prompt: Optional system prompt
            sleep_between_batches: Time to sleep between batches
            verbose: Whether to print progress
        """
        if verbose:
            print(f"\n[BatchProcessor] Starting continuous batch processing")
            print(f"Running {num_cycles} cycles of {batch_size} prompts each")
        
        try:
            for cycle in range(num_cycles):
                if verbose:
                    print(f"\n--- Cycle {cycle+1}/{num_cycles} ---")
                
                # Sample random prompts for this batch
                batch_prompts = random.sample(prompts, min(batch_size, len(prompts)))
                
                # Run the batch
                self.run_batch(batch_prompts, system_prompt=system_prompt, verbose=verbose)
                
                # Check if this is the last cycle
                if cycle < num_cycles - 1:
                    if verbose:
                        print(f"Sleeping for {sleep_between_batches}s before next batch...")
                    time.sleep(sleep_between_batches)
        
        except KeyboardInterrupt:
            if verbose:
                print("\n[BatchProcessor] Interrupted by user")
        
        # Save final metrics
        self._log_performance_metrics()
        
        if verbose:
            print("\n[BatchProcessor] Continuous processing complete")
            print(f"Total requests: {self.metrics['total_requests']}")
            print(f"Average response time: {self.metrics['average_time']:.2f}s")
    
    def _log_batch_results(self, results: List[Dict[str, Any]]) -> None:
        """Log batch results to file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(self.log_dir, f"batch_results_{timestamp}.json")
        
        try:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump({
                    "timestamp": timestamp,
                    "results": results,
                    "metrics": {
                        k: v for k, v in self.metrics.items() 
                        if k != "request_times"  # Don't save the full request times array
                    }
                }, f, indent=2)
        except Exception as e:
            print(f"[BatchProcessor] Error logging batch results: {e}")
    
    def _log_performance_metrics(self) -> None:
        """Log performance metrics to file"""
        log_path = os.path.join(self.log_dir, DEFAULT_PERFORMANCE_LOG)
        
        try:
            # Calculate final metrics
            metrics = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_requests": self.metrics["total_requests"],
                "successful_requests": self.metrics["successful_requests"],
                "failed_requests": self.metrics["failed_requests"],
                "average_time": self.metrics["average_time"],
                "min_time": self.metrics["min_time"],
                "max_time": self.metrics["max_time"],
                "success_rate": (
                    self.metrics["successful_requests"] / self.metrics["total_requests"] 
                    if self.metrics["total_requests"] > 0 else 0
                )
            }
            
            # Append to existing log file
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(metrics) + "\n")
        except Exception as e:
            print(f"[BatchProcessor] Error logging metrics: {e}")


# --- Sample test prompts from BlackwallV2 pipeline ---
SAMPLE_TEST_PROMPTS = [
    "What is the TREES framework and how does it work?",
    "Can you explain how UML Calculator processes symbolic mathematics?",
    "I'm feeling lost and don't know what to do next.",
    "What's the relationship between recursion and identity in your model?",
    "How do blackwalls work in the context of AI cognition?",
    "I'm curious about how you integrate memory into your system.",
    "Explain the concept of symbolic compression.",
    "What are the benefits of biomimetic AI architectures?",
    "How does your system handle emotional content?",
    "Tell me about the relationship between T.R.E.E.S. and RIS theory."
]

# Example usage
if __name__ == "__main__":
    print("BatchProcessor demonstration")
    brain = EnhancedBrainstem()
    processor = BatchProcessor(brain=brain)
    processor.run_continuous(
        SAMPLE_TEST_PROMPTS,
        num_cycles=2,
        batch_size=3,
        verbose=True
    )
