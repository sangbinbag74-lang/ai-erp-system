"""
File Manager Module for AI ERP System

Enhanced file management system with AI-powered analysis,
automatic processing, and intelligent organization.
"""

from .processors.document_processor import DocumentProcessor
from .analyzers.content_analyzer import ContentAnalyzer
from .storage.cloud_manager import CloudStorageManager

__version__ = "1.0.0"
__all__ = ["DocumentProcessor", "ContentAnalyzer", "CloudStorageManager"]