"""
Optimized Fragment Routing System - Performance Enhancement for BlackwallV2

This module implements an optimized version of the fragment routing system,
focusing on improved performance for routing decisions, faster keyword analysis,
and more efficient signal handling.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
from collections import defaultdict

# Constants
DEFAULT_FRAGMENT_BLEND = {
    "Lyra": 50.0,
    "Blackwall": 50.0,
    "Nyx": 30.0,
    "Obelisk": 30.0,
    "Seraphis": 30.0,
    "Velastra": 30.0,
    "Echoe": 30.0
}

# Pre-build the routing bias lookup as a nested dictionary for O(1) lookup
ROUTING_BIAS = {
    "Lyra": {"general_processing": 2.0},
    "Blackwall": {"security": 2.0, "validation": 1.5},
    "Nyx": {"creativity": 2.0, "exploration": 1.5},
    "Obelisk": {"math": 2.0, "logic": 1.5, "structure": 1.2},
    "Seraphis": {"language": 2.0, "empathy": 1.8, "emotion": 1.5},
    "Velastra": {"art": 2.0, "insight": 1.5, "creativity": 1.2},
    "Echoe": {"memory": 2.0, "history": 1.5, "continuity": 1.2}
}

# Pre-build the keyword dictionary for fast text analysis
FRAGMENT_KEYWORDS = {
    "Lyra": ["balance", "harmony", "center", "core", "integrate"],
    "Blackwall": ["protect", "security", "guard", "shield", "safety"],
    "Nyx": ["explore", "discover", "free", "autonomy", "independence"],
    "Obelisk": ["logic", "math", "structure", "analyze", "calculate"],
    "Seraphis": ["feel", "emotion", "empathy", "compassion", "human"],
    "Velastra": ["create", "imagine", "wonder", "curiosity", "possibility"],
    "Echoe": ["remember", "reflect", "history", "pattern", "connection"]
}

# Create an inverted index for fast keyword lookup
KEYWORD_TO_FRAGMENT = {}
for fragment, keywords in FRAGMENT_KEYWORDS.items():
    for keyword in keywords:
        KEYWORD_TO_FRAGMENT[keyword] = fragment


class OptimizedFragmentManager:
    """
    Optimized version of the FragmentManager, with performance enhancements
    for fragment routing, keyword analysis, and signal handling.
    """
    
    def __init__(self, 
                 router=None, 
                 body=None,
                 logger=None,
                 fragment_config_path=None,
                 cache_size=100):
        """
        Initialize the OptimizedFragmentManager.
        
        Args:
            router: The Router instance for integration with routing
            body: The Body instance for system-wide signaling
            logger: Optional logger for recording fragment activities
            fragment_config_path: Path to fragment profiles JSON file
            cache_size: Size of the routing decision cache
        """
        self.router = router
        self.body = body
        self.logger = logger
        self.cache_size = cache_size
        
        # Set default fragment activation levels
        self.fragment_activations = DEFAULT_FRAGMENT_BLEND.copy()
        
        # Track activation history - limit size for memory efficiency
        self.activation_history = []
        self.max_history = 1000  # Limit history to prevent unbounded growth
        
        # Cache for routing decisions to avoid recalculation
        self.routing_cache = {}
        
        # Timestamp for cache invalidation
        self.last_fragment_change = time.time()
        
        # Determine fragment profiles path
        if not fragment_config_path:
            implementation_dir = Path(__file__).resolve().parent.parent
            fragment_config_path = os.path.join(
                implementation_dir, 
                "personality", 
                "fragment_profiles_and_blends.json"
            )
        
        # Load fragment profiles
        self.fragment_profiles = self._load_fragment_profiles(fragment_config_path)
        
        # Keep track of dominant fragment
        self._update_dominant_fragment()
        
        # Pre-compute active fragments for faster routing
        self.active_fragments = self._get_active_fragments()
        
        # Signal handlers mapped to functions for O(1) lookup
        self.signal_handlers = {
            'input_text': self._handle_input_text,
            'adjust_fragments': self._handle_adjust_fragments,
            'get_fragments': self._handle_get_fragments,
            'reset_fragments': self._handle_reset_fragments
        }
        
    def _load_fragment_profiles(self, config_path: str) -> Dict[str, Any]:
        """
        Load fragment profiles from JSON file with better error handling.
        
        Args:
            config_path: Path to fragment profiles JSON file
            
        Returns:
            Dict containing fragment profiles and blend rules
        """
        default_profiles = {
            "fragments": {
                name: {
                    "style": "balanced",
                    "focus": "general",
                    "values": ["balance", "integration"],
                    "voice": "neutral"
                } for name in DEFAULT_FRAGMENT_BLEND.keys()
            }
        }
        
        if not os.path.exists(config_path):
            if self.logger:
                self.logger.warning(f"Fragment profiles not found at {config_path}, using defaults")
            return default_profiles
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict) or "fragments" not in data:
                    if self.logger:
                        self.logger.warning("Invalid fragment profile format, using defaults")
                    return default_profiles
                return data
        except (json.JSONDecodeError, IOError) as e:
            if self.logger:
                self.logger.error(f"Error loading fragment profiles: {e}")
            return default_profiles
    
    def _update_dominant_fragment(self) -> str:
        """
        Update and return the currently dominant fragment.
        Optimized to avoid multiple iterations through fragments.
        
        Returns:
            str: Name of dominant fragment
        """
        max_activation = 0.0
        dom_fragment = "Lyra"  # Default to Lyra
        
        # Single pass to find the dominant fragment
        for fragment, activation in self.fragment_activations.items():
            if activation > max_activation:
                max_activation = activation
                dom_fragment = fragment
        
        self.dominant_fragment = dom_fragment
        return self.dominant_fragment
    
    def _get_active_fragments(self, threshold=10.0) -> Dict[str, float]:
        """
        Get fragments with activation levels above threshold.
        This helps optimize routing by ignoring low-activation fragments.
        
        Args:
            threshold: Minimum activation level to consider a fragment active
            
        Returns:
            Dict of active fragments and their activation levels
        """
        return {f: a for f, a in self.fragment_activations.items() if a > threshold}
    
    def get_activation_levels(self) -> Dict[str, float]:
        """
        Get current fragment activation levels.
        
        Returns:
            Dict[str, float]: Fragment name to activation level mapping
        """
        return self.fragment_activations.copy()
    
    def get_dominant_fragment(self) -> str:
        """
        Get the currently dominant fragment.
        
        Returns:
            str: Name of dominant fragment
        """
        return self.dominant_fragment
    
    def adjust_fragment_levels(self, adjustments: Dict[str, float]) -> Dict[str, float]:
        """
        Adjust fragment activation levels with optimized implementation.
        
        Args:
            adjustments: Dict mapping fragment names to adjustment values
            
        Returns:
            Dict[str, float]: Updated activation levels
        """
        # Check if there are any actual adjustments
        if not adjustments:
            return self.fragment_activations.copy()
        
        # Apply adjustments with bounds checking
        for fragment, adjustment in adjustments.items():
            if fragment in self.fragment_activations:
                self.fragment_activations[fragment] = max(0.0, min(100.0, 
                    self.fragment_activations[fragment] + adjustment
                ))
        
        # Log the adjustment - limit history size
        timestamp = datetime.now().isoformat()
        self.activation_history.append({
            "timestamp": timestamp,
            "adjustments": adjustments,
            "result": self.fragment_activations.copy()
        })
        
        # Trim history if needed
        if len(self.activation_history) > self.max_history:
            self.activation_history = self.activation_history[-self.max_history:]
        
        # Update dominant fragment and active fragments
        self._update_dominant_fragment()
        self.active_fragments = self._get_active_fragments()
        
        # Mark timestamp for cache invalidation
        self.last_fragment_change = time.time()
        self.routing_cache.clear()  # Clear cache on fragment changes
        
        # Signal change if body is available
        if self.body:
            self.body.route_signal("fragment_manager", "brainstem", {
                "type": "fragment_change",
                "timestamp": timestamp,
                "dominant_fragment": self.dominant_fragment,
                "activation_levels": self.fragment_activations.copy()
            })
            
        return self.fragment_activations.copy()
    
    def reset_to_default(self) -> Dict[str, float]:
        """
        Reset fragment activation levels to default.
        
        Returns:
            Dict[str, float]: Default activation levels
        """
        self.fragment_activations = DEFAULT_FRAGMENT_BLEND.copy()
        self._update_dominant_fragment()
        self.active_fragments = self._get_active_fragments()
        self.routing_cache.clear()  # Clear cache on reset
        self.last_fragment_change = time.time()
        
        if self.body:
            self.body.route_signal("fragment_manager", "brainstem", {
                "type": "fragment_reset",
                "timestamp": datetime.now().isoformat(),
                "dominant_fragment": self.dominant_fragment,
                "activation_levels": self.fragment_activations.copy()
            })
            
        return self.fragment_activations.copy()
    
    def analyze_input_for_fragments(self, input_text: str) -> Dict[str, float]:
        """
        Analyze input text to determine relevant fragment adjustments.
        Optimized for performance using pre-built keyword index.
        
        Args:
            input_text: Text to analyze
            
        Returns:
            Dict[str, float]: Suggested fragment adjustments
        """
        input_lower = input_text.lower()
        
        # Use defaultdict to avoid checking if key exists
        adjustments = defaultdict(float)
        
        # Use the inverted index for faster lookup
        for keyword, fragment in KEYWORD_TO_FRAGMENT.items():
            if keyword in input_lower:
                adjustments[fragment] += 5.0
        
        return dict(adjustments)  # Convert back to regular dict
    
    def modify_routing_by_fragments(self, capability: str, organs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Modify routing decisions based on fragment activation levels.
        Optimized with caching and early-exit strategies.
        
        Args:
            capability: The capability being requested
            organs: List of organs that provide the capability
            
        Returns:
            List[Dict]: Organs sorted by fragment-weighted priority
        """
        # Early exit for empty inputs
        if not organs or not capability:
            return organs
            
        # Check cache first - use frozenset of organ IDs for immutable key
        cache_key = (capability, frozenset(org.get('id', id(org)) for org in organs))
        if cache_key in self.routing_cache:
            return self.routing_cache[cache_key]
        
        # Create weighted scores for each organ - preallocate list
        scored_organs = []
        
        # Use only active fragments for scoring to reduce unnecessary computation
        active_fragments = self.active_fragments
        
        for organ in organs:
            base_score = 1.0
            weighted_score = base_score
            
            # Apply fragment biases to relevant capabilities - only check active fragments
            for fragment, activation in active_fragments.items():
                # Get bias dict for this fragment
                bias_dict = ROUTING_BIAS.get(fragment, {})
                
                # Check if this fragment has a bias for this capability
                capability_bias = bias_dict.get(capability)
                if capability_bias:
                    # Apply weighted bias
                    fragment_weight = activation / 100.0
                    bias_effect = fragment_weight * capability_bias
                    weighted_score += bias_effect
            
            # Apply health score if available - use get with default for safety
            health_score = organ.get('health', 1.0)
            if isinstance(health_score, (int, float)):
                weighted_score *= health_score
            
            scored_organs.append({
                "organ": organ,
                "score": weighted_score
            })
            
        # Sort by score in descending order
        scored_organs.sort(key=lambda x: x["score"], reverse=True)
        
        # Extract just the organs in sorted order
        result = [item["organ"] for item in scored_organs]
        
        # Cache the result for future lookups - limit cache size
        if len(self.routing_cache) >= self.cache_size:
            # Simple strategy: clear cache when it gets too large
            self.routing_cache = {}
        
        self.routing_cache[cache_key] = result
        return result
    
    def integrate_with_router(self):
        """
        Integrate with the router to enable fragment-aware routing.
        Uses method reference caching for better performance.
        """
        if not self.router:
            return False
            
        # Store the original find_organs_by_capability method
        if not hasattr(self.router, 'original_find_organs_by_capability'):
            self.router.original_find_organs_by_capability = self.router.find_organs_by_capability
            
            # Create an optimized wrapper method with built-in profiling
            def fragment_aware_find_organs(capability):
                start_time = time.time()
                
                # Get organs from original method
                organs = self.router.original_find_organs_by_capability(capability)
                
                # Apply fragment-based weighting
                result = self.modify_routing_by_fragments(capability, organs)
                
                end_time = time.time()
                if self.logger and end_time - start_time > 0.01:  # Log only if taking significant time
                    self.logger.debug(f"Fragment routing for '{capability}' took {(end_time-start_time)*1000:.2f}ms")
                
                return result
                
            # Replace the router's method with our wrapper
            self.router.find_organs_by_capability = fragment_aware_find_organs
            
            return True
        return False
    
    def restore_router(self):
        """
        Restore the router's original routing method.
        """
        if not self.router:
            return False
            
        if hasattr(self.router, 'original_find_organs_by_capability'):
            self.router.find_organs_by_capability = self.router.original_find_organs_by_capability
            delattr(self.router, 'original_find_organs_by_capability')
            return True
        return False
    
    # Signal handling with function mapping for better performance
    def _handle_input_text(self, signal):
        text = signal.get('content', '')
        adjustments = self.analyze_input_for_fragments(text)
        if adjustments:
            self.adjust_fragment_levels(adjustments)
        return {
            'status': 'processed',
            'adjustments': adjustments,
            'fragments': self.fragment_activations
        }
        
    def _handle_adjust_fragments(self, signal):
        adjustments = signal.get('adjustments', {})
        if adjustments:
            self.adjust_fragment_levels(adjustments)
        return {
            'status': 'adjusted',
            'fragments': self.fragment_activations
        }
        
    def _handle_get_fragments(self, signal):
        return {
            'status': 'success',
            'fragments': self.fragment_activations,
            'dominant': self.dominant_fragment
        }
        
    def _handle_reset_fragments(self, signal):
        self.reset_to_default()
        return {
            'status': 'reset',
            'fragments': self.fragment_activations
        }
    
    def receive_signal(self, signal):
        """Handle signals with optimized dispatch."""
        if not isinstance(signal, dict):
            return {'status': 'invalid_signal_format'}
        
        # Get signal type with fallback
        signal_type = signal.get('type') or signal.get('command')
        
        if not signal_type:
            return {'status': 'unknown_signal'}
            
        # Use function map for O(1) handler lookup
        handler = self.signal_handlers.get(signal_type)
        if handler:
            return handler(signal)
            
        return {'status': 'unknown_signal'}

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            self.body = body
            result = body.register_module("fragment_manager", self)
            if self.logger:
                self.logger.info("[OptimizedFragmentManager] Registered with body system")
            return result
        return False
    
    def get_fragment_activation_levels(self):
        """
        Get the current activation levels of all fragments.
        
        Returns:
            Dict mapping fragment names to their activation levels (0.0-100.0)
        """
        return self.fragment_activations.copy()
    
    def get_metrics(self):
        """
        Get performance metrics for the fragment manager.
        
        Returns:
            Dict with performance metrics
        """
        return {
            "cache_size": len(self.routing_cache),
            "cache_capacity": self.cache_size,
            "active_fragments": len(self.active_fragments),
            "history_size": len(self.activation_history),
            "last_fragment_change": self.last_fragment_change
        }


