# LLM Integration Guide

This document provides details on integrating BlackwallV2 with various LLM providers and configuring the system for optimal performance.

## System Requirements

- **OS:** Windows 10/11 64-bit
- **CPU:** 4+ cores recommended (8+ preferred)
- **RAM:** 16GB minimum (32GB recommended)
- **Storage:** 5GB for base system, additional space for LLM models
- **Optional GPU:** NVIDIA GPU with 8GB+ VRAM for local LLM inference

## LLM Integration Options

BlackwallV2 supports multiple LLM providers through a unified interface:

### 1. Local LLM Integration

- **LM Studio**
  - Default URL: http://localhost:1234
  - Supports various models like Qwen, Mistral, Llama, etc.
  - Configure in `llm_integration/config.json`

- **Ollama**
  - Default URL: http://localhost:11434
  - Easy model management with `ollama pull <model>`
  - Configure in `llm_integration/config.json`

### 2. API-based Integration

- **OpenAI API**
  - Requires API key in `.env` file
  - Models: GPT-3.5-Turbo, GPT-4, etc.
  - Configure in `llm_integration/config.json`

- **Anthropic API**
  - Requires API key in `.env` file
  - Models: Claude 3 Opus, Claude 3 Sonnet, etc.
  - Configure in `llm_integration/config.json`

## Configuration

1. **Setup environment**:
   - Copy `.env.example` to `.env`
   - Add any required API keys

2. **Configure LLM settings**:
   - Edit `llm_integration/config.json`:
   ```json
   {
     "provider": "local",  // Options: "local", "openai", "anthropic"
     "local_url": "http://localhost:1234",  // For local models
     "model": "qwen/qwen3-14b",  // Model identifier
     "temperature": 0.7,
     "max_tokens": 2000,
     "system_prompt_file": "system_prompt.txt"
   }
   ```

3. **Customize system prompt**:
   - Edit `llm_integration/system_prompt.txt`
   - This defines Lyra's core personality and behavior

## Example LLM Integration

To interact with the LLM through the BlackwallV2 system:

```python
from BlackwallV2.Implementation.llm_integration import llm_interface

# Initialize the LLM interface
llm = llm_interface.LLMInterface()

# Generate a response
response = llm.generate_response("Tell me about the TREES framework.")

print(response)
```

## Batch Processing

The system supports batch processing of inputs through:

```python
from BlackwallV2.Implementation.llm_integration import batch_processor

# Process a list of inputs
processor = batch_processor.BatchProcessor()
results = processor.process_batch([
    "What is the UML Calculator?",
    "Explain the TREES framework.",
    "What is BlackwallV2?"
])

for result in results:
    print(result)
```

## Testing LLM Connection

Run the LLM demo to test your connection:

```bash
cd d:\UML Calculator\UML_Calculator_V1\TREES\BlackwallV2\Implementation
python run_llm_demo.py
```

Or use the batch file:

```bash
run_llm_demo.bat
```

## Troubleshooting

- **Connection issues**: Verify the LLM server is running and the URL is correct
- **Authorization errors**: Check API keys in the .env file
- **Model errors**: Ensure the specified model is available on your provider
- **Timeout issues**: Adjust timeout settings in `llm_interface.py`

## Advanced Configuration

See `llm_integration/enhanced_brainstem.py` for advanced LLM integration options, including:
- Fragment-based personality adjustments
- Context management for coherent conversations
- Memory integration for persistent context
