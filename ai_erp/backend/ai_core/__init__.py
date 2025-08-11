"""
AI Core Module for AI ERP System

This module provides the core AI functionality including LLM integration,
context management, and intelligent task processing.
"""

from .llm.api_client import LLMClient
from .context.manager import ContextManager
from .tasks.router import TaskRouter

__version__ = "1.0.0"
__all__ = ["LLMClient", "ContextManager", "TaskRouter"]