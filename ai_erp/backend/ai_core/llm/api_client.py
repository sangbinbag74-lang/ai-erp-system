"""
LLM API Client for multiple providers
Supports OpenAI, Anthropic, and other LLM providers
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import openai
import anthropic
from dataclasses import dataclass
import os
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROK = "grok"


@dataclass
class LLMResponse:
    """Standardized response from LLM providers"""
    content: str
    tokens_used: int
    model: str
    provider: str
    cost_estimate: float
    metadata: Dict[str, Any] = None


@dataclass
class LLMMessage:
    """Standardized message format"""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        **kwargs
    ) -> LLMResponse:
        pass
    
    @abstractmethod
    def estimate_cost(self, tokens: int, model: str) -> float:
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str):
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
        }
    
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        model: str = "gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        try:
            formatted_messages = [
                {"role": msg.role, "content": msg.content} 
                for msg in messages
            ]
            
            response = await self.client.chat.completions.create(
                model=model,
                messages=formatted_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            cost = self.estimate_cost(tokens_used, model)
            
            return LLMResponse(
                content=content,
                tokens_used=tokens_used,
                model=model,
                provider="openai",
                cost_estimate=cost,
                metadata={
                    "finish_reason": response.choices[0].finish_reason,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                }
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def estimate_cost(self, tokens: int, model: str) -> float:
        if model not in self.pricing:
            return 0.0
        
        # Rough estimate assuming 50/50 split between input/output
        input_tokens = tokens // 2
        output_tokens = tokens // 2
        
        pricing = self.pricing[model]
        cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1000
        return cost


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.pricing = {
            "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
            "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125}
        }
    
    async def generate_response(
        self, 
        messages: List[LLMMessage], 
        model: str = "claude-3-sonnet-20240229",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> LLMResponse:
        try:
            # Separate system message from other messages
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg.role == "system":
                    system_message = msg.content
                else:
                    user_messages.append({
                        "role": msg.role, 
                        "content": msg.content
                    })
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else None,
                messages=user_messages,
                **kwargs
            )
            
            content = response.content[0].text
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            cost = self.estimate_cost(tokens_used, model)
            
            return LLMResponse(
                content=content,
                tokens_used=tokens_used,
                model=model,
                provider="anthropic",
                cost_estimate=cost,
                metadata={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "stop_reason": response.stop_reason
                }
            )
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
    
    def estimate_cost(self, tokens: int, model: str) -> float:
        if model not in self.pricing:
            return 0.0
        
        # Use actual token counts from response if available
        input_tokens = tokens // 2
        output_tokens = tokens // 2
        
        pricing = self.pricing[model]
        cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1000
        return cost


class LLMClient:
    """
    Main LLM client that manages multiple providers and routing
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.providers = {}
        self.default_provider = config.get("default_provider", "openai")
        self.fallback_providers = config.get("fallback_providers", [])
        self.cost_tracking = config.get("cost_tracking", True)
        self.total_cost = 0.0
        
        # Initialize providers based on config
        self._initialize_providers(config)
    
    def _initialize_providers(self, config: Dict[str, Any]):
        """Initialize available LLM providers"""
        
        # OpenAI
        if "openai_api_key" in config:
            self.providers["openai"] = OpenAIProvider(config["openai_api_key"])
            logger.info("OpenAI provider initialized")
        
        # Anthropic
        if "anthropic_api_key" in config:
            self.providers["anthropic"] = AnthropicProvider(config["anthropic_api_key"])
            logger.info("Anthropic provider initialized")
        
        if not self.providers:
            raise ValueError("No LLM providers configured")
    
    async def generate_response(
        self, 
        messages: Union[str, List[LLMMessage]], 
        provider: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """
        Generate response using specified or default provider
        """
        
        # Convert string to LLMMessage if needed
        if isinstance(messages, str):
            messages = [LLMMessage(role="user", content=messages)]
        
        # Use specified provider or default
        provider_name = provider or self.default_provider
        
        if provider_name not in self.providers:
            if self.fallback_providers:
                provider_name = self.fallback_providers[0]
                logger.warning(f"Falling back to {provider_name} provider")
            else:
                raise ValueError(f"Provider {provider_name} not available")
        
        try:
            provider_instance = self.providers[provider_name]
            response = await provider_instance.generate_response(messages, **kwargs)
            
            # Track costs
            if self.cost_tracking:
                self.total_cost += response.cost_estimate
                logger.info(f"Generated response. Cost: ${response.cost_estimate:.4f}, Total: ${self.total_cost:.4f}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error with {provider_name}: {str(e)}")
            
            # Try fallback providers
            for fallback in self.fallback_providers:
                if fallback != provider_name and fallback in self.providers:
                    try:
                        logger.info(f"Trying fallback provider: {fallback}")
                        fallback_provider = self.providers[fallback]
                        response = await fallback_provider.generate_response(messages, **kwargs)
                        
                        if self.cost_tracking:
                            self.total_cost += response.cost_estimate
                        
                        return response
                        
                    except Exception as fallback_error:
                        logger.error(f"Fallback {fallback} also failed: {str(fallback_error)}")
                        continue
            
            # If all providers failed, re-raise the original error
            raise e
    
    async def analyze_file(self, file_content: str, file_type: str, **kwargs) -> LLMResponse:
        """
        Analyze file content using AI
        """
        system_prompt = """
        You are an AI assistant specialized in analyzing business documents and files. 
        Analyze the provided file content and provide:
        1. Summary of the content
        2. Key insights and findings
        3. Recommendations for action
        4. Any data quality issues or concerns
        
        Be concise but thorough in your analysis.
        """
        
        user_prompt = f"""
        Please analyze this {file_type} file:
        
        Content:
        {file_content}
        """
        
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]
        
        return await self.generate_response(messages, **kwargs)
    
    async def process_query(self, user_query: str, context: Optional[Dict] = None, **kwargs) -> LLMResponse:
        """
        Process natural language queries about ERP data
        """
        system_prompt = """
        You are an AI ERP assistant. Help users with business operations, data analysis, 
        and ERP system tasks. You can:
        - Analyze business data and provide insights
        - Help with inventory management
        - Process accounting and financial queries  
        - Assist with sales and purchasing operations
        - Generate reports and summaries
        
        Always provide actionable and accurate information.
        """
        
        context_info = ""
        if context:
            context_info = f"\nContext: {context}"
        
        user_prompt = f"Query: {user_query}{context_info}"
        
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]
        
        return await self.generate_response(messages, **kwargs)
    
    def get_cost_summary(self) -> Dict[str, float]:
        """Get cost tracking summary"""
        return {
            "total_cost": self.total_cost,
            "providers": list(self.providers.keys())
        }
    
    def reset_cost_tracking(self):
        """Reset cost tracking"""
        self.total_cost = 0.0
        logger.info("Cost tracking reset")


# Factory function for easy initialization
def create_llm_client(
    openai_key: Optional[str] = None,
    anthropic_key: Optional[str] = None,
    default_provider: str = "openai",
    **kwargs
) -> LLMClient:
    """
    Factory function to create LLM client with environment variables
    """
    config = {
        "default_provider": default_provider,
        **kwargs
    }
    
    # Use provided keys or environment variables
    if openai_key or os.getenv("OPENAI_API_KEY"):
        config["openai_api_key"] = openai_key or os.getenv("OPENAI_API_KEY")
    
    if anthropic_key or os.getenv("ANTHROPIC_API_KEY"):
        config["anthropic_api_key"] = anthropic_key or os.getenv("ANTHROPIC_API_KEY")
    
    return LLMClient(config)