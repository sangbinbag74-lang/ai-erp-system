"""
Cloud Storage Manager for AI ERP System

Unified storage management across multiple cloud providers
with intelligent routing, cost optimization, and AI-powered insights.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import hashlib
import json

from ..providers.aws_provider import AWSProvider, UploadResult

logger = logging.getLogger(__name__)


class StorageProvider(Enum):
    AWS_S3 = "aws_s3"
    GCP_STORAGE = "gcp_storage"
    AZURE_BLOB = "azure_blob"
    LOCAL = "local"


class FileAccessPattern(Enum):
    HOT = "hot"          # Frequently accessed
    WARM = "warm"        # Occasionally accessed
    COLD = "cold"        # Rarely accessed
    ARCHIVE = "archive"  # Long-term storage


@dataclass
class StorageFile:
    """Unified file representation across providers"""
    id: str
    key: str
    original_name: str
    size: int
    content_type: str
    provider: StorageProvider
    bucket: str
    created_at: datetime
    last_accessed: Optional[datetime] = None
    access_count: int = 0
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None
    checksum: Optional[str] = None
    encryption: bool = True
    access_pattern: FileAccessPattern = FileAccessPattern.HOT


@dataclass
class StorageQuota:
    """Storage quota and usage information"""
    total_limit_bytes: int
    used_bytes: int
    files_count: int
    provider_quotas: Dict[StorageProvider, Dict[str, Any]]
    
    @property
    def used_percentage(self) -> float:
        if self.total_limit_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_limit_bytes) * 100
    
    @property
    def available_bytes(self) -> int:
        return max(0, self.total_limit_bytes - self.used_bytes)


class CloudStorageManager:
    """
    Unified cloud storage manager with multi-provider support
    """
    
    def __init__(self, config: Dict[str, Any], llm_client=None):
        self.config = config
        self.llm_client = llm_client
        
        # Initialize providers
        self.providers = {}
        self._initialize_providers()
        
        # Default provider and fallback chain
        self.default_provider = config.get('default_provider', StorageProvider.AWS_S3)
        self.fallback_providers = config.get('fallback_providers', [])
        
        # Cost optimization settings
        self.cost_optimization = config.get('cost_optimization', True)
        self.intelligent_routing = config.get('intelligent_routing', True)
        self.auto_tiering = config.get('auto_tiering', True)
        
        # File tracking (in production, this would be in a database)
        self._file_registry = {}
        self._access_logs = []
        
        # Quotas and limits
        self.quotas = self._initialize_quotas()
    
    def _initialize_providers(self):
        """Initialize available storage providers"""
        
        # AWS S3
        aws_config = self.config.get('aws', {})
        if aws_config.get('enabled', False):
            try:
                self.providers[StorageProvider.AWS_S3] = AWSProvider(aws_config)
                logger.info("AWS S3 provider initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AWS provider: {str(e)}")
        
        # Google Cloud Storage (placeholder)
        gcp_config = self.config.get('gcp', {})
        if gcp_config.get('enabled', False):
            # self.providers[StorageProvider.GCP_STORAGE] = GCPProvider(gcp_config)
            logger.info("GCP Storage provider not implemented yet")
        
        # Azure Blob Storage (placeholder)
        azure_config = self.config.get('azure', {})
        if azure_config.get('enabled', False):
            # self.providers[StorageProvider.AZURE_BLOB] = AzureProvider(azure_config)
            logger.info("Azure Blob provider not implemented yet")
        
        if not self.providers:
            raise ValueError("No storage providers configured")
    
    def _initialize_quotas(self) -> StorageQuota:
        """Initialize storage quotas"""
        
        quota_config = self.config.get('quotas', {})
        
        return StorageQuota(
            total_limit_bytes=quota_config.get('total_limit_gb', 100) * 1024 * 1024 * 1024,
            used_bytes=0,
            files_count=0,
            provider_quotas={}
        )
    
    async def upload_file(
        self,
        file_data: bytes,
        filename: str,
        user_id: str,
        team_id: str,
        content_type: str = None,
        metadata: Dict[str, Any] = None,
        access_pattern: FileAccessPattern = FileAccessPattern.HOT,
        **kwargs
    ) -> Tuple[bool, Optional[StorageFile], Optional[str]]:
        """
        Upload file with intelligent provider selection
        """
        
        try:
            # Check quota
            if not self._check_quota(len(file_data)):
                return False, None, "Storage quota exceeded"
            
            # Generate file key and metadata
            file_key = self._generate_file_key(filename, user_id, team_id)
            file_checksum = hashlib.sha256(file_data).hexdigest()
            
            # Determine optimal provider
            provider = await self._select_optimal_provider(
                file_size=len(file_data),
                content_type=content_type or "application/octet-stream",
                access_pattern=access_pattern,
                user_preferences=kwargs.get('user_preferences', {})
            )
            
            # Prepare enhanced metadata
            enhanced_metadata = {
                'user_id': user_id,
                'team_id': team_id,
                'original_filename': filename,
                'upload_timestamp': datetime.now().isoformat(),
                'checksum': file_checksum,
                'access_pattern': access_pattern.value,
                'ai_erp_version': '1.0.0'
            }
            
            if metadata:
                enhanced_metadata.update(metadata)
            
            # Upload to selected provider
            provider_instance = self.providers[provider]
            result = await provider_instance.upload_file(
                file_data=file_data,
                key=file_key,
                content_type=content_type,
                metadata=enhanced_metadata,
                access_pattern=access_pattern.value,
                **kwargs
            )
            
            if result.success:
                # Create storage file record
                storage_file = StorageFile(
                    id=file_checksum[:16],
                    key=file_key,
                    original_name=filename,
                    size=len(file_data),
                    content_type=content_type or "application/octet-stream",
                    provider=provider,
                    bucket=result.bucket,
                    created_at=datetime.now(),
                    tags={
                        'user_id': user_id,
                        'team_id': team_id,
                        'access_pattern': access_pattern.value
                    },
                    metadata=enhanced_metadata,
                    checksum=file_checksum,
                    access_pattern=access_pattern
                )
                
                # Register file
                self._register_file(storage_file)
                
                # Update quota usage
                self._update_quota_usage(len(file_data), 1)
                
                # Log successful upload
                self._log_access(storage_file.id, 'upload', user_id)
                
                logger.info(f"Successfully uploaded {filename} ({len(file_data)} bytes) to {provider.value}")
                
                return True, storage_file, None
            else:
                # Try fallback providers
                for fallback in self.fallback_providers:
                    if fallback in self.providers and fallback != provider:
                        try:
                            fallback_provider = self.providers[fallback]
                            fallback_result = await fallback_provider.upload_file(
                                file_data=file_data,
                                key=file_key,
                                content_type=content_type,
                                metadata=enhanced_metadata,
                                **kwargs
                            )
                            
                            if fallback_result.success:
                                storage_file = StorageFile(
                                    id=file_checksum[:16],
                                    key=file_key,
                                    original_name=filename,
                                    size=len(file_data),
                                    content_type=content_type or "application/octet-stream",
                                    provider=fallback,
                                    bucket=fallback_result.bucket,
                                    created_at=datetime.now(),
                                    tags={'user_id': user_id, 'team_id': team_id},
                                    metadata=enhanced_metadata,
                                    checksum=file_checksum,
                                    access_pattern=access_pattern
                                )
                                
                                self._register_file(storage_file)
                                self._update_quota_usage(len(file_data), 1)
                                self._log_access(storage_file.id, 'upload', user_id)
                                
                                logger.info(f"Upload succeeded with fallback provider {fallback.value}")
                                return True, storage_file, None
                                
                        except Exception as e:
                            logger.warning(f"Fallback provider {fallback.value} also failed: {str(e)}")
                            continue
                
                return False, None, result.error or "Upload failed"
                
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            return False, None, str(e)
    
    async def download_file(
        self,
        file_id: str,
        user_id: str
    ) -> Tuple[bool, Optional[bytes], Optional[str]]:
        """
        Download file by ID
        """
        
        try:
            # Get file record
            storage_file = self._get_file(file_id)
            if not storage_file:
                return False, None, "File not found"
            
            # Check access permissions (basic implementation)
            if not self._check_access_permission(storage_file, user_id):
                return False, None, "Access denied"
            
            # Download from provider
            provider = self.providers.get(storage_file.provider)
            if not provider:
                return False, None, f"Provider {storage_file.provider.value} not available"
            
            success, file_data, error = await provider.download_file(storage_file.key)
            
            if success:
                # Update access tracking
                self._update_file_access(storage_file, user_id)
                self._log_access(file_id, 'download', user_id)
                
                logger.info(f"Successfully downloaded file {storage_file.original_name}")
                
                return True, file_data, None
            else:
                return False, None, error
                
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {str(e)}")
            return False, None, str(e)
    
    async def delete_file(
        self,
        file_id: str,
        user_id: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Delete file by ID
        """
        
        try:
            # Get file record
            storage_file = self._get_file(file_id)
            if not storage_file:
                return False, "File not found"
            
            # Check delete permissions
            if not self._check_delete_permission(storage_file, user_id):
                return False, "Delete access denied"
            
            # Delete from provider
            provider = self.providers.get(storage_file.provider)
            if not provider:
                return False, f"Provider {storage_file.provider.value} not available"
            
            success, error = await provider.delete_file(storage_file.key)
            
            if success:
                # Unregister file
                self._unregister_file(storage_file)
                
                # Update quota usage
                self._update_quota_usage(-storage_file.size, -1)
                
                # Log deletion
                self._log_access(file_id, 'delete', user_id)
                
                logger.info(f"Successfully deleted file {storage_file.original_name}")
                
                return True, None
            else:
                return False, error
                
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {str(e)}")
            return False, str(e)
    
    async def list_files(
        self,
        user_id: str,
        team_id: str = None,
        limit: int = 100,
        offset: int = 0,
        filters: Dict[str, Any] = None
    ) -> List[StorageFile]:
        """
        List files with filtering and pagination
        """
        
        try:
            files = []
            
            for file_record in self._file_registry.values():
                # Apply filters
                if team_id and file_record.tags.get('team_id') != team_id:
                    continue
                
                if not self._check_access_permission(file_record, user_id):
                    continue
                
                # Apply additional filters
                if filters:
                    if 'content_type' in filters and file_record.content_type != filters['content_type']:
                        continue
                    
                    if 'access_pattern' in filters and file_record.access_pattern.value != filters['access_pattern']:
                        continue
                    
                    if 'min_size' in filters and file_record.size < filters['min_size']:
                        continue
                    
                    if 'max_size' in filters and file_record.size > filters['max_size']:
                        continue
                
                files.append(file_record)
            
            # Sort by creation date (newest first)
            files.sort(key=lambda f: f.created_at, reverse=True)
            
            # Apply pagination
            return files[offset:offset + limit]
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    async def get_storage_analytics(
        self,
        user_id: str,
        team_id: str = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive storage analytics
        """
        
        try:
            analytics = {
                'total_files': 0,
                'total_size_bytes': 0,
                'by_provider': {},
                'by_content_type': {},
                'by_access_pattern': {},
                'recent_activity': [],
                'cost_analysis': {},
                'recommendations': []
            }
            
            # Aggregate file statistics
            for file_record in self._file_registry.values():
                # Filter by team if specified
                if team_id and file_record.tags.get('team_id') != team_id:
                    continue
                
                # Check access permissions
                if not self._check_access_permission(file_record, user_id):
                    continue
                
                analytics['total_files'] += 1
                analytics['total_size_bytes'] += file_record.size
                
                # Provider breakdown
                provider_key = file_record.provider.value
                if provider_key not in analytics['by_provider']:
                    analytics['by_provider'][provider_key] = {'count': 0, 'size': 0}
                analytics['by_provider'][provider_key]['count'] += 1
                analytics['by_provider'][provider_key]['size'] += file_record.size
                
                # Content type breakdown
                if file_record.content_type not in analytics['by_content_type']:
                    analytics['by_content_type'][file_record.content_type] = {'count': 0, 'size': 0}
                analytics['by_content_type'][file_record.content_type]['count'] += 1
                analytics['by_content_type'][file_record.content_type]['size'] += file_record.size
                
                # Access pattern breakdown
                pattern_key = file_record.access_pattern.value
                if pattern_key not in analytics['by_access_pattern']:
                    analytics['by_access_pattern'][pattern_key] = {'count': 0, 'size': 0}
                analytics['by_access_pattern'][pattern_key]['count'] += 1
                analytics['by_access_pattern'][pattern_key]['size'] += file_record.size
            
            # Add recent activity
            recent_logs = [log for log in self._access_logs[-50:] if log.get('user_id') == user_id]
            analytics['recent_activity'] = recent_logs
            
            # Cost analysis
            analytics['cost_analysis'] = await self._analyze_costs(team_id)
            
            # Generate recommendations
            if self.llm_client:
                try:
                    recommendations = await self._generate_storage_recommendations(analytics)
                    analytics['recommendations'] = recommendations
                except Exception as e:
                    logger.warning(f"Failed to generate recommendations: {str(e)}")
            
            # Add quota information
            analytics['quota'] = {
                'total_limit_gb': self.quotas.total_limit_bytes / (1024 * 1024 * 1024),
                'used_gb': self.quotas.used_bytes / (1024 * 1024 * 1024),
                'used_percentage': self.quotas.used_percentage,
                'available_gb': self.quotas.available_bytes / (1024 * 1024 * 1024)
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating storage analytics: {str(e)}")
            return {}
    
    async def optimize_storage(
        self,
        team_id: str,
        user_id: str,
        dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        AI-powered storage optimization
        """
        
        try:
            optimization_results = {
                'actions_planned': [],
                'potential_savings': 0.0,
                'files_to_migrate': 0,
                'estimated_cost_reduction': 0.0
            }
            
            # Analyze file access patterns
            for file_record in self._file_registry.values():
                if file_record.tags.get('team_id') != team_id:
                    continue
                
                # Suggest tiering based on access patterns
                current_pattern = file_record.access_pattern
                suggested_pattern = self._suggest_optimal_pattern(file_record)
                
                if suggested_pattern != current_pattern:
                    action = {
                        'type': 'tier_migration',
                        'file_id': file_record.id,
                        'current_tier': current_pattern.value,
                        'suggested_tier': suggested_pattern.value,
                        'potential_savings': self._calculate_tier_savings(file_record, suggested_pattern)
                    }
                    
                    optimization_results['actions_planned'].append(action)
                    optimization_results['files_to_migrate'] += 1
                    optimization_results['potential_savings'] += action['potential_savings']
            
            # Execute optimizations if not dry run
            if not dry_run and optimization_results['actions_planned']:
                executed_actions = []
                for action in optimization_results['actions_planned']:
                    try:
                        # In a real implementation, this would migrate files to different storage tiers
                        executed_actions.append(action)
                    except Exception as e:
                        logger.warning(f"Failed to execute optimization action: {str(e)}")
                
                optimization_results['executed_actions'] = executed_actions
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Error optimizing storage: {str(e)}")
            return {'error': str(e)}
    
    # Helper methods
    
    async def _select_optimal_provider(
        self,
        file_size: int,
        content_type: str,
        access_pattern: FileAccessPattern,
        user_preferences: Dict[str, Any]
    ) -> StorageProvider:
        """
        Select optimal storage provider using AI or heuristics
        """
        
        if not self.intelligent_routing:
            return self.default_provider
        
        # Use AI-powered selection if available
        if self.llm_client:
            try:
                provider = await self._ai_provider_selection(
                    file_size, content_type, access_pattern, user_preferences
                )
                if provider:
                    return provider
            except Exception as e:
                logger.warning(f"AI provider selection failed: {str(e)}")
        
        # Fallback to heuristic-based selection
        return self._heuristic_provider_selection(file_size, content_type, access_pattern)
    
    async def _ai_provider_selection(
        self,
        file_size: int,
        content_type: str,
        access_pattern: FileAccessPattern,
        user_preferences: Dict[str, Any]
    ) -> Optional[StorageProvider]:
        """
        AI-powered provider selection
        """
        
        available_providers = list(self.providers.keys())
        
        prompt = f"""
        Select the optimal cloud storage provider for this file:
        
        File size: {file_size} bytes
        Content type: {content_type}
        Access pattern: {access_pattern.value}
        Available providers: {[p.value for p in available_providers]}
        User preferences: {user_preferences}
        
        Consider:
        1. Cost optimization
        2. Performance requirements
        3. Geographic location
        4. Compliance requirements
        
        Respond with just the provider name.
        """
        
        try:
            response = await self.llm_client.generate_response(prompt)
            
            # Parse provider from response
            for provider in available_providers:
                if provider.value.lower() in response.content.lower():
                    return provider
            
            return None
            
        except Exception as e:
            logger.error(f"AI provider selection error: {str(e)}")
            return None
    
    def _heuristic_provider_selection(
        self,
        file_size: int,
        content_type: str,
        access_pattern: FileAccessPattern
    ) -> StorageProvider:
        """
        Heuristic-based provider selection
        """
        
        # For large files or archive pattern, prefer providers with better archive tiers
        if file_size > 100 * 1024 * 1024 or access_pattern == FileAccessPattern.ARCHIVE:
            if StorageProvider.AWS_S3 in self.providers:
                return StorageProvider.AWS_S3
        
        # For frequently accessed files, prefer fastest provider
        if access_pattern == FileAccessPattern.HOT:
            # Use provider with best performance characteristics
            available_providers = list(self.providers.keys())
            return available_providers[0]  # Simplified selection
        
        # Default to configured default provider
        return self.default_provider if self.default_provider in self.providers else list(self.providers.keys())[0]
    
    def _generate_file_key(self, filename: str, user_id: str, team_id: str) -> str:
        """
        Generate unique file key
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_hash = hashlib.md5(f"{filename}{user_id}{team_id}{timestamp}".encode()).hexdigest()[:8]
        
        # Sanitize filename
        safe_filename = "".join(c for c in filename if c.isalnum() or c in '.-_')
        
        return f"ai-erp/{team_id}/{user_id}/{timestamp}_{file_hash}_{safe_filename}"
    
    def _check_quota(self, file_size: int) -> bool:
        """
        Check if upload would exceed quota
        """
        return (self.quotas.used_bytes + file_size) <= self.quotas.total_limit_bytes
    
    def _register_file(self, storage_file: StorageFile):
        """
        Register file in tracking system
        """
        self._file_registry[storage_file.id] = storage_file
    
    def _unregister_file(self, storage_file: StorageFile):
        """
        Unregister file from tracking system
        """
        if storage_file.id in self._file_registry:
            del self._file_registry[storage_file.id]
    
    def _get_file(self, file_id: str) -> Optional[StorageFile]:
        """
        Get file record by ID
        """
        return self._file_registry.get(file_id)
    
    def _update_quota_usage(self, size_delta: int, files_delta: int):
        """
        Update quota usage statistics
        """
        self.quotas.used_bytes += size_delta
        self.quotas.files_count += files_delta
    
    def _log_access(self, file_id: str, action: str, user_id: str):
        """
        Log file access for analytics
        """
        access_log = {
            'file_id': file_id,
            'action': action,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        }
        
        self._access_logs.append(access_log)
        
        # Keep only recent logs (limit memory usage)
        if len(self._access_logs) > 10000:
            self._access_logs = self._access_logs[-5000:]
    
    def _update_file_access(self, storage_file: StorageFile, user_id: str):
        """
        Update file access tracking
        """
        storage_file.last_accessed = datetime.now()
        storage_file.access_count += 1
    
    def _check_access_permission(self, storage_file: StorageFile, user_id: str) -> bool:
        """
        Check if user has access to file (simplified implementation)
        """
        # For now, allow access if user is in same team or is file owner
        file_user_id = storage_file.tags.get('user_id')
        file_team_id = storage_file.tags.get('team_id')
        
        # Owner can always access
        if file_user_id == user_id:
            return True
        
        # Team members can access (in production, check actual team membership)
        if file_team_id:
            return True  # Simplified - assume user is in team
        
        return False
    
    def _check_delete_permission(self, storage_file: StorageFile, user_id: str) -> bool:
        """
        Check if user can delete file (simplified implementation)
        """
        # Only file owner can delete (simplified)
        return storage_file.tags.get('user_id') == user_id
    
    def _suggest_optimal_pattern(self, file_record: StorageFile) -> FileAccessPattern:
        """
        Suggest optimal access pattern based on usage
        """
        
        # If never accessed in 90 days, suggest archive
        if file_record.last_accessed:
            days_since_access = (datetime.now() - file_record.last_accessed).days
            if days_since_access > 90:
                return FileAccessPattern.ARCHIVE
            elif days_since_access > 30:
                return FileAccessPattern.COLD
        
        # If accessed frequently, suggest hot
        if file_record.access_count > 10:
            return FileAccessPattern.HOT
        
        # Default to warm
        return FileAccessPattern.WARM
    
    def _calculate_tier_savings(
        self,
        file_record: StorageFile,
        suggested_pattern: FileAccessPattern
    ) -> float:
        """
        Calculate potential savings from tier migration
        """
        
        # Simplified cost calculation (in production, use actual provider pricing)
        cost_per_gb = {
            FileAccessPattern.HOT: 0.025,
            FileAccessPattern.WARM: 0.015,
            FileAccessPattern.COLD: 0.008,
            FileAccessPattern.ARCHIVE: 0.002
        }
        
        current_cost = (file_record.size / (1024**3)) * cost_per_gb[file_record.access_pattern]
        suggested_cost = (file_record.size / (1024**3)) * cost_per_gb[suggested_pattern]
        
        return max(0, current_cost - suggested_cost)
    
    async def _analyze_costs(self, team_id: str = None) -> Dict[str, Any]:
        """
        Analyze storage costs
        """
        
        cost_analysis = {
            'total_monthly_cost': 0.0,
            'by_provider': {},
            'by_tier': {},
            'trends': []
        }
        
        # Calculate costs for each file
        for file_record in self._file_registry.values():
            if team_id and file_record.tags.get('team_id') != team_id:
                continue
            
            # Simplified cost calculation
            size_gb = file_record.size / (1024**3)
            
            cost_per_gb = {
                FileAccessPattern.HOT: 0.025,
                FileAccessPattern.WARM: 0.015,
                FileAccessPattern.COLD: 0.008,
                FileAccessPattern.ARCHIVE: 0.002
            }
            
            monthly_cost = size_gb * cost_per_gb[file_record.access_pattern]
            cost_analysis['total_monthly_cost'] += monthly_cost
            
            # Provider breakdown
            provider_key = file_record.provider.value
            if provider_key not in cost_analysis['by_provider']:
                cost_analysis['by_provider'][provider_key] = 0.0
            cost_analysis['by_provider'][provider_key] += monthly_cost
            
            # Tier breakdown
            tier_key = file_record.access_pattern.value
            if tier_key not in cost_analysis['by_tier']:
                cost_analysis['by_tier'][tier_key] = 0.0
            cost_analysis['by_tier'][tier_key] += monthly_cost
        
        return cost_analysis
    
    async def _generate_storage_recommendations(
        self,
        analytics: Dict[str, Any]
    ) -> List[str]:
        """
        Generate AI-powered storage recommendations
        """
        
        if not self.llm_client:
            return []
        
        try:
            prompt = f"""
            Analyze this storage usage data and provide 3-5 specific recommendations:
            
            Total files: {analytics['total_files']}
            Total size: {analytics['total_size_bytes'] / (1024**3):.2f} GB
            Provider distribution: {analytics['by_provider']}
            Access pattern distribution: {analytics['by_access_pattern']}
            Cost analysis: {analytics.get('cost_analysis', {})}
            
            Provide actionable recommendations for:
            1. Cost optimization
            2. Performance improvement
            3. Storage organization
            4. Compliance and security
            
            Keep recommendations specific and implementable.
            """
            
            response = await self.llm_client.generate_response(prompt)
            
            # Parse recommendations
            recommendations = []
            lines = response.content.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                    recommendation = line.lstrip('-•0123456789. ').strip()
                    if recommendation:
                        recommendations.append(recommendation)
            
            return recommendations[:5]
            
        except Exception as e:
            logger.error(f"Error generating storage recommendations: {str(e)}")
            return []


def create_storage_manager(config: Dict[str, Any], llm_client=None) -> CloudStorageManager:
    """Factory function to create storage manager"""
    return CloudStorageManager(config=config, llm_client=llm_client)