# Test function if run directly
def test_fragment_manager():
    """Test OptimizedFragmentManager functionality."""
    print("Testing OptimizedFragmentManager")
    fm = OptimizedFragmentManager()
    
    print("Default fragment activations:")
    for fragment, level in fm.get_activation_levels().items():
        print(f"  {fragment}: {level}")
    
    print("\nDominant fragment:", fm.get_dominant_fragment())
    
    print("\nAdjusting fragment levels...")
    fm.adjust_fragment_levels({"Obelisk": 30.0, "Nyx": -10.0})
    
    print("Updated fragment activations:")
    for fragment, level in fm.get_activation_levels().items():
        print(f"  {fragment}: {level}")
    
    print("\nDominant fragment:", fm.get_dominant_fragment())
    
    print("\nTesting input analysis...")
    test_input = "I need to calculate the sum of these numbers logically."
    start_time = time.time()
    adjustments = fm.analyze_input_for_fragments(test_input)
    end_time = time.time()
    
    print(f"Input: '{test_input}'")
    print(f"Analysis time: {(end_time-start_time)*1000:.2f}ms")
    print("Suggested adjustments:")
    for fragment, adj in adjustments.items():
        print(f"  {fragment}: {adj:+.1f}")
    
    # Test routing performance
    print("\nTesting routing performance...")
    mock_organs = [
        {"id": "organ1", "name": "Test Organ 1", "capabilities": ["math"], "health": 0.9},
        {"id": "organ2", "name": "Test Organ 2", "capabilities": ["math"], "health": 0.8},
        {"id": "organ3", "name": "Test Organ 3", "capabilities": ["math"], "health": 1.0},
    ]
    
    start_time = time.time()
    for _ in range(1000):
        sorted_organs = fm.modify_routing_by_fragments("math", mock_organs)
    end_time = time.time()
    
    print(f"Routing performance: {(end_time-start_time)*1000:.2f}ms for 1000 iterations")
    print(f"Average: {(end_time-start_time)/1000*1000:.3f}ms per routing decision")
    
    # Check metrics
    print("\nFragment Manager Metrics:")
    metrics = fm.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_fragment_manager()
