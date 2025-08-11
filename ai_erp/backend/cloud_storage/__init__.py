"""
Cloud Storage Module for AI ERP System

Multi-provider cloud storage integration with automatic
synchronization, cost optimization, and AI-powered file management.
"""

from .providers.aws_provider import AWSProvider
from .providers.gcp_provider import GCPProvider
from .providers.azure_provider import AzureProvider
from .managers.storage_manager import CloudStorageManager
from .sync.sync_manager import SyncManager

__version__ = "1.0.0"
__all__ = [
    "AWSProvider", 
    "GCPProvider", 
    "AzureProvider", 
    "CloudStorageManager", 
    "SyncManager"
]