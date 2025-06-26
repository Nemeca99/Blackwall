# BlackwallV2 Queue-Driven Architecture with Context-Aware Routing

## Overview
This demo showcases the biomimetic, heartbeat-driven queue management system with dynamic routing, organ discovery, health checks, and detailed logging capabilities. It also demonstrates advanced context-aware routing with specialized organs.

## Key Features
- Heartbeat-driven processing with controlled concurrency
- Robust queue management system
- Dynamic organ discovery and registration
- Context-aware routing based on prompt analysis
- Health checks and fault tolerance
- Detailed logging to demo_run_log.txt

## Specialized Organs
- **MathOrgan**: Handles mathematical computations and related queries
- **LanguageOrgan**: Handles language translations and linguistic requests
- **MemoryOrgan**: Provides memory storage and retrieval capabilities

## Fixed Issues
- Fixed empty input handling in Brainstem's process_input method
- Fixed context-aware routing in router.py to properly detect specialized capabilities
- Fixed import errors and module discovery
- Enhanced logging with terminal output mirroring
- Fixed math operation detection in MathOrgan

## Running the Demo
- **Standard Queue Demo**: Use `run_queue_demo.bat`
- **Advanced Context-Aware Routing**: Use `run_context_routing_demo.bat`

## Output
The demo generates output to:
- Terminal (real-time processing)
- demo_run_log.txt (persistent log)
- dynamic_routing_table.txt (organ capabilities)

## Architecture
The system is composed of biomimetic components:
- Heart: Controls processing rhythm
- Brainstem: Central orchestrator
- Body: Central nervous system for inter-organ communication
- Router: Dynamic organ discovery and capability-based routing
- Specialized Organs: Purpose-built processing units

This implementation demonstrates a truly event-driven, biomimetic architecture that efficiently processes information through specialized pathways.
