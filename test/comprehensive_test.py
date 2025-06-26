"""
BlackwallV2 Comprehensive System Test

This script runs a complete end-to-end test of the integrated BlackwallV2 system,
including Dream Cycle, Fragment Integration, and LLM capabilities.

Usage:
    python comprehensive_test.py [--llm] [--real-memory]
"""

import os
import sys
import time
import json
import argparse
import logging
from datetime import datetime
from pathlib import Path
import threading

# Add parent directory to path for imports
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Parse command line arguments
parser = argparse.ArgumentParser(description='BlackwallV2 Comprehensive System Test')
parser.add_argument('--llm', action='store_true', help='Enable LLM integration testing')
parser.add_argument('--real-memory', action='store_true', help='Use real memory instead of test data')
args = parser.parse_args()

# Configure logging
log_dir = parent_dir / "log"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"comprehensive_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Import core components
try:
    from root.body import Body
    from root.brainstem import Brainstem
    from root.heart import Heart
    from root.router import Router
    from root.dream_manager import DreamManager
    from root.fragment_manager import FragmentManager
    from root.Left_Hemisphere import ShortTermMemory
    from root.Right_Hemisphere import LongTermMemory
    
    # Import LLM components if requested
    if args.llm:
        from llm_integration.llm_interface import LLMInterface
        from llm_integration.enhanced_dream_manager import EnhancedDreamManager
        
    logging.info("Core modules imported successfully")
except ImportError as e:
    logging.error(f"Error importing core modules: {e}")
    sys.exit(1)

class TestResult:
    """Store and report test results."""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failures = []
        
    def record_pass(self, test_name):
        self.total += 1
        self.passed += 1
        logging.info(f"✓ PASS: {test_name}")
        
    def record_fail(self, test_name, reason):
        self.total += 1
        self.failed += 1
        self.failures.append((test_name, reason))
        logging.error(f"✗ FAIL: {test_name} - {reason}")
        
    def record_skip(self, test_name, reason):
        self.total += 1
        self.skipped += 1
        logging.warning(f"⚠ SKIP: {test_name} - {reason}")
        
    def summary(self):
        logging.info("\n" + "=" * 60)
        logging.info(f"TEST SUMMARY: {self.passed}/{self.total} passed ({self.failed} failed, {self.skipped} skipped)")
        
        if self.failures:
            logging.info("\nFAILURES:")
            for name, reason in self.failures:
                logging.info(f"  - {name}: {reason}")
        
        logging.info("=" * 60)
        
        return self.failed == 0

