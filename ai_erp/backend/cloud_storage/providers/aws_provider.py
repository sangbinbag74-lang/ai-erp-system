"""
AWS S3 Provider for AI ERP Cloud Storage

Provides AWS S3 integration with optimized operations,
intelligent tiering, and cost management.
"""

import boto3
import logging
from typing import Dict, List, Optional, Any, Tuple, BinaryIO
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import hashlib
import mimetypes
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class StorageClass(Enum):
    STANDARD = "STANDARD"
    STANDARD_IA = "STANDARD_IA"  # Infrequent Access
    GLACIER = "GLACIER"
    GLACIER_IR = "GLACIER_IR"  # Instant Retrieval
    DEEP_ARCHIVE = "DEEP_ARCHIVE"


@dataclass
class AWSFile:
    """AWS S3 file metadata"""
    key: str
    bucket: str
    size: int
    etag: str
    last_modified: datetime
    storage_class: str
    metadata: Dict[str, str]
    url: Optional[str] = None


@dataclass
class UploadResult:
    """Result of file upload operation"""
    success: bool
    key: str
    bucket: str
    url: Optional[str] = None
    etag: Optional[str] = None
    error: Optional[str] = None
    cost_estimate: float = 0.0


class AWSProvider:
    """
    AWS S3 storage provider with intelligent cost optimization
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS credentials and config
        self.access_key = config.get('aws_access_key')
        self.secret_key = config.get('aws_secret_key')
        self.region = config.get('aws_region', 'us-east-1')
        self.bucket_name = config.get('bucket_name')
        
        # Cost optimization settings
        self.enable_intelligent_tiering = config.get('enable_intelligent_tiering', True)
        self.lifecycle_policies = config.get('lifecycle_policies', True)
        
        # Initialize S3 client
        try:
            session = boto3.Session(
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region
            )
            
            self.s3_client = session.client('s3')
            self.s3_resource = session.resource('s3')
            
            # Validate connection
            self._validate_connection()
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error(f"Error initializing AWS S3 client: {str(e)}")
            raise
    
    def _validate_connection(self):
        """Validate AWS connection and bucket access"""
        try:
            # Test bucket access
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Successfully connected to AWS S3 bucket: {self.bucket_name}")
            
            # Setup bucket policies if needed
            self._setup_bucket_policies()
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                raise ValueError(f"Bucket {self.bucket_name} does not exist")
            elif error_code == '403':
                raise PermissionError(f"Access denied to bucket {self.bucket_name}")
            else:
                raise e
    
    def _setup_bucket_policies(self):
        """Setup intelligent tiering and lifecycle policies"""
        
        if not self.lifecycle_policies:
            return
        
        try:
            # Create lifecycle configuration for cost optimization
            lifecycle_config = {
                'Rules': [
                    {
                        'ID': 'AIERPCostOptimization',
                        'Status': 'Enabled',
                        'Filter': {'Prefix': 'ai-erp/'},
                        'Transitions': [
                            {
                                'Days': 30,
                                'StorageClass': 'STANDARD_IA'
                            },
                            {
                                'Days': 90,
                                'StorageClass': 'GLACIER_IR'
                            },
                            {
                                'Days': 365,
                                'StorageClass': 'DEEP_ARCHIVE'
                            }
                        ],
                        'NoncurrentVersionTransitions': [
                            {
                                'NoncurrentDays': 7,
                                'StorageClass': 'STANDARD_IA'
                            },
                            {
                                'NoncurrentDays': 30,
                                'StorageClass': 'GLACIER'
                            }
                        ],
                        'NoncurrentVersionExpiration': {
                            'NoncurrentDays': 180
                        }
                    }
                ]
            }
            
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket_name,
                LifecycleConfiguration=lifecycle_config
            )
            
            logger.info("Configured S3 lifecycle policies for cost optimization")
            
        except Exception as e:
            logger.warning(f"Could not setup lifecycle policies: {str(e)}")
    
    async def upload_file(
        self, 
        file_data: bytes, 
        key: str,
        content_type: str = None,
        metadata: Dict[str, str] = None,
        storage_class: StorageClass = StorageClass.STANDARD,
        **kwargs
    ) -> UploadResult:
        """
        Upload file to S3 with intelligent optimization
        """
        
        try:
            # Auto-detect content type if not provided
            if not content_type:
                content_type, _ = mimetypes.guess_type(key)
                if not content_type:
                    content_type = 'application/octet-stream'
            
            # Prepare metadata
            s3_metadata = metadata or {}
            s3_metadata.update({
                'uploaded-by': 'ai-erp-system',
                'upload-timestamp': datetime.now().isoformat(),
                'file-hash': hashlib.sha256(file_data).hexdigest()
            })
            
            # Determine optimal storage class
            optimal_storage_class = self._determine_storage_class(
                file_size=len(file_data),
                content_type=content_type,
                access_pattern=kwargs.get('access_pattern', 'standard')
            )
            
            # Upload file
            extra_args = {
                'ContentType': content_type,
                'Metadata': s3_metadata,
                'StorageClass': optimal_storage_class.value
            }
            
            # Enable server-side encryption
            extra_args['ServerSideEncryption'] = 'AES256'
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_data,
                **extra_args
            )
            
            # Generate presigned URL if needed
            url = None
            if kwargs.get('generate_url', False):
                url = self._generate_presigned_url(key, expires_in=3600)
            
            # Calculate cost estimate
            cost_estimate = self._calculate_upload_cost(
                file_size=len(file_data),
                storage_class=optimal_storage_class
            )
            
            logger.info(f"Successfully uploaded {key} to S3 ({len(file_data)} bytes)")
            
            return UploadResult(
                success=True,
                key=key,
                bucket=self.bucket_name,
                url=url,
                etag=hashlib.md5(file_data).hexdigest(),
                cost_estimate=cost_estimate
            )
            
        except Exception as e:
            logger.error(f"Error uploading file {key}: {str(e)}")
            return UploadResult(
                success=False,
                key=key,
                bucket=self.bucket_name,
                error=str(e)
            )
    
    async def download_file(self, key: str) -> Tuple[bool, Optional[bytes], Optional[str]]:
        """
        Download file from S3
        """
        
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            file_data = response['Body'].read()
            
            logger.info(f"Successfully downloaded {key} from S3")
            return True, file_data, None
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                return False, None, "File not found"
            else:
                logger.error(f"Error downloading file {key}: {str(e)}")
                return False, None, str(e)
        except Exception as e:
            logger.error(f"Error downloading file {key}: {str(e)}")
            return False, None, str(e)
    
    async def delete_file(self, key: str) -> Tuple[bool, Optional[str]]:
        """
        Delete file from S3
        """
        
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"Successfully deleted {key} from S3")
            return True, None
            
        except Exception as e:
            logger.error(f"Error deleting file {key}: {str(e)}")
            return False, str(e)
    
    async def list_files(
        self, 
        prefix: str = "", 
        limit: int = 1000,
        continuation_token: str = None
    ) -> Tuple[List[AWSFile], Optional[str]]:
        """
        List files in S3 bucket with pagination
        """
        
        try:
            kwargs = {
                'Bucket': self.bucket_name,
                'MaxKeys': limit
            }
            
            if prefix:
                kwargs['Prefix'] = prefix
            
            if continuation_token:
                kwargs['ContinuationToken'] = continuation_token
            
            response = self.s3_client.list_objects_v2(**kwargs)
            
            files = []
            for obj in response.get('Contents', []):
                aws_file = AWSFile(
                    key=obj['Key'],
                    bucket=self.bucket_name,
                    size=obj['Size'],
                    etag=obj['ETag'].strip('"'),
                    last_modified=obj['LastModified'],
                    storage_class=obj.get('StorageClass', 'STANDARD'),
                    metadata={}
                )
                files.append(aws_file)
            
            next_token = response.get('NextContinuationToken')
            
            logger.info(f"Listed {len(files)} files from S3")
            return files, next_token
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return [], None
    
    async def get_file_metadata(self, key: str) -> Optional[AWSFile]:
        """
        Get file metadata without downloading content
        """
        
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=key)
            
            aws_file = AWSFile(
                key=key,
                bucket=self.bucket_name,
                size=response['ContentLength'],
                etag=response['ETag'].strip('"'),
                last_modified=response['LastModified'],
                storage_class=response.get('StorageClass', 'STANDARD'),
                metadata=response.get('Metadata', {})
            )
            
            return aws_file
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return None
            raise e
    
    def _generate_presigned_url(self, key: str, expires_in: int = 3600) -> str:
        """
        Generate presigned URL for temporary access
        """
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expires_in
            )
            return url
            
        except Exception as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return ""
    
    def _determine_storage_class(
        self, 
        file_size: int, 
        content_type: str,
        access_pattern: str
    ) -> StorageClass:
        """
        Determine optimal storage class based on file characteristics
        """
        
        # For frequently accessed files
        if access_pattern == 'frequent':
            return StorageClass.STANDARD
        
        # For infrequently accessed files
        if access_pattern == 'infrequent':
            return StorageClass.STANDARD_IA
        
        # For archive files
        if access_pattern == 'archive':
            return StorageClass.GLACIER_IR
        
        # Auto-determine based on file size and type
        if file_size < 128 * 1024:  # Files smaller than 128KB
            return StorageClass.STANDARD
        
        # Document types that might be accessed infrequently
        document_types = ['application/pdf', 'application/msword', 'text/plain']
        if content_type in document_types:
            return StorageClass.STANDARD_IA
        
        # Default to standard
        return StorageClass.STANDARD
    
    def _calculate_upload_cost(self, file_size: int, storage_class: StorageClass) -> float:
        """
        Estimate upload cost based on AWS pricing
        """
        
        # AWS S3 pricing (approximate, varies by region)
        pricing = {
            StorageClass.STANDARD: 0.023,  # per GB per month
            StorageClass.STANDARD_IA: 0.0125,
            StorageClass.GLACIER: 0.004,
            StorageClass.GLACIER_IR: 0.004,
            StorageClass.DEEP_ARCHIVE: 0.00099
        }
        
        # Calculate monthly storage cost
        file_size_gb = file_size / (1024 * 1024 * 1024)
        monthly_cost = file_size_gb * pricing.get(storage_class, 0.023)
        
        # Add request cost (PUT request)
        request_cost = 0.0005 / 1000  # $0.0005 per 1,000 PUT requests
        
        return monthly_cost + request_cost
    
    async def sync_directory(
        self, 
        local_path: str, 
        s3_prefix: str,
        delete_extra: bool = False
    ) -> Dict[str, Any]:
        """
        Sync local directory to S3
        """
        
        import os
        from pathlib import Path
        
        try:
            results = {
                'uploaded': 0,
                'skipped': 0,
                'deleted': 0,
                'errors': []
            }
            
            # Upload local files
            local_files = {}
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_path)
                    s3_key = f"{s3_prefix}/{relative_path}".replace('\\', '/')
                    
                    local_files[s3_key] = local_file_path
                    
                    # Check if file needs uploading
                    should_upload = True
                    try:
                        s3_file = await self.get_file_metadata(s3_key)
                        if s3_file:
                            local_mtime = datetime.fromtimestamp(os.path.getmtime(local_file_path))
                            if local_mtime <= s3_file.last_modified:
                                should_upload = False
                    except:
                        pass
                    
                    if should_upload:
                        try:
                            with open(local_file_path, 'rb') as f:
                                file_data = f.read()
                            
                            result = await self.upload_file(file_data, s3_key)
                            if result.success:
                                results['uploaded'] += 1
                            else:
                                results['errors'].append(f"Upload failed: {s3_key}")
                                
                        except Exception as e:
                            results['errors'].append(f"Error uploading {s3_key}: {str(e)}")
                    else:
                        results['skipped'] += 1
            
            # Delete extra S3 files if requested
            if delete_extra:
                s3_files, _ = await self.list_files(prefix=s3_prefix)
                for s3_file in s3_files:
                    if s3_file.key not in local_files:
                        success, error = await self.delete_file(s3_file.key)
                        if success:
                            results['deleted'] += 1
                        else:
                            results['errors'].append(f"Delete failed: {s3_file.key}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error syncing directory: {str(e)}")
            return {'error': str(e)}
    
    async def get_storage_analytics(self, prefix: str = "") -> Dict[str, Any]:
        """
        Get storage usage analytics
        """
        
        try:
            files, _ = await self.list_files(prefix=prefix, limit=10000)
            
            total_size = sum(f.size for f in files)
            total_files = len(files)
            
            # Storage class breakdown
            storage_classes = {}
            for f in files:
                storage_classes[f.storage_class] = storage_classes.get(f.storage_class, 0) + 1
            
            # File type breakdown
            file_types = {}
            for f in files:
                ext = f.key.split('.')[-1].lower() if '.' in f.key else 'no_extension'
                file_types[ext] = file_types.get(ext, 0) + 1
            
            # Calculate estimated monthly cost
            monthly_cost = 0.0
            for f in files:
                file_size_gb = f.size / (1024 * 1024 * 1024)
                if f.storage_class == 'STANDARD':
                    monthly_cost += file_size_gb * 0.023
                elif f.storage_class == 'STANDARD_IA':
                    monthly_cost += file_size_gb * 0.0125
                elif f.storage_class in ['GLACIER', 'GLACIER_IR']:
                    monthly_cost += file_size_gb * 0.004
                elif f.storage_class == 'DEEP_ARCHIVE':
                    monthly_cost += file_size_gb * 0.00099
            
            return {
                'total_files': total_files,
                'total_size_bytes': total_size,
                'total_size_gb': total_size / (1024 * 1024 * 1024),
                'storage_classes': storage_classes,
                'file_types': file_types,
                'estimated_monthly_cost': monthly_cost,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting storage analytics: {str(e)}")
            return {'error': str(e)}
    
    async def cleanup_old_versions(self, days: int = 30) -> Dict[str, int]:
        """
        Clean up old file versions to reduce costs
        """
        
        try:
            # This would require versioning to be enabled on the bucket
            # For now, return a placeholder result
            return {
                'versions_deleted': 0,
                'space_freed_bytes': 0,
                'message': 'Version cleanup requires bucket versioning to be enabled'
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up old versions: {str(e)}")
            return {'error': str(e)}


def create_aws_provider(**config) -> AWSProvider:
    """Factory function to create AWS provider"""
    return AWSProvider(config)