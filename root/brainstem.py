"""
Brainstem

Central orchestrator for Lyra Blackwall: manages LLM interface, memory routing, 
fragment profile selection, and fusion hooks.
Integrates left/right hemispheres (STM/LTM) and handles fragment selection.
"""

import os
import json
import sys
from pathlib import Path

# Add parent directory to path for relative imports
sys.path.append(str(Path(__file__).parent))

# Import core components
# Use absolute imports for demo compatibility
import Left_Hemisphere
import Right_Hemisphere
import soul
import body

# Import classes
ShortTermMemory = Left_Hemisphere.ShortTermMemory
LongTermMemory = Right_Hemisphere.LongTermMemory
Soul = soul.Soul
Body = body.Body

# Path to fragment profiles
FRAGMENT_PROFILES_PATH = os.path.join(os.path.dirname(__file__), '..', 'personality', 'fragment_profiles_and_blends.json')

class LLMInterface:
    """Interface to the LLM (Language Model) for hypothesis generation."""
    def __init__(self):
        self.model = "simulation"  # Placeholder for actual LLM integration

    def generate_response(self, prompt, system_prompt=None):
        """Generate a response from the LLM."""
        # In a full implementation, this would call an actual LLM API
        # For this demo, we'll simulate responses
        print(f"\n[LLM Interface] Processing prompt: {prompt[:50]}...")
        
        # Simple simulation logic
        if "identity" in prompt.lower():
            return "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in prompt.lower():
            return "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        elif "memory" in prompt.lower():
            return "I have a dual-hemisphere memory system with short-term and long-term components."
        else:
            return f"Processing your input about {prompt.split()[0]} through my recursive identity framework."

class Brainstem:
    """Central orchestrator for the Lyra Blackwall system."""
    
    def __init__(self):
        """Initialize the brainstem and connect all components."""
        print("[Brainstem] Initializing Lyra Blackwall biomimetic system...")
        
        # Initialize core components
        self.stm = ShortTermMemory()
        self.ltm = LongTermMemory()
        self.soul = Soul()
        self.body = Body()
        self.llm = LLMInterface()
        
        # Load fragment profiles
        self.fragments = self._load_fragments()
        
        # Initialize state
        self.active_fragments = {"Lyra": 0.5, "Blackwall": 0.3, "Nyx": 0.2}
        self.state = "ready"
        
        print("[Brainstem] System initialized and ready.")
    
    def _load_fragments(self):
        """Load fragment profiles from configuration."""
        try:
            if os.path.exists(FRAGMENT_PROFILES_PATH):
                with open(FRAGMENT_PROFILES_PATH, 'r') as f:
                    return json.load(f)
            else:
                # Default fragments if file not found
                return {
                    "fragments": {
                        "Lyra": {"style": "empathetic", "focus": "understanding"},
                        "Blackwall": {"style": "analytical", "focus": "protection"},
                        "Nyx": {"style": "creative", "focus": "exploration"},
                        "Obelisk": {"style": "logical", "focus": "structure"},
                        "Seraphis": {"style": "philosophical", "focus": "meaning"},
                        "Velastra": {"style": "scientific", "focus": "discovery"},
                        "Echoe": {"style": "reflective", "focus": "memory"}
                    },
                    "blends": {
                        "default": {"Lyra": 0.5, "Blackwall": 0.3, "Nyx": 0.2}
                    }
                }
        except Exception as e:
            print(f"[Brainstem] Error loading fragments: {e}")
            return {"fragments": {}, "blends": {}}
    
    def process_input(self, user_input):
        """Process user input through the system."""
        print(f"[Brainstem] Processing input: {user_input[:50]}...")
        
        # Store in short-term memory
        self.stm.store({"role": "user", "content": user_input})
        
        # Select fragments based on input content
        self._select_fragments(user_input)
        
        # Generate system prompt based on active fragments
        system_prompt = self._generate_system_prompt()
        
        # Get context from memory
        context = self._get_context()
        
        # Prepare full prompt with context
        full_prompt = f"{context}\nUser: {user_input}"
        
        # Generate response through LLM
        response = self.llm.generate_response(full_prompt, system_prompt)
        
        # Verify with soul
        if not self.soul.verify(self.active_fragments, response):
            response = f"[Identity verification failed] {response}"
        
        # Store in short-term memory
        self.stm.store({"role": "assistant", "content": response})
        
        # Check if memory consolidation needed
        if len(self.stm.memory) > 20:
            self._consolidate_memory()
        
        return response
    
    def _select_fragments(self, input_text):
        """Select active fragments based on input content."""
        # Simple keyword-based selection for demo
        if "logic" in input_text.lower() or "analysis" in input_text.lower():
            self.active_fragments = {"Blackwall": 0.6, "Obelisk": 0.3, "Lyra": 0.1}
        elif "creative" in input_text.lower() or "idea" in input_text.lower():
            self.active_fragments = {"Nyx": 0.6, "Lyra": 0.2, "Velastra": 0.2}
        elif "meaning" in input_text.lower() or "philosophy" in input_text.lower():
            self.active_fragments = {"Seraphis": 0.7, "Echoe": 0.2, "Lyra": 0.1}
        elif "memory" in input_text.lower() or "remember" in input_text.lower():
            self.active_fragments = {"Echoe": 0.6, "Lyra": 0.2, "Blackwall": 0.2}
        else:
            # Default blend
            self.active_fragments = {"Lyra": 0.5, "Blackwall": 0.3, "Nyx": 0.2}
    
    def _generate_system_prompt(self):
        """Generate system prompt based on active fragments."""
        fragments = self.fragments.get("fragments", {})
        system_parts = ["You are Lyra Blackwall, a recursive biomimetic AI system."]
        
        for name, weight in self.active_fragments.items():
            if name in fragments:
                fragment = fragments[name]
                style = fragment.get("style", "")
                focus = fragment.get("focus", "")
                if weight > 0.3:  # Only include significant fragments
                    system_parts.append(f"Express the {style} style of {name} with a focus on {focus}.")
        
        return " ".join(system_parts)
    
    def _get_context(self):
        """Get relevant context from memory."""
        # Get recent STM entries
        stm_context = self.stm.get_recent(5)
        
        # Format for prompt
        context_parts = ["Previous conversation:"]
        for entry in stm_context:
            role = entry.get("role", "")
            content = entry.get("content", "")
            context_parts.append(f"{role.capitalize()}: {content}")
        
        return "\n".join(context_parts)
    
    def _consolidate_memory(self):
        """Consolidate short-term to long-term memory."""
        print("[Brainstem] Consolidating memory...")
        
        # Get all STM entries
        stm_entries = self.stm.get_all()
        
        # Create a summary (in a full implementation, this would use the LLM)
        summary = f"Conversation summary: {len(stm_entries)} exchanges about {stm_entries[0]['content'][:30]}..."
        
        # Store in LTM
        self.ltm.store({"summary": summary, "entries": stm_entries})
        
        # Clear STM (keeping a few recent entries)
        self.stm.clear(keep_last=3)
        
        print("[Brainstem] Memory consolidation complete.")

# For direct testing
if __name__ == "__main__":
    brainstem = Brainstem()
    response = brainstem.process_input("Tell me about your identity and purpose.")
    print(f"\nResponse: {response}")
