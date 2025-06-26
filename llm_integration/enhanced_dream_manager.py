"""
Enhanced Dream Manager with LLM Integration

This module extends the standard Dream Manager with LLM capabilities for:
1. Improved insight generation between memories
2. Symbolic compression using natural language understanding
3. Enhanced memory consolidation with semantic similarity
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime

# Add necessary paths for imports
current_dir = Path(__file__).resolve().parent
root_dir = current_dir.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "llm_integration"))

# Import the base Dream Manager
from root.dream_manager import DreamManager

# Try to import LLM interface
try:
    from llm_integration.llm_interface import LLMInterface
    llm_available = True
except ImportError:
    llm_available = False
    print("LLM interface not available, falling back to simulation")

class EnhancedDreamManager(DreamManager):
    """
    Enhanced Dream Manager with LLM capabilities for improved insight generation,
    symbolic compression, and memory consolidation.
    """
    
    def __init__(self, 
                 long_term_memory=None, 
                 heart=None,
                 body=None,
                 logger=None,
                 llm_config=None):
        """Initialize the Enhanced Dream Manager with LLM support."""
        # Initialize the base class
        super().__init__(long_term_memory, heart, body, logger)
        
        # Set up LLM interface if available
        self.llm = None
        self.llm_available = llm_available
        
        if self.llm_available:
            try:
                self.llm = LLMInterface(config=llm_config)
                self.log_dream_activity("LLM integration enabled for dream cycles", "INFO")
            except Exception as e:
                self.log_dream_activity(f"LLM initialization failed: {e}", "ERROR")
                self.llm_available = False
        
        # Enhanced insight generation stats
        self.insight_stats = {
            "llm_insights_generated": 0,
            "llm_consolidations": 0,
            "semantic_connections": 0,
            "avg_insight_quality": 0.0
        }
    
    def enter_dream_cycle(self) -> bool:
        """
        Enhanced dream cycle with LLM-powered insights and consolidation.
        
        Returns:
            bool: True if dream cycle completed successfully
        """
        if self.is_dreaming:
            self.log_dream_activity("Already in dream cycle", "WARNING")
            return False
            
        self.is_dreaming = True
        start_time = time.time()
        self.log_dream_activity("Entering dream cycle...", "INFO")
        
        # Signal system about dream cycle start
        if self.body:
            self.body.route_signal("dream_manager", "brainstem", {
                "type": "system_event",
                "event": "dream_cycle_start",
                "data": {"timestamp": datetime.now().isoformat()}
            })
        
        # Adjust heart rate if available
        if self.heart:
            self.heart.slow_down_for_dream()
        
        # ----- Begin Enhanced Dream Processing -----
        
        # First perform standard memory consolidation as in the base class
        memories_processed = self._consolidate_memories()
        
        # ENHANCEMENT: Generate insights using LLM if available
        insights_generated = 0
        semantic_connections = 0
        
        if self.llm_available and self.llm:
            insights_generated, semantic_connections = self._generate_llm_insights()
            
        # Update stats
        self.consolidation_stats["total_cycles"] += 1
        self.consolidation_stats["total_memories_processed"] += memories_processed
        self.consolidation_stats["insights_generated"] += insights_generated
        self.consolidation_stats["last_cycle_duration"] = time.time() - start_time
        
        if self.llm_available:
            self.insight_stats["llm_insights_generated"] += insights_generated
            self.insight_stats["semantic_connections"] += semantic_connections
        
        # Save stats
        self._save_stats()
        
        # ----- End Dream Processing -----
        
        # Signal system about dream cycle end
        if self.body:
            self.body.route_signal("dream_manager", "brainstem", {
                "type": "system_event",
                "event": "dream_cycle_end",
                "data": {
                    "timestamp": datetime.now().isoformat(),
                    "duration": time.time() - start_time,
                    "memories_processed": memories_processed,
                    "insights_generated": insights_generated,
                    "semantic_connections": semantic_connections
                }
            })
        
        # Restore heart rate if available
        if self.heart:
            self.heart.restore_rate_after_dream()
        
        self.is_dreaming = False
        self.last_dream_time = time.time()
        
        self.log_dream_activity(f"Dream cycle completed in {time.time() - start_time:.2f} seconds", "INFO")
        return True
    
    def _generate_llm_insights(self) -> Tuple[int, int]:
        """
        Generate insights using LLM by finding relationships between different memory clusters.
        
        Returns:
            Tuple[int, int]: (insights_generated, semantic_connections)
        """
        if not self.llm_available or not self.llm or not self.ltm or not self.ltm.memory:
            return 0, 0
            
        insights_generated = 0
        semantic_connections = 0
        
        # Group memories by tag/topic
        memory_groups = {}
        for mem in self.ltm.memory:
            if isinstance(mem, dict):
                tag = mem.get('tag', 'untagged')
                if tag not in memory_groups:
                    memory_groups[tag] = []
                memory_groups[tag].append(mem)
        
        # Must have at least two memory groups to find connections
        if len(memory_groups) < 2:
            return 0, 0
            
        # Select up to 3 random pairs of memory groups to find connections
        import random
        topics = list(memory_groups.keys())
        pairs_to_analyze = min(3, len(topics) // 2 + 1)
        
        for _ in range(pairs_to_analyze):
            if len(topics) < 2:
                break
                
            topic_a = random.choice(topics)
            topics.remove(topic_a)
            topic_b = random.choice(topics)
            topics.remove(topic_b)
            
            # Generate insight between these two topics
            success, connections = self._llm_analyze_memory_groups(
                topic_a, memory_groups[topic_a],
                topic_b, memory_groups[topic_b]
            )
            
            if success:
                insights_generated += 1
                semantic_connections += connections
        
        return insights_generated, semantic_connections
        
    def _llm_analyze_memory_groups(self, topic_a, memories_a, topic_b, memories_b):
        """
        Use LLM to analyze two memory groups and find connections.
        
        Returns:
            Tuple[bool, int]: (success, num_connections)
        """
        if not memories_a or not memories_b:
            return False, 0
            
        # Create a sample of memories from each group
        sample_a = random.sample(memories_a, min(3, len(memories_a)))
        sample_b = random.sample(memories_b, min(3, len(memories_b)))
        
        # Format memories for the LLM
        memory_text_a = "\n".join([f"- {m.get('content', 'No content')}" for m in sample_a])
        memory_text_b = "\n".join([f"- {m.get('content', 'No content')}" for m in sample_b])
        
        # Prepare the prompt for the LLM
        prompt = f"""
        Analyze these two sets of memories and identify meaningful connections, patterns or insights:

        MEMORIES ABOUT {topic_a.upper()}:
        {memory_text_a}

        MEMORIES ABOUT {topic_b.upper()}:
        {memory_text_b}

        Identify 1-3 specific connections or insights that bridge these memory domains.
        Format your answer as a JSON object with these fields:
        - "connections": [array of connection strings]
        - "reasoning": brief explanation of your thought process
        - "potential_applications": how this insight could be useful
        """
        
        try:
            # Use the LLM to generate insights
            response = self.llm.generate_response(
                prompt=prompt,
                system_prompt="You are an insight generation system that finds meaningful connections between memories."
            )
            
            # Process and store the insight
            try:
                # Try to parse as JSON
                import json
                insight_data = json.loads(response)
                
                # Store the insight in a new memory
                if "connections" in insight_data and insight_data["connections"]:
                    connections = insight_data["connections"]
                    
                    # Create a new memory with the insight
                    insight_memory = {
                        "type": "insight",
                        "tags": [topic_a, topic_b, "connection"],
                        "timestamp": datetime.now().isoformat(),
                        "source": "dream_cycle_llm",
                        "connections": connections,
                        "content": f"Connection between {topic_a} and {topic_b}: {connections[0]}"
                    }
                    
                    if "reasoning" in insight_data:
                        insight_memory["reasoning"] = insight_data["reasoning"]
                        
                    if "potential_applications" in insight_data:
                        insight_memory["potential_applications"] = insight_data["potential_applications"]
                    
                    # Add to memory
                    self.ltm.memory.append(insight_memory)
                    
                    # Log the insight
                    self.log_dream_activity(f"Generated insight between {topic_a} and {topic_b}: {connections[0]}", "INFO")
                    
                    return True, len(connections)
                    
            except Exception as e:
                # If JSON parsing fails, create a simpler memory
                insight_memory = {
                    "type": "insight",
                    "tags": [topic_a, topic_b, "connection"],
                    "timestamp": datetime.now().isoformat(),
                    "source": "dream_cycle_llm",
                    "content": f"Connection between {topic_a} and {topic_b}: {response[:200]}..."
                }
                
                # Add to memory
                self.ltm.memory.append(insight_memory)
                
                # Log the insight
                self.log_dream_activity(f"Generated insight (text format) between {topic_a} and {topic_b}", "INFO")
                
                return True, 1
                
        except Exception as e:
            self.log_dream_activity(f"Error generating LLM insight: {e}", "ERROR")
            return False, 0
