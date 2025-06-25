"""
LLM Integration Module for BlackwallV2

This module provides integration with Language Models (LLMs) through various providers:
1. OpenAI API
2. Local LM Studio server
3. Anthropic API
4. Custom providers through LiteLLM

Configurable through environment variables or configuration files.
"""

import os
import json
import time
import requests
import dotenv
from typing import Dict, List, Any, Optional
import importlib.util

# Try to import OpenAI if available
openai_available = importlib.util.find_spec("openai") is not None

if openai_available:
    import openai
    from openai import OpenAI

# Try to import LiteLLM if available
litellm_available = importlib.util.find_spec("litellm") is not None

if litellm_available:
    import litellm

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

class LLMConfig:
    """Configuration class for LLM providers"""
    def __init__(self, config_file: Optional[str] = None):
        # Default configuration
        self.config = {
            "provider": os.getenv("LLM_PROVIDER", "local"),  # local, openai, anthropic, litellm
            "api_key": os.getenv("LLM_API_KEY", ""),
            "model": os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
            "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "1024")),
            "top_p": float(os.getenv("LLM_TOP_P", "0.9")),
            "frequency_penalty": float(os.getenv("LLM_FREQUENCY_PENALTY", "0.0")),
            "presence_penalty": float(os.getenv("LLM_PRESENCE_PENALTY", "0.0")),
            "stop_sequences": os.getenv("LLM_STOP_SEQUENCES", "").split(",") if os.getenv("LLM_STOP_SEQUENCES") else [],
            "local_api_url": os.getenv("LLM_LOCAL_API_URL", "http://localhost:1234/v1/chat/completions"),
        }
        
        # Override with config file if provided
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    self.config.update(file_config)
            except Exception as e:
                print(f"Error loading config file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self.config[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update configuration with a dictionary"""
        self.config.update(config_dict)


class LLMInterface:
    """Interface to the LLM (Language Model) for hypothesis generation."""
    def __init__(self, config_file: Optional[str] = None):
        self.config = LLMConfig(config_file)
        self._setup_client()
    
    def _setup_client(self) -> None:
        """Set up the LLM client based on the provider"""
        provider = self.config.get("provider", "local")
        
        if provider == "openai" and openai_available:
            self.client = OpenAI(api_key=self.config.get("api_key"))
        elif provider == "litellm" and litellm_available:
            # Configure LiteLLM if it's being used
            litellm.api_key = self.config.get("api_key")
            self.client = litellm
        else:
            # Default to HTTP requests for local or other providers
            self.client = None
    
    def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a response from the LLM based on the prompt"""
        # Log the attempt
        print(f"[LLM] Generating response for prompt: {prompt[:50]}...")
        
        try:
            provider = self.config.get("provider", "local")
            
            # Prepare messages in the ChatML format
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Track performance
            start_time = time.time()
            
            if provider == "openai" and openai_available:
                response = self.client.chat.completions.create(
                    model=self.config.get("model"),
                    messages=messages,
                    temperature=self.config.get("temperature"),
                    max_tokens=self.config.get("max_tokens"),
                    top_p=self.config.get("top_p"),
                    frequency_penalty=self.config.get("frequency_penalty"),
                    presence_penalty=self.config.get("presence_penalty"),
                    stop=self.config.get("stop_sequences") or None
                )
                result = response.choices[0].message.content
                
            elif provider == "litellm" and litellm_available:
                response = litellm.completion(
                    model=self.config.get("model"),
                    messages=messages,
                    temperature=self.config.get("temperature"),
                    max_tokens=self.config.get("max_tokens"),
                    top_p=self.config.get("top_p"),
                    frequency_penalty=self.config.get("frequency_penalty"),
                    presence_penalty=self.config.get("presence_penalty"),
                    stop=self.config.get("stop_sequences") or None
                )
                result = response.choices[0].message.content
                
            else:
                # Default to local API call using requests
                url = self.config.get("local_api_url")
                headers = {'Content-Type': 'application/json'}
                data = {
                    "model": self.config.get("model"),
                    "messages": messages,
                    "temperature": self.config.get("temperature"),
                    "max_tokens": self.config.get("max_tokens"),
                    "top_p": self.config.get("top_p"),
                    "frequency_penalty": self.config.get("frequency_penalty"),
                    "presence_penalty": self.config.get("presence_penalty"),
                }
                if self.config.get("stop_sequences"):
                    data["stop"] = self.config.get("stop_sequences")
                
                # Handle timeouts and connection errors gracefully
                try:
                    response = requests.post(url, headers=headers, json=data, timeout=180)
                    response.raise_for_status()  # Raise exception for 4XX/5XX responses
                    result = response.json()['choices'][0]['message']['content']
                except requests.exceptions.Timeout:
                    print(f"[LLM] Request timed out after 180s to {url}")
                    return f"[ERROR: Request to LLM API timed out. Please check if the service at {url} is running.]"
                except requests.exceptions.ConnectionError:
                    print(f"[LLM] Connection error to {url}")
                    return f"[ERROR: Could not connect to LLM API at {url}. Is the server running?]"
                except requests.exceptions.RequestException as e:
                    print(f"[LLM] Request failed: {str(e)}")
                    return f"[ERROR: LLM API request failed: {str(e)}]"
                except (KeyError, IndexError, ValueError) as e:
                    print(f"[LLM] Failed to parse response: {str(e)}")
                    return f"[ERROR: Failed to parse LLM API response: {str(e)}]"
            
            # Track and log performance
            elapsed_time = time.time() - start_time
            print(f"[LLM] Response generated in {elapsed_time:.2f}s")
            
            return result
                    
        except Exception as e:
            print(f"[LLM] Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"


# Example usage
if __name__ == "__main__":
    llm = LLMInterface()
    response = llm.generate_response("Tell me about the TREES framework")
    print(response)
