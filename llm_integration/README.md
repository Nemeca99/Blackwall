# LLM Integration for BlackwallV2

This module provides integration with Language Model APIs for the BlackwallV2 system, incorporating the best patterns from legacy BlackwallV2/Lyra systems.

## Features

- Support for multiple LLM providers:
  - OpenAI API
  - Local LLM servers (e.g., LM Studio)
  - Anthropic API
  - LiteLLM (unified API wrapper)

- Enhanced text processing:
  - Smart text formatting and cleaning
  - Advanced tokenization
  - Stopword filtering

- Batch processing capabilities:
  - Performance evaluation
  - Metrics collection
  - Continuous learning mode

- Configurable through:
  - Environment variables
  - Configuration files
  - Runtime settings

## Setup

1. Install required dependencies:
   ```bash
   pip install openai requests python-dotenv litellm
   ```

2. Configure LLM provider:
   - Set environment variables or create a .env file:
     ```
     LLM_PROVIDER=openai
     LLM_API_KEY=your_api_key_here
     LLM_MODEL=gpt-4
     ```
   - Alternatively, modify `config.json` file

## Usage

### Basic Usage

```python
from llm_integration.enhanced_brainstem import EnhancedBrainstem

# Initialize with optional custom config file
brain = EnhancedBrainstem("path/to/config.json")

# Generate a response
response = brain.generate_response("Tell me about the TREES framework")
print(response)

# Full thinking process with context and fragment integration
result = brain.think("Explain UML symbolic processing")
print(result["fused_response"])
```

### Batch Processing

```python
from llm_integration.batch_processor import BatchProcessor, SAMPLE_TEST_PROMPTS

# Initialize the processor
brain = EnhancedBrainstem()
processor = BatchProcessor(brain=brain)

# Run a batch of prompts
results = processor.run_batch(SAMPLE_TEST_PROMPTS[:5])

# Run continuous processing with metrics collection
processor.run_continuous(
    SAMPLE_TEST_PROMPTS,
    num_cycles=3,
    batch_size=5
)
```

## Using Local LLMs

To use a local LLM server (like LM Studio or similar):

1. Start your local LLM server
2. Set the environment variable:
   ```
   LLM_PROVIDER=local
   LLM_LOCAL_API_URL=http://localhost:1234/v1/chat/completions
   ```

## Configuration Reference

| Setting | Environment Variable | Default | Description |
|---------|---------------------|---------|-------------|
| provider | LLM_PROVIDER | local | LLM provider (local, openai, anthropic, litellm) |
| api_key | LLM_API_KEY | | API key for the provider |
| model | LLM_MODEL | gpt-3.5-turbo | Model to use |
| temperature | LLM_TEMPERATURE | 0.7 | Response randomness (0-1) |
| max_tokens | LLM_MAX_TOKENS | 1024 | Maximum tokens in the response |
| local_api_url | LLM_LOCAL_API_URL | http://localhost:1234/v1/chat/completions | URL for local LLM server |