class ComprehensiveSystemTest:
    """Run comprehensive tests on the BlackwallV2 system."""
    
    def __init__(self, use_llm=False, use_real_memory=False):
        self.use_llm = use_llm
        self.use_real_memory = use_real_memory
        self.results = TestResult()
        self.components = {}
        self.memory_path = None
        
        if use_real_memory:
            self.memory_path = parent_dir / "memlong" / "ltm_buffer.json"
            logging.info(f"Using real memory from: {self.memory_path}")
        else:
            logging.info("Using test memory data")
            
        # Initialize test inputs
        self.test_inputs = [
            "Calculate the derivative of x^2 + 3x + 2", 
            "What security measures should we implement?",
            "Can you remember what I asked earlier?",
            "Let's create something beautiful together",
            "Translate this document into French"
        ]
            
    def setup(self):
        """Initialize the system components."""
        logging.info("Setting up system components...")
        
        try:
            # Core system components
            self.components['body'] = Body()
            self.components['heart'] = Heart()
            self.components['ltm'] = LongTermMemory()
            self.components['stm'] = ShortTermMemory()
            self.components['router'] = Router()
            self.components['fragment_manager'] = FragmentManager()
            
            # LLM integration if enabled
            if self.use_llm:
                self.components['llm_interface'] = LLMInterface()
                self.components['dream_manager'] = EnhancedDreamManager(
                    long_term_memory=self.components['ltm'],
                    heart=self.components['heart'],
                    body=self.components['body'],
                    llm_interface=self.components['llm_interface']
                )
                logging.info("LLM integration enabled")
            else:
                self.components['dream_manager'] = DreamManager(
                    long_term_memory=self.components['ltm'],
                    heart=self.components['heart'],
                    body=self.components['body']
                )
            
            # Brainstem (central coordinator)
            self.components['brainstem'] = Brainstem(
                short_term_memory=self.components['stm'], 
                long_term_memory=self.components['ltm'],
                router=self.components['router'],
                heart=self.components['heart'],
                dream_manager=self.components['dream_manager'],
                fragment_manager=self.components['fragment_manager']
            )
            
            # Load memories if real memory path was provided
            if self.use_real_memory and self.memory_path.exists():
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    memories = json.load(f)
                    for memory in memories:
                        self.components['ltm'].add_memory(memory)
                logging.info(f"Loaded {len(memories)} memories from file")
            else:
                # Add test memories
                for i in range(1, 16):
                    tag = ["language", "history", "science", "art", "math"][i % 5]
                    self.components['ltm'].add_memory({
                        "content": f"Test memory {i} about {tag}",
                        "tags": [tag],
                        "timestamp": datetime.now().timestamp() - i * 3600
                    })
                    logging.info(f"Added memory: {tag} - Test memory {i} about {tag}")
            
            self.results.record_pass("System setup")
            return True
            
        except Exception as e:
            self.results.record_fail("System setup", str(e))
            return False
    
    def test_system_initialization(self):
        """Test that all components initialize properly."""
        try:
            # Register components with body
            for name, component in self.components.items():
                if hasattr(component, 'register_with_body'):
                    component.register_with_body(self.components['body'])
            
            # Check registrations
            registered_modules = self.components['body'].registered_modules
            expected_modules = ['brainstem', 'heart', 'ltm', 'stm', 'dream_manager', 'fragment_manager']
            
            for module in expected_modules:
                if module not in registered_modules:
                    self.results.record_fail("Module registration", f"Module '{module}' not registered with body")
                    return False
            
            self.results.record_pass("System initialization")
            return True
            
        except Exception as e:
            self.results.record_fail("System initialization", str(e))
            return False
    
    def test_fragment_activation(self):
        """Test fragment activation and dominance calculations."""
        try:
            fragment_manager = self.components['fragment_manager']
            
            # Initial state check
            initial_levels = fragment_manager.get_activation_levels()
            if 'Lyra' not in initial_levels or 'Blackwall' not in initial_levels:
                self.results.record_fail("Fragment activation", "Core fragments missing")
                return False
                
            # Test activation adjustments
            fragment_manager.adjust_fragment('Obelisk', 20)
            levels = fragment_manager.get_activation_levels()
            if levels['Obelisk'] <= initial_levels['Obelisk']:
                self.results.record_fail("Fragment activation", "Fragment level not increased")
                return False
                
            # Test dominant fragment calculation
            dominant = fragment_manager.get_dominant_fragment()
            logging.info(f"Dominant fragment after adjustment: {dominant}")
            
            # Reset levels
            fragment_manager.reset_to_default()
            
            self.results.record_pass("Fragment activation")
            return True
            
        except Exception as e:
            self.results.record_fail("Fragment activation", str(e))
            return False
    
    def test_dream_cycle(self):
        """Test the dream cycle memory consolidation."""
        try:
            dream_manager = self.components['dream_manager']
            ltm = self.components['ltm']
            
            # Get initial memory count
            initial_count = len(ltm.get_all_memories())
            logging.info(f"Initial memory count: {initial_count}")
            
            # Force a dream cycle
            logging.info("Forcing dream cycle...")
            dream_manager.force_dream_cycle()
            
            # Check for consolidated memories
            final_count = len(ltm.get_all_memories())
            consolidated = [m for m in ltm.get_all_memories() if m.get('tags', []) and 'consolidated_memory' in m.get('tags', [])]
            
            logging.info(f"Final memory count: {final_count}")
            logging.info(f"Consolidated memories: {len(consolidated)}")
            
            if len(consolidated) == 0 and initial_count > 5:
                self.results.record_fail("Dream cycle", "No memory consolidation occurred")
                return False
                
            self.results.record_pass("Dream cycle")
            return True
            
        except Exception as e:
            self.results.record_fail("Dream cycle", str(e))
            return False
    
    def test_fragment_routing(self):
        """Test fragment-aware routing."""
        try:
            router = self.components['router']
            fragment_manager = self.components['fragment_manager']
            
            # Create test organs for routing
            test_organs = {
                'math_organ': {'capabilities': ['math', 'calculation']},
                'lang_organ': {'capabilities': ['language', 'translation']},
                'security_organ': {'capabilities': ['security', 'validation']}
            }
            
            for name, organ in test_organs.items():
                router.register_organ(name, organ)
            
            # Test default routing
            math_organs = router.find_organs_with_capability('math')
            if 'math_organ' not in math_organs:
                self.results.record_fail("Fragment routing", "Basic capability routing failed")
                return False
            
            # Activate Blackwall (security) fragment and check routing priority
            fragment_manager.adjust_fragment('Blackwall', 30)
            fragment_manager.analyze_input("We need to ensure security and protect the system")
            
            # Route a security-related request
            security_organs = router.find_organs_with_capability('security')
            if 'security_organ' not in security_organs:
                self.results.record_fail("Fragment routing", "Security routing failed")
                return False
                
            # Reset fragments
            fragment_manager.reset_to_default()
            
            # Clean up test organs
            for name in test_organs:
                router.unregister_organ(name)
                
            self.results.record_pass("Fragment routing")
            return True
            
        except Exception as e:
            self.results.record_fail("Fragment routing", str(e))
            return False
    
    def test_llm_integration(self):
        """Test LLM integration if enabled."""
        if not self.use_llm:
            self.results.record_skip("LLM integration", "LLM testing not enabled")
            return True
            
        try:
            llm_interface = self.components['llm_interface']
            enhanced_dm = self.components['dream_manager']
            
            # Test connection to LLM
            test_prompt = "Generate a very brief system status report"
            response = llm_interface.query(test_prompt)
            
            if not response or len(response) < 10:
                self.results.record_fail("LLM integration", "Failed to get meaningful response from LLM")
                return False
                
            # Test insight generation
            test_memories = [
                {"content": "The sky is blue because of Rayleigh scattering", "tags": ["science"]},
                {"content": "Water appears blue due to selective absorption of light", "tags": ["science"]}
            ]
            
            insights = enhanced_dm.generate_insights(test_memories)
            if not insights:
                self.results.record_fail("LLM integration", "Failed to generate insights")
                return False
                
            self.results.record_pass("LLM integration")
            return True
            
        except Exception as e:
            self.results.record_fail("LLM integration", str(e))
            return False
    
    def test_full_processing_pipeline(self):
        """Test the complete system with an input through the whole pipeline."""
        try:
            for i, test_input in enumerate(self.test_inputs):
                logging.info(f"\nTesting input {i+1}/{len(self.test_inputs)}: \"{test_input}\"")
                
                # Process through fragment manager first
                self.components['fragment_manager'].analyze_input(test_input)
                dominant = self.components['fragment_manager'].get_dominant_fragment()
                logging.info(f"Fragment analysis result: dominant fragment is {dominant}")
                
                # Process through brainstem
                self.components['brainstem'].process_input(test_input)
                
                # Check that the input was added to memory
                recent_memories = self.components['stm'].get_recent_memories(1)
                if not recent_memories or test_input not in str(recent_memories[0]):
                    logging.warning(f"Input may not have been properly stored in memory")
            
            self.results.record_pass("Full processing pipeline")
            return True
            
        except Exception as e:
            self.results.record_fail("Full processing pipeline", str(e))
            return False
    
    def run_all_tests(self):
        """Run all tests and report results."""
        logging.info("\n" + "=" * 60)
        logging.info("STARTING COMPREHENSIVE BLACKWALLV2 SYSTEM TESTS")
        logging.info("=" * 60)
        
        if not self.setup():
            logging.error("Setup failed, cannot proceed with tests")
            return False
        
        # Core tests
        self.test_system_initialization()
        self.test_fragment_activation()
        self.test_dream_cycle()
        self.test_fragment_routing()
        
        # Optional LLM test
        self.test_llm_integration()
        
        # Final full-pipeline test
        self.test_full_processing_pipeline()
        
        # Report results
        success = self.results.summary()
        
        return success

if __name__ == "__main__":
    test = ComprehensiveSystemTest(use_llm=args.llm, use_real_memory=args.real_memory)
    success = test.run_all_tests()
    sys.exit(0 if success else 1)
