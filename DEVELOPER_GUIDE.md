# BlackwallV2 Implementation Guide for Developers

This document provides technical details for developers working on or extending the BlackwallV2 biomimetic AI architecture.

## Architecture Overview

BlackwallV2 implements a biomimetic design that mirrors human cognitive and physiological systems:

```
                                +---------------+
                                |    Soul       |
                                | (Identity)    |
                                +-------+-------+
                                        |
+----------------+             +--------v--------+
|  Left          |             |                 |
|  Hemisphere    <------------->   Brainstem     |
| (Short-Term    |             | (Orchestrator)  |
|  Memory)       |             |                 |
+----------------+             +--------+--------+
                                        |
+----------------+                      |                +--------------+
|  Right         |             +--------v--------+       | Fragments    |
|  Hemisphere    <------------->                 |       | - Lyra       |
| (Long-Term     |             |     Body        |       | - Blackwall  |
|  Memory)       |             | (Communication) <------->- Nyx         |
+----------------+             |                 |       | - Obelisk    |
                              ++-----------------+       | - Seraphis   |
                               |    |      |     |       | - Velastra   |
                               |    |      |     |       | - Echoe      |
                               |    |      |     |       +--------------+
                        +------v+  +v------v+  +v------+
                        | Input |  |Process |  |Output |
                        +-------+  +--------+  +-------+
```

## Core Components

### 1. Brainstem (`brainstem.py`)

The central orchestrator that:
- Manages fragment selection based on input content
- Routes memory between short-term and long-term storage
- Interfaces with LLM for response generation
- Conducts memory consolidation via the Dream Cycle

### 2. Memory System

- **Left Hemisphere** (`Left_Hemisphere.py`): Short-term memory for recent interactions
- **Right Hemisphere** (`Right_Hemisphere.py`): Long-term memory for consolidated information

### 3. Identity System

- **Soul** (`soul.py`): Identity anchor and verification
- **Fragments** (`fragment_profiles_and_blends.json`): Specialized cognitive personas

### 4. Communication System

- **Body** (`body.py`): Central communication hub connecting all components

## Implementation Details

### Fragment Selection Logic

The system selects active fragments based on input content, using a combination of keyword matching and context analysis. Fragment weights determine the cognitive style and focus of the system's response.

```python
def _select_fragments(self, input_text):
    """Select active fragments based on input content."""
    # Example logic - would be more sophisticated in production
    if "logic" in input_text.lower():
        self.active_fragments = {"Blackwall": 0.6, "Obelisk": 0.3, "Lyra": 0.1}
    elif "creative" in input_text.lower():
        self.active_fragments = {"Nyx": 0.6, "Lyra": 0.2, "Velastra": 0.2}
    # ... additional selection logic ...
```

### Memory Consolidation

The system consolidates short-term memories into long-term storage when the STM buffer reaches capacity:

```python
def _consolidate_memory(self):
    """Consolidate short-term to long-term memory."""
    # Get all STM entries
    stm_entries = self.stm.get_all()
    
    # Create a summary
    summary = f"Conversation summary: {len(stm_entries)} exchanges..."
    
    # Store in LTM
    self.ltm.store({"summary": summary, "entries": stm_entries})
    
    # Clear STM (keeping a few recent entries)
    self.stm.clear(keep_last=3)
```

## T.R.E.E.S. Integration

This implementation demonstrates several key T.R.E.E.S. principles:

1. **Recursive Identity**: Fragment-based identity system with specialized personas
2. **Memory Gravity**: Emotional and contextual weighting of information
3. **Symbolic Compression**: Efficient encoding of information through summaries
4. **Logic Shells**: Layered processing via the fragment system

## Development Roadmap

### Current Implementation
- Basic biomimetic structure
- Fragment-based identity system
- Dual-hemisphere memory
- Simple LLM interface simulation

### Planned Enhancements
1. Integration with actual LLM API
2. Dream cycle implementation for memory optimization
3. Symbolic compression using UML Calculator principles
4. Enhanced fragment selection with emotional context
5. Vector memory integration for semantic search

## Contributing

When developing for BlackwallV2:

1. Maintain the biomimetic architecture pattern
2. Document all T.R.E.E.S. principles implemented
3. Ensure fragment identity verification via the Soul module
4. Implement proper error handling and memory persistence
5. Follow the module interface conventions for Body communication
