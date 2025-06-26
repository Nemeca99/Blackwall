"""
BlackwallV2 Core Components Test Suite

This module provides comprehensive tests for each core component of the BlackwallV2
biomimetic architecture, including individual tests for:

1. Heart (timing mechanism)
2. Brainstem (central orchestrator)
3. Left Hemisphere (Short-Term Memory)
4. Right Hemisphere (Long-Term Memory)
5. Lungs (I/O buffer)
6. Body (communication hub)
7. Fragment Manager
8. Dream Manager

Each component is tested in isolation with mock dependencies where appropriate,
and then tested with its actual dependencies for integration verification.

Usage:
    python test_core_components.py [--component <component_name>]
    
    Optional arguments:
    --component: Test only a specific component (heart, brainstem, stm, ltm, lungs, body, fragment, dream)
    --verbose: Show detailed output for all tests
"""

import os
import sys
import time
import json
import threading
import argparse
import logging
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

# Add parent directory to path for imports
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

# Configure logging
log_dir = parent_dir / "log"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / f"core_components_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Parse command line arguments
parser = argparse.ArgumentParser(description='BlackwallV2 Core Components Test Suite')
parser.add_argument('--component', choices=['heart', 'brainstem', 'stm', 'ltm', 'lungs', 'body', 'fragment', 'dream'],
                   help='Test only a specific component')
parser.add_argument('--verbose', action='store_true', help='Show detailed output for all tests')
args = parser.parse_args()

# Set logging level based on verbosity
if args.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

# Import core components
try:
    from root.body import Body
    from root.brainstem import Brainstem
    from root.heart import Heart
    from root.lungs import Lungs
    from root.Left_Hemisphere import ShortTermMemory
    from root.Right_Hemisphere import LongTermMemory
    from root.fragment_manager import FragmentManager
    from root.dream_manager import DreamManager
    from root.router import Router
    
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


