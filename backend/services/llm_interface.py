"""
LLM Interface - Abstract interface for different LLM providers.

Supports multiple providers (OpenAI, Anthropic, Google) with unified interface.
Configuration is loaded from environment variables.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from enum import Enum
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/.env")

class LLMProvider(Enum):
    GOOGLE = "google"


class Message:
    """Represents a chat message."""
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


class LLMInterface(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Message], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate a response from the LLM."""
        pass

class GoogleLLM(LLMInterface):
    """Google Gemini implementation."""
    
    def __init__(self, api_key: str, model: str = "gemini-3-pro-preview"):
        self.api_key = api_key
        self.model = model
        
    async def generate_response(
        self, 
        messages: List[Message], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            model = genai.GenerativeModel(self.model)
            
            # Convert messages to Gemini format
            prompt_parts = []
            for msg in messages:
                prefix = f"{msg.role}: " if msg.role != "user" else ""
                prompt_parts.append(f"{prefix}{msg.content}")
            
            prompt = "\n".join(prompt_parts)
            
            generation_config = {
                "temperature": temperature,
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens
            
            response = await model.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        except ImportError:
            raise ImportError("Google GenAI package not installed. Run: pip install google-generativeai")


class LLMFactory:
    """Factory to create LLM instances based on configuration."""
    
    @staticmethod
    def create_llm(
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ) -> LLMInterface:
        """
        Create an LLM instance based on environment variables or provided parameters.
        
        Environment variables:
        - LLM_PROVIDER: openai, anthropic, or google
        - LLM_API_KEY: API key for the provider
        - LLM_MODEL: Model name (optional, uses defaults)
        """
        #provider = provider or os.getenv("LLM_PROVIDER")
        #api_key = api_key or os.getenv("LLM_API_KEY")
        #model = model or os.getenv("LLM_MODEL")

        provider = "google"
        api_key = "AIzaSyCWhRgarx6x8TPu0Uud1iA1Lch8ijvoZJE"
        model = "gemini-3-pro-preview"
        
        print(provider)
        if not api_key:
            raise ValueError("LLM_API_KEY environment variable not set")
        
        provider_enum = LLMProvider(provider.lower())
        
        if provider_enum == LLMProvider.GOOGLE:
            default_model = "gemini-pro"
            return GoogleLLM(api_key, model or default_model)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
