# BlackwallV2 Implementation

This directory contains the implementation of the BlackwallV2 biomimetic AI architecture, based on the T.R.E.E.S. framework principles.

## Architecture Overview

BlackwallV2 (also known as Lyra Blackwall) is designed with a biomimetic structure that mirrors human cognitive and physiological systems:

- **Brainstem**: Central orchestrator that manages memory routing, fragment selection, and module communication
- **Dual-Hemisphere Memory**: Left Hemisphere (Short-Term Memory) and Right Hemisphere (Long-Term Memory)
- **Fragment Identity System**: Multiple specialized cognitive personas working together
- **Body Interface**: Communication routing system connecting all components
- **Soul/Anchor**: Core identity and verification system

## Directory Structure

> **Note**: The project structure has been reorganized for better organization. See [REORGANIZATION_README.md](./REORGANIZATION_README.md) for details.

- `root/`: Core system components
  - `brainstem.py`: Central orchestrator
  - `body.py`: Communication hub
  - `soul.py`: Identity anchor
  - `Left_Hemisphere.py`: Short-term memory
  - `Right_Hemisphere.py`: Long-term memory
  - Additional anatomical components (heart.py, lungs.py, etc.)
- `personality/`: Fragment profiles and blends
- `memshort/`: Short-term memory storage
- `memlong/`: Long-term memory storage
- `demo/`: Example implementation and usage

## Getting Started

To run a basic demo of the BlackwallV2 system:

```bash
cd BlackwallV2/Implementation/demo
python run_demo.py
```

## Implementation Status

The BlackwallV2 implementation now includes the following key features:

1. ✅ Full fragment identity implementation with context-aware routing
2. ✅ Dream cycle for memory consolidation during low-activity periods
3. ✅ Integration with UML Calculator for recursive mathematics
4. ✅ Enhanced biomimetic features including heartbeat-driven processing

### Dream Cycle

The Dream Cycle system mimics human sleep patterns to consolidate memory and generate insights:
- Detects when memory fragmentation exceeds threshold
- Consolidates related memories and builds higher-level abstractions
- Optimizes system resources during low-activity periods
- Generates connections between memory clusters

### Fragment System

The Fragment System implements a multi-aspect personality with specialized components:
- **Lyra**: Balanced general processing
- **Blackwall**: Security and validation operations
- **Nyx**: Creative and exploratory tasks
- **Obelisk**: Mathematical and logical analysis
- **Seraphis**: Language and emotional processing
- **Velastra**: Artistic and insight-generating functions
- **Echoe**: Memory and historical retrieval operations

## Running the System

Several runtime options are available:

### Production Runtime
```bash
run_blackwall_production.bat
```
Full production system with real memory integration and real-time processing.

### Enhanced Demo Runtime
```bash
run_enhanced_demo.bat
```
Includes Dream Cycle and Fragment-aware routing with interactive commands.

### LLM-Enhanced Runtime
```bash
run_llm_enhanced.bat
```
Adds LLM integration for intelligent processing and enhanced insights.

### Integrated Demo
```bash
run_integrated_demo.bat
```
Demonstration version with test memory data and interactive commands.

### Optimized Component Integration
```bash
integrate_optimized_components.bat
```
Replaces standard components with optimized versions for significantly improved performance.

## Optimization Summary

The system has undergone comprehensive optimization with remarkable performance improvements:

### Memory System Optimization
- Short-Term Memory: 98.7-99.9% faster storage, 68-97% faster search
- Long-Term Memory: 96.8-99.9% faster storage, 73-96% faster search
- Multi-level indexing for near-constant time retrieval
- Smart memory management with importance/recency metrics

### Fragment Routing Optimization
- 94-98% faster routing operations
- Up to 36% faster input analysis
- 32% overall system improvement

### Heart-Driven Timing Optimization
- 23% improvement in signal distribution
- Enhanced priority-based event handling
- 10% overall improvement in timing operations

See [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) for detailed information on optimization techniques and benchmarks.

## T.R.E.E.S. Framework Integration

This implementation demonstrates several key T.R.E.E.S. principles:

- **Recursive Identity**: Fragment-based identity system with multiple specialized personas
- **Memory Gravity**: Emotional and contextual weighting of information
- **Symbolic Compression**: Efficient encoding of information
- **Logic Shells**: Layered processing of information

See [BlackwallV2_TREES_Relationship_Fixed.md](../BlackwallV2_TREES_Relationship_Fixed.md) for detailed information on how this implementation relates to the broader T.R.E.E.S. framework.