class CoreComponentTests:
    """Tests for all core components of the BlackwallV2 architecture."""
    
    def __init__(self):
        self.results = TestResult()
        self.test_data = {
            "memory_items": [
                {"content": "Test memory 1", "tags": ["test"], "timestamp": datetime.now().timestamp()},
                {"content": "Test memory 2", "tags": ["test"], "timestamp": datetime.now().timestamp()},
                {"content": "Mathematical equation x²+y²=r²", "tags": ["math"], "timestamp": datetime.now().timestamp()},
                {"content": "Security protocol update needed", "tags": ["security"], "timestamp": datetime.now().timestamp()},
                {"content": "Creative writing exercise", "tags": ["art"], "timestamp": datetime.now().timestamp()},
            ],
            "test_inputs": [
                "Calculate the derivative of x^2 + 3x + 2",
                "What security measures should we implement?",
                "Can you remember what I asked earlier?",
                "Let's create something beautiful together",
                "Translate this document into French"
            ]
        }
        self.mocks = {}
        
    def create_mocks(self):
        """Create mock objects for component dependencies."""
        self.mocks = {
            'body': MagicMock(spec=Body),
            'brainstem': MagicMock(spec=Brainstem),
            'heart': MagicMock(spec=Heart),
            'ltm': MagicMock(spec=LongTermMemory),
            'stm': MagicMock(spec=ShortTermMemory),
            'router': MagicMock(spec=Router),
            'fragment_manager': MagicMock(spec=FragmentManager),
            'dream_manager': MagicMock(spec=DreamManager)
        }        # Configure mock behaviors
        self.mocks['body'].register_module = MagicMock(return_value=True)
        self.mocks['body'].route_signal = MagicMock(return_value=True)
        self.mocks['body'].emit_event = MagicMock(return_value=True)
        
        # Only add pulse method if it exists in the real class
        if hasattr(Brainstem, 'pulse'):
            self.mocks['brainstem'].pulse = MagicMock(return_value=True)
        
        # Use the correct method for FragmentManager
        self.mocks['fragment_manager'].analyze_input_for_fragments = MagicMock(return_value={"Blackwall": 0.8})
        self.mocks['fragment_manager'].get_dominant_fragment = MagicMock(return_value="Blackwall")
        
        # Configure Router mock with flexible methods
        router_methods = dir(Router)
        routing_methods = [method for method in router_methods if method.startswith('route') or 'route' in method]
        if 'route' in routing_methods:
            self.mocks['router'].route = MagicMock(return_value=True)
        # Add any other routing methods found
        for method in routing_methods:
            if method != 'route':  # Already added above
                setattr(self.mocks['router'], method, MagicMock(return_value=True))
        
        return self.mocks
        
    def test_heart(self):
        """Test the Heart component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING HEART COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Create mock dependencies
            mock_brainstem = MagicMock()
            mock_body = MagicMock()
            mock_body.register_module = MagicMock(return_value=True)
            mock_body.emit_event = MagicMock(return_value=True)
            
            # Test 1: Basic initialization
            heart = Heart(brainstem=mock_brainstem, body=mock_body)
            if heart.heartbeat_rate != 1.0 or heart.pulse_capacity != 10:
                self.results.record_fail("Heart initialization", "Default parameters not set correctly")
            else:
                self.results.record_pass("Heart initialization")
            
            # Test 2: Heart rate adjustment
            heart.set_rate(0.5)
            if heart.heartbeat_rate != 0.5:
                self.results.record_fail("Heart rate adjustment", "Rate not updated correctly")
            else:
                self.results.record_pass("Heart rate adjustment")
            
            # Test 3: Pulse capacity adjustment
            heart.set_pulse_capacity(20)
            if heart.pulse_capacity != 20:
                self.results.record_fail("Pulse capacity adjustment", "Capacity not updated correctly")
            else:
                self.results.record_pass("Pulse capacity adjustment")
            
            # Test 4: Run a few heartbeats and check brainstem pulses
            heart.start(cycles=5)
            # Verify brainstem was called
            if not mock_brainstem.pulse.called:
                self.results.record_fail("Heart pulse to brainstem", "Brainstem pulse method not called")
            else:
                self.results.record_pass("Heart pulse to brainstem")
            
            # Test 5: Check event emission
            if not mock_body.emit_event.called:
                self.results.record_fail("Heart event emission", "Body emit_event method not called")
            else:
                self.results.record_pass("Heart event emission")
            
            # Test 6: Status reporting
            status = heart.get_status()
            if not isinstance(status, dict) or 'state' not in status:
                self.results.record_fail("Heart status reporting", "Status not returned as expected")
            else:
                self.results.record_pass("Heart status reporting")
                
            # Test 7: Background thread operation
            heart = Heart(brainstem=mock_brainstem, body=mock_body)
            heart.set_rate(0.1)  # Fast rate for testing
            heart.start()  # Start in background
            
            # Wait a moment and check that beats occurred
            time.sleep(0.5)
            initial_count = heart.beat_count
            
            # Wait more time and check for more beats
            time.sleep(0.5)
            if heart.beat_count <= initial_count:
                self.results.record_fail("Heart background operation", "Beat count did not increase")
            else:
                self.results.record_pass("Heart background operation")
                
            # Stop the heart and ensure it's stopped
            heart.stop()
            time.sleep(0.2)
            if heart.alive:
                self.results.record_fail("Heart stop function", "Heart still alive after stop")
            else:
                self.results.record_pass("Heart stop function")
                
            # Test 8: Integration with real Body
            try:
                real_body = Body()
                heart = Heart(brainstem=mock_brainstem, body=real_body)
                heart.set_rate(0.1)
                
                # Register with body - pass body as parameter
                if not heart.register_with_body(body=real_body):
                    self.results.record_fail("Heart-Body integration", "Failed to register with Body")
                else:
                    self.results.record_pass("Heart-Body integration")
                    
                # Run a few heartbeats
                heart.start(cycles=2)
                
                # Clean up
                if heart.thread and heart.thread.is_alive():
                    heart.stop()
            except Exception as e:
                self.results.record_fail("Heart-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("Heart component", str(e))
            
        return True
        
    def test_brainstem(self):
        """Test the Brainstem component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING BRAINSTEM COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Test 1: Basic initialization with default constructor (self-initializes components)
            try:
                brainstem = Brainstem()
                if not brainstem:
                    self.results.record_fail("Brainstem initialization", "Failed to initialize")
                else:
                    self.results.record_pass("Brainstem initialization")
            except Exception as e:
                self.results.record_fail("Brainstem initialization", f"Exception: {str(e)}")
            
            # Create mock dependencies for isolated testing
            mocks = self.create_mocks()
              # Test 2: Pulse handling - check if method exists
            brainstem = Brainstem()  # Create a fresh instance
            if hasattr(brainstem, 'pulse'):
                try:
                    # Call pulse with correct parameter (interval) instead of beat_count
                    result = brainstem.pulse(interval=1.0)
                    if result is not False:  # Some implementations may return None
                        self.results.record_pass("Brainstem pulse handling")
                    else:
                        self.results.record_fail("Brainstem pulse handling", "Pulse returned False")
                except Exception as e:
                    self.results.record_fail("Brainstem pulse handling", str(e))
            else:
                self.results.record_skip("Brainstem pulse handling", "No pulse method")
            
            # Test 3: Process input routing
            try:
                test_input = "Test input for brainstem processing"
                brainstem = Brainstem()  # Create a fresh instance
                
                # Replace fragment manager with mock for testing
                original_fragment_manager = brainstem.fragment_manager
                brainstem.fragment_manager = mocks['fragment_manager']
                
                # Replace router with mock for testing
                original_router = brainstem.router
                brainstem.router = mocks['router']
                
                # Configure mock
                mocks['fragment_manager'].analyze_input_for_fragments.return_value = {"Blackwall": 0.8}
                mocks['fragment_manager'].get_dominant_fragment.return_value = "Blackwall"
                
                if hasattr(brainstem, 'process_input'):
                    result = brainstem.process_input(test_input)
                    if result:
                        self.results.record_pass("Brainstem input processing")
                    else:
                        self.results.record_fail("Brainstem input processing", "Processing returned False")
                        
                    # Verify fragment manager was called to analyze input - check both possible method names
                    if hasattr(mocks['fragment_manager'], 'analyze_input_for_fragments') and mocks['fragment_manager'].analyze_input_for_fragments.called:
                        self.results.record_pass("Brainstem-FragmentManager interaction")
                    elif hasattr(mocks['fragment_manager'], 'analyze_input') and mocks['fragment_manager'].analyze_input.called:
                        self.results.record_pass("Brainstem-FragmentManager interaction")
                    else:
                        self.results.record_fail("Brainstem-FragmentManager interaction", "Fragment manager analyze methods not called")                    
                    # Verify router was used - check if it has a route method first
                    if hasattr(mocks['router'], 'route'):
                        if mocks['router'].route.called:
                            self.results.record_pass("Brainstem-Router interaction")
                        else:
                            self.results.record_fail("Brainstem-Router interaction", "Router not called")
                    else:
                        # The Router is initialized in the Brainstem constructor but might not be
                        # used directly in the process_input method
                        if hasattr(brainstem, 'router') and isinstance(brainstem.router, Router):
                            self.results.record_pass("Brainstem-Router initialization")
                        else:
                            self.results.record_fail("Brainstem-Router initialization", "Router not properly initialized")
                else:
                    self.results.record_skip("Brainstem input processing", "No process_input method")
                
                # Clean up
                brainstem.fragment_manager = original_fragment_manager
                brainstem.router = original_router
            except Exception as e:
                self.results.record_fail("Brainstem input processing", str(e))
              # Test 4: Registration with Body
            try:
                brainstem = Brainstem()  # Create a fresh instance
                
                # Create a real body for registration
                real_body = Body()
                brainstem.body = real_body  # Set the body
                
                # Check if registration method exists
                if hasattr(brainstem, 'register_with_body'):
                    try:
                        result = brainstem.register_with_body()
                        if result:
                            self.results.record_pass("Brainstem-Body registration")
                        else:
                            self.results.record_fail("Brainstem-Body registration", "Registration returned False")
                    except TypeError as e:
                        # Try with body parameter if the first attempt failed with TypeError
                        try:
                            result = brainstem.register_with_body(body=real_body)
                            if result:
                                self.results.record_pass("Brainstem-Body registration")
                            else:
                                self.results.record_fail("Brainstem-Body registration", "Registration returned False")
                        except Exception as e2:
                            self.results.record_fail("Brainstem-Body registration", f"Both attempts failed: {str(e2)}")
                    except Exception as e:
                        self.results.record_fail("Brainstem-Body registration", str(e))
                else:
                    # Check if registration happens in the constructor
                    if "brainstem" in real_body.modules:
                        self.results.record_pass("Brainstem-Body registration (auto registration)")
                    else:
                        self.results.record_skip("Brainstem-Body registration", "No register_with_body method and not auto-registered")
            except Exception as e:
                self.results.record_fail("Brainstem-Body registration", str(e))
            
        except Exception as e:
            self.results.record_fail("Brainstem component", str(e))
            
        return True
        
    def test_left_hemisphere(self):
        """Test the Left_Hemisphere (Short-Term Memory) component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING LEFT HEMISPHERE (STM) COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Test 1: Basic initialization with buffer size
            stm = ShortTermMemory(buffer_size=20)
            if stm.buffer_size != 20:
                self.results.record_fail("STM initialization", "Buffer size not set correctly")
            else:
                self.results.record_pass("STM initialization")
            
            # Test 2: Memory storage
            test_item = {"content": "Test memory", "timestamp": datetime.now().timestamp()}
            result = stm.store(test_item)
            if not result:
                self.results.record_fail("STM memory storage", "Store method returned False")
            else:
                self.results.record_pass("STM memory storage")
            
            # Test 3: Memory retrieval
            recent = stm.get_recent(1)
            if not recent or "Test memory" not in str(recent[0]):
                self.results.record_fail("STM memory retrieval", "Retrieved memory doesn't match stored memory")
            else:
                self.results.record_pass("STM memory retrieval")
            
            # Test 4: Buffer size enforcement
            # Add enough items to exceed buffer size
            for i in range(25):
                stm.store({"content": f"Overflow test {i}", "timestamp": datetime.now().timestamp()})
                
            # Check that buffer size was maintained
            all_memories = stm.get_all()
            if len(all_memories) > 20:
                self.results.record_fail("STM buffer size enforcement", f"Buffer exceeded max size: {len(all_memories)}")
            else:
                self.results.record_pass("STM buffer size enforcement")
            
            # Test 5: Clear function
            stm.clear()
            all_after_clear = stm.get_all()
            if all_after_clear:
                self.results.record_fail("STM clear function", "Memory not cleared properly")
            else:
                self.results.record_pass("STM clear function")
                
            # Test 6: Clear with keep_last parameter
            for i in range(5):
                stm.store({"content": f"Keep test {i}", "timestamp": datetime.now().timestamp()})
            
            stm.clear(keep_last=2)
            remaining = stm.get_all()
            if len(remaining) != 2:
                self.results.record_fail("STM clear with keep_last", f"Expected 2 items, found {len(remaining)}")
            else:
                self.results.record_pass("STM clear with keep_last")
            
            # Test 7: Integration with Body if applicable
            try:
                if hasattr(stm, 'register_with_body'):
                    body = Body()
                    stm.body = body
                    result = stm.register_with_body(body=body)
                    if result:
                        self.results.record_pass("STM-Body integration")
                    else:
                        self.results.record_fail("STM-Body integration", "Registration returned False")
                else:
                    self.results.record_skip("STM-Body integration", "No register_with_body method")
            except Exception as e:
                self.results.record_fail("STM-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("Left Hemisphere (STM) component", str(e))
            
        return True
        
    def test_right_hemisphere(self):
        """Test the Right_Hemisphere (Long-Term Memory) component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING RIGHT HEMISPHERE (LTM) COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Test 1: Basic initialization
            ltm = LongTermMemory()
            if not ltm:
                self.results.record_fail("LTM initialization", "Failed to initialize")
            else:
                self.results.record_pass("LTM initialization")
            
            # Test 2: Memory storage
            test_summary = {"summary": "Test consolidated memory", "timestamp": datetime.now().timestamp()}
            result = ltm.store(test_summary)
            if not result:
                self.results.record_fail("LTM memory storage", "Store method returned False")
            else:
                self.results.record_pass("LTM memory storage")
            
            # Test 3: Memory retrieval (get_all)
            all_memories = ltm.get_all()
            if not all_memories or "Test consolidated memory" not in str(all_memories):
                self.results.record_fail("LTM memory retrieval (get_all)", "Retrieved memories don't include test memory")
            else:
                self.results.record_pass("LTM memory retrieval (get_all)")
            
            # Test 4: Memory search
            search_results = ltm.search("test")
            if not search_results or "Test consolidated memory" not in str(search_results):
                self.results.record_fail("LTM memory search", "Search didn't find test memory")
            else:
                self.results.record_pass("LTM memory search")
            
            # Test 5: Integration with Body if applicable
            try:
                if hasattr(ltm, 'register_with_body'):
                    body = Body()
                    ltm.body = body
                    result = ltm.register_with_body(body=body)
                    if result:
                        self.results.record_pass("LTM-Body integration")
                    else:
                        self.results.record_fail("LTM-Body integration", "Registration returned False")
                else:
                    self.results.record_skip("LTM-Body integration", "No register_with_body method")
            except Exception as e:
                self.results.record_fail("LTM-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("Right Hemisphere (LTM) component", str(e))
            
        return True
        
    def test_lungs(self):
        """Test the Lungs (I/O buffer) component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING LUNGS COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Test 1: Basic initialization
            lungs = Lungs()
            if not lungs:
                self.results.record_fail("Lungs initialization", "Failed to initialize")
            else:
                self.results.record_pass("Lungs initialization")
            
            # Test 2: Check basic methods exist
            if not hasattr(lungs, 'inhale') or not hasattr(lungs, 'exhale'):
                self.results.record_fail("Lungs methods", "Missing inhale or exhale method")
            else:
                self.results.record_pass("Lungs methods")
                
            # Test 3: Test inhale method (even if stubbed)
            try:
                result = lungs.inhale()
                self.results.record_pass("Lungs inhale method")
            except Exception as e:
                self.results.record_fail("Lungs inhale method", str(e))
            
            # Test 4: Test exhale method (even if stubbed)
            try:
                lungs.exhale()
                self.results.record_pass("Lungs exhale method")
            except Exception as e:
                self.results.record_fail("Lungs exhale method", str(e))
                
            # Test 5: Log reading
            if hasattr(lungs, 'read_log'):
                try:
                    logs = lungs.read_log(n=5)
                    self.results.record_pass("Lungs log reading")
                except Exception as e:
                    self.results.record_fail("Lungs log reading", str(e))
            else:
                self.results.record_skip("Lungs log reading", "No read_log method")
                
            # Test 6: Fragment history parsing if applicable
            if hasattr(lungs, 'parse_fragment_history'):
                try:
                    history = lungs.parse_fragment_history(n=5)
                    self.results.record_pass("Lungs fragment history parsing")
                except Exception as e:
                    self.results.record_fail("Lungs fragment history parsing", str(e))
            else:
                self.results.record_skip("Lungs fragment history parsing", "No parse_fragment_history method")
            
            # Test 7: Integration with Body if applicable
            try:
                if hasattr(lungs, 'register_with_body'):
                    body = Body()
                    lungs.body = body
                    result = lungs.register_with_body(body=body)
                    if result:
                        self.results.record_pass("Lungs-Body integration")
                    else:
                        self.results.record_fail("Lungs-Body integration", "Registration returned False")
                else:
                    self.results.record_skip("Lungs-Body integration", "No register_with_body method")
            except Exception as e:
                self.results.record_fail("Lungs-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("Lungs component", str(e))
            
        return True
        
    def test_body(self):
        """Test the Body (communication hub) component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING BODY COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Test 1: Basic initialization
            body = Body()
            if not body:
                self.results.record_fail("Body initialization", "Failed to initialize")
            else:
                self.results.record_pass("Body initialization")
            
            # Test 2: Module registration
            mock_module = MagicMock()
            result = body.register_module("test_module", mock_module)
            if not result or "test_module" not in body.modules:
                self.results.record_fail("Body module registration", "Failed to register module")
            else:
                self.results.record_pass("Body module registration")
            
            # Test 3: Signal routing
            mock_receiver = MagicMock()
            mock_receiver.receive_signal = MagicMock(return_value=True)
            body.register_module("receiver", mock_receiver)
            
            result = body.route_signal("source", "receiver", {"data": "test"})
            if not result or not mock_receiver.receive_signal.called:
                self.results.record_fail("Body signal routing", "Failed to route signal")
            else:
                self.results.record_pass("Body signal routing")
                
            # Test 4: Error handling for nonexistent module
            result = body.route_signal("source", "nonexistent", {"data": "test"})
            if result:  # Should return False for nonexistent module
                self.results.record_fail("Body nonexistent module handling", "Should return False for nonexistent module")
            else:
                self.results.record_pass("Body nonexistent module handling")
                
            # Test 5: Broadcast signal
            mock_receiver1 = MagicMock()
            mock_receiver2 = MagicMock()
            mock_receiver1.receive_signal = MagicMock(return_value=True)
            mock_receiver2.receive_signal = MagicMock(return_value=True)
            
            body.register_module("receiver1", mock_receiver1)
            body.register_module("receiver2", mock_receiver2)
            
            body.broadcast_signal("source", {"broadcast": "test"}, exclude=["receiver2"])
            
            if not mock_receiver1.receive_signal.called:
                self.results.record_fail("Body broadcast signal", "Signal not broadcasted to receiver1")
            elif mock_receiver2.receive_signal.called:  # Should not be called because it's excluded
                self.results.record_fail("Body broadcast exclude", "Signal broadcasted to excluded module")
            else:
                self.results.record_pass("Body broadcast signal")
                
            # Test 6: Event system if applicable
            if hasattr(body, 'emit_event') and hasattr(body, 'register_for_event'):
                event_handler = MagicMock(return_value=True)
                body.register_for_event("test_event", event_handler)
                
                body.emit_event("test_event", {"data": "test"})
                
                if event_handler.called:
                    self.results.record_pass("Body event system")
                else:
                    self.results.record_fail("Body event system", "Event handler not called")
            else:
                self.results.record_skip("Body event system", "Event system not implemented")
            
        except Exception as e:
            self.results.record_fail("Body component", str(e))
            
        return True
        
    def test_fragment_manager(self):
        """Test the FragmentManager component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING FRAGMENT MANAGER COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Create mock dependencies
            mocks = self.create_mocks()
            
            # Test 1: Basic initialization
            fragment_manager = FragmentManager(router=mocks['router'], body=mocks['body'])
            if not fragment_manager:
                self.results.record_fail("FragmentManager initialization", "Failed to initialize")
            else:
                self.results.record_pass("FragmentManager initialization")
            
            # Test 2: Input analysis
            test_inputs = {
                "Calculate the derivative of x^2 + 3x + 2": "Obelisk",  # Math content
                "What security measures should we implement?": "Blackwall",  # Security content
                "Let's create something beautiful together": "Nyx",  # Creative content
                "Tell me about the history of mathematics": "Echoe"  # History content
            }
            
            for input_text, expected_fragment in test_inputs.items():
                try:
                    # Use the correct method name: analyze_input_for_fragments instead of analyze_input
                    fragment_activations = fragment_manager.analyze_input_for_fragments(input_text)
                    
                    # Check that we get valid fragment activations
                    if not fragment_activations or not isinstance(fragment_activations, dict):
                        self.results.record_fail(f"FragmentManager input analysis: '{input_text[:20]}...'", 
                                               f"No valid fragment activations returned")
                    else:
                        self.results.record_pass(f"FragmentManager input analysis: '{input_text[:20]}...'")
                        logging.debug(f"Input: '{input_text}', Expected dominant: {expected_fragment}, Activations: {fragment_activations}")
                        
                    # Check get_dominant_fragment if available
                    if hasattr(fragment_manager, 'get_dominant_fragment'):
                        dominant = fragment_manager.get_dominant_fragment()
                        if not dominant or not isinstance(dominant, str):
                            self.results.record_fail(f"FragmentManager get_dominant_fragment", 
                                                   f"No dominant fragment returned")
                        else:
                            self.results.record_pass(f"FragmentManager get_dominant_fragment")
                except Exception as e:
                    self.results.record_fail(f"FragmentManager input analysis: '{input_text[:20]}...'", str(e))
            
            # Test 3: Fragment activation levels
            if hasattr(fragment_manager, 'get_fragment_activation_levels'):
                try:
                    activation_levels = fragment_manager.get_fragment_activation_levels()
                    if not activation_levels or not isinstance(activation_levels, dict):
                        self.results.record_fail("FragmentManager activation levels", "No valid activation levels returned")
                    else:
                        self.results.record_pass("FragmentManager activation levels")
                except Exception as e:
                    self.results.record_fail("FragmentManager activation levels", str(e))
            else:
                self.results.record_skip("FragmentManager activation levels", "No get_fragment_activation_levels method")
            
            # Test 4: Integration with Body if applicable
            try:
                if hasattr(fragment_manager, 'register_with_body'):
                    body = Body()  # Create real body for integration test
                    fragment_manager.body = body
                    result = fragment_manager.register_with_body(body=body)
                    if result:
                        self.results.record_pass("FragmentManager-Body integration")
                    else:
                        self.results.record_fail("FragmentManager-Body integration", "Registration returned False")
                else:
                    self.results.record_skip("FragmentManager-Body integration", "No register_with_body method")
            except Exception as e:
                self.results.record_fail("FragmentManager-Body integration", str(e))
            
        except Exception as e:
            self.results.record_fail("FragmentManager component", str(e))
            
        return True
        
    def test_dream_manager(self):
        """Test the DreamManager component."""
        logging.info("\n" + "=" * 60)
        logging.info("TESTING DREAM MANAGER COMPONENT")
        logging.info("=" * 60)
        
        try:
            # Create mock dependencies
            mocks = self.create_mocks()
            
            # Test 1: Basic initialization
            dream_manager = DreamManager(
                long_term_memory=mocks['ltm'],
                heart=mocks['heart'],
                body=mocks['body']
            )
            
            if not dream_manager:
                self.results.record_fail("DreamManager initialization", "Failed to initialize")
            else:
                self.results.record_pass("DreamManager initialization")
                
            # Test 2: Dream state management
            if not hasattr(dream_manager, 'is_dreaming'):
                self.results.record_fail("DreamManager dream state", "No is_dreaming attribute")
            else:
                self.results.record_pass("DreamManager dream state")
                
            # Test 3: Memory clustering if implemented
            test_memories = [
                {"content": "Mathematical equation x²+y²=r²", "tags": ["math"], "timestamp": datetime.now().timestamp()},
                {"content": "Solving for x in equation x+5=10", "tags": ["math"], "timestamp": datetime.now().timestamp()},
                {"content": "Security protocol update needed", "tags": ["security"], "timestamp": datetime.now().timestamp()},
                {"content": "Firewall configuration changes", "tags": ["security"], "timestamp": datetime.now().timestamp()},
                {"content": "Creative writing exercise", "tags": ["art"], "timestamp": datetime.now().timestamp()}
            ]
            
            if hasattr(dream_manager, 'cluster_memories'):
                try:
                    clusters = dream_manager.cluster_memories(test_memories)
                    if isinstance(clusters, dict) or isinstance(clusters, list):
                        self.results.record_pass("DreamManager memory clustering")
                    else:
                        self.results.record_fail("DreamManager memory clustering", "Invalid clusters returned")
                except Exception as e:
                    self.results.record_fail("DreamManager memory clustering", str(e))
            else:
                self.results.record_skip("DreamManager memory clustering", "No cluster_memories method")
                
            # Test 4: Dream cycle check
            if hasattr(dream_manager, 'check_dream_cycle'):
                try:
                    # Force last dream time to be old enough to trigger a new dream
                    dream_manager.last_dream_time = 0
                    
                    result = dream_manager.check_dream_cycle()
                    # Just ensure it runs without error, result depends on many factors
                    self.results.record_pass("DreamManager dream cycle check")
                except Exception as e:
                    self.results.record_fail("DreamManager dream cycle check", str(e))
            else:
                self.results.record_skip("DreamManager dream cycle check", "No check_dream_cycle method")
                
            # Test 5: Integration with Body
            try:
                if hasattr(dream_manager, 'register_with_body'):
                    body = Body()
                    result = dream_manager.register_with_body(body=body)
                    if result:
                        self.results.record_pass("DreamManager-Body integration")
                    else:
                        self.results.record_fail("DreamManager-Body integration", "Registration returned False")
                else:
                    self.results.record_skip("DreamManager-Body integration", "No register_with_body method")
            except Exception as e:
                self.results.record_fail("DreamManager-Body integration", str(e))
                
            # Test 6: Integration with real components
            try:
                real_body = Body()
                real_ltm = LongTermMemory()
                real_heart = Heart(body=real_body)
                
                real_dream_manager = DreamManager(
                    long_term_memory=real_ltm,
                    heart=real_heart,
                    body=real_body
                )
                
                # Test registration if applicable
                if hasattr(real_dream_manager, 'register_with_body'):
                    result = real_dream_manager.register_with_body(body=real_body)
                    if result:
                        self.results.record_pass("DreamManager real component integration")
                    else:
                        self.results.record_fail("DreamManager real component integration", "Registration failed")
                else:
                    self.results.record_pass("DreamManager real component integration")
            except Exception as e:
                self.results.record_fail("DreamManager real component integration", str(e))
            
        except Exception as e:
            self.results.record_fail("DreamManager component", str(e))
            
        return True
        
    def run_tests(self, component=None):
        """Run specified or all component tests."""
        logging.info("\n" + "=" * 60)
        logging.info("STARTING BLACKWALLV2 CORE COMPONENT TESTS")
        logging.info("=" * 60)
        
        start_time = time.time()
        
        # Run requested test or all tests
        if component == 'heart':
            self.test_heart()
        elif component == 'brainstem':
            self.test_brainstem()
        elif component == 'stm':
            self.test_left_hemisphere()
        elif component == 'ltm':
            self.test_right_hemisphere()
        elif component == 'lungs':
            self.test_lungs()
        elif component == 'body':
            self.test_body()
        elif component == 'fragment':
            self.test_fragment_manager()
        elif component == 'dream':
            self.test_dream_manager()
        else:
            # Run all tests
            self.test_heart()
            self.test_brainstem()
            self.test_left_hemisphere()
            self.test_right_hemisphere()
            self.test_lungs()
            self.test_body()
            self.test_fragment_manager()
            self.test_dream_manager()
            
        end_time = time.time()
        duration = end_time - start_time
        
        logging.info(f"\nTests completed in {duration:.2f} seconds")
        
        # Report results
        success = self.results.summary()
        
        return success


if __name__ == "__main__":
    tests = CoreComponentTests()
    success = tests.run_tests(component=args.component)
    sys.exit(0 if success else 1)
