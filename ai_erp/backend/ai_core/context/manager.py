"""
Context Manager for AI ERP System

Manages conversation context, user session data, and intelligent caching
for enhanced AI interactions across the ERP system.
"""

import json
import redis
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class ContextType(Enum):
    USER_SESSION = "user_session"
    CONVERSATION = "conversation"
    DOCUMENT = "document"
    TASK = "task"
    ANALYSIS = "analysis"


@dataclass
class ContextEntry:
    """Single context entry"""
    id: str
    type: ContextType
    content: Any
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime] = None
    access_count: int = 0
    last_accessed: Optional[datetime] = None


@dataclass 
class UserSession:
    """User session information"""
    user_id: str
    session_id: str
    company_id: str
    role: str
    permissions: List[str]
    preferences: Dict[str, Any]
    active_modules: List[str]


class ContextManager:
    """
    Advanced context management system for AI ERP
    """
    
    def __init__(self, redis_client: Optional[redis.Redis] = None, config: Dict[str, Any] = None):
        self.config = config or {}
        self.redis_client = redis_client or redis.Redis(
            host=self.config.get('redis_host', 'localhost'),
            port=self.config.get('redis_port', 6379),
            db=self.config.get('redis_db', 0),
            decode_responses=True
        )
        
        # Configuration
        self.max_conversation_length = self.config.get('max_conversation_length', 50)
        self.default_ttl = self.config.get('default_ttl', 3600)  # 1 hour
        self.max_context_size = self.config.get('max_context_size', 10000)  # characters
        
        # Namespace prefixes
        self.prefixes = {
            ContextType.USER_SESSION: "session:",
            ContextType.CONVERSATION: "conv:",
            ContextType.DOCUMENT: "doc:",
            ContextType.TASK: "task:",
            ContextType.ANALYSIS: "analysis:"
        }
    
    def _generate_key(self, context_type: ContextType, identifier: str) -> str:
        """Generate Redis key for context entry"""
        prefix = self.prefixes[context_type]
        return f"ai_erp:{prefix}{identifier}"
    
    def _serialize_context(self, context: ContextEntry) -> str:
        """Serialize context entry for storage"""
        data = asdict(context)
        data['created_at'] = data['created_at'].isoformat()
        if data['expires_at']:
            data['expires_at'] = data['expires_at'].isoformat()
        if data['last_accessed']:
            data['last_accessed'] = data['last_accessed'].isoformat()
        data['type'] = data['type'].value
        return json.dumps(data, default=str)
    
    def _deserialize_context(self, data: str) -> ContextEntry:
        """Deserialize context entry from storage"""
        parsed = json.loads(data)
        parsed['created_at'] = datetime.fromisoformat(parsed['created_at'])
        if parsed['expires_at']:
            parsed['expires_at'] = datetime.fromisoformat(parsed['expires_at'])
        if parsed['last_accessed']:
            parsed['last_accessed'] = datetime.fromisoformat(parsed['last_accessed'])
        parsed['type'] = ContextType(parsed['type'])
        return ContextEntry(**parsed)
    
    async def store_context(
        self, 
        context_type: ContextType, 
        identifier: str, 
        content: Any,
        metadata: Optional[Dict[str, Any]] = None,
        ttl: Optional[int] = None
    ) -> str:
        """Store context entry"""
        
        try:
            context_id = f"{identifier}_{hashlib.md5(str(content).encode()).hexdigest()[:8]}"
            key = self._generate_key(context_type, context_id)
            
            expires_at = None
            if ttl or self.default_ttl:
                expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
            
            context_entry = ContextEntry(
                id=context_id,
                type=context_type,
                content=content,
                metadata=metadata or {},
                created_at=datetime.now(),
                expires_at=expires_at
            )
            
            serialized = self._serialize_context(context_entry)
            
            # Store in Redis
            if ttl or self.default_ttl:
                self.redis_client.setex(key, ttl or self.default_ttl, serialized)
            else:
                self.redis_client.set(key, serialized)
            
            logger.info(f"Stored context: {context_type.value} - {context_id}")
            return context_id
            
        except Exception as e:
            logger.error(f"Error storing context: {str(e)}")
            raise
    
    async def get_context(
        self, 
        context_type: ContextType, 
        identifier: str,
        update_access: bool = True
    ) -> Optional[ContextEntry]:
        """Retrieve context entry"""
        
        try:
            key = self._generate_key(context_type, identifier)
            data = self.redis_client.get(key)
            
            if not data:
                return None
            
            context = self._deserialize_context(data)
            
            # Update access tracking
            if update_access:
                context.access_count += 1
                context.last_accessed = datetime.now()
                
                # Store updated context
                serialized = self._serialize_context(context)
                self.redis_client.set(key, serialized, xx=True)  # Only if exists
            
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return None
    
    async def store_user_session(self, session: UserSession, ttl: int = 86400) -> str:
        """Store user session context"""
        
        session_data = {
            "user_id": session.user_id,
            "session_id": session.session_id,
            "company_id": session.company_id,
            "role": session.role,
            "permissions": session.permissions,
            "preferences": session.preferences,
            "active_modules": session.active_modules
        }
        
        return await self.store_context(
            ContextType.USER_SESSION,
            session.session_id,
            session_data,
            metadata={"user_id": session.user_id},
            ttl=ttl
        )
    
    async def get_user_session(self, session_id: str) -> Optional[UserSession]:
        """Get user session"""
        
        context = await self.get_context(ContextType.USER_SESSION, session_id)
        if not context:
            return None
        
        data = context.content
        return UserSession(**data)
    
    async def store_conversation(
        self, 
        user_id: str, 
        messages: List[Dict[str, Any]],
        conversation_id: Optional[str] = None
    ) -> str:
        """Store conversation context"""
        
        if not conversation_id:
            conversation_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Limit conversation length
        if len(messages) > self.max_conversation_length:
            messages = messages[-self.max_conversation_length:]
        
        # Calculate total size and truncate if needed
        total_size = sum(len(str(msg)) for msg in messages)
        if total_size > self.max_context_size:
            # Keep most recent messages within size limit
            truncated_messages = []
            current_size = 0
            
            for msg in reversed(messages):
                msg_size = len(str(msg))
                if current_size + msg_size <= self.max_context_size:
                    truncated_messages.insert(0, msg)
                    current_size += msg_size
                else:
                    break
            
            messages = truncated_messages
            logger.warning(f"Conversation truncated to fit size limit: {len(messages)} messages")
        
        return await self.store_context(
            ContextType.CONVERSATION,
            conversation_id,
            messages,
            metadata={
                "user_id": user_id,
                "message_count": len(messages),
                "total_size": sum(len(str(msg)) for msg in messages)
            }
        )
    
    async def get_conversation(
        self, 
        conversation_id: str, 
        user_id: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Get conversation history"""
        
        context = await self.get_context(ContextType.CONVERSATION, conversation_id)
        if not context:
            return None
        
        # Check user access if provided
        if user_id and context.metadata.get("user_id") != user_id:
            logger.warning(f"User {user_id} attempted to access conversation {conversation_id}")
            return None
        
        return context.content
    
    async def append_to_conversation(
        self, 
        conversation_id: str, 
        message: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> bool:
        """Append message to existing conversation"""
        
        messages = await self.get_conversation(conversation_id, user_id)
        if messages is None:
            # Start new conversation
            messages = []
        
        messages.append(message)
        
        # Update conversation
        await self.store_conversation(user_id or "system", messages, conversation_id)
        return True
    
    async def store_document_analysis(
        self, 
        document_id: str, 
        analysis: Dict[str, Any],
        user_id: str
    ) -> str:
        """Store document analysis results"""
        
        return await self.store_context(
            ContextType.DOCUMENT,
            document_id,
            analysis,
            metadata={"user_id": user_id, "document_id": document_id}
        )
    
    async def get_document_analysis(
        self, 
        document_id: str,
        user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get document analysis"""
        
        context = await self.get_context(ContextType.DOCUMENT, document_id)
        if not context:
            return None
        
        # Check user access
        if user_id and context.metadata.get("user_id") != user_id:
            return None
        
        return context.content
    
    async def store_task_context(
        self, 
        task_id: str, 
        task_data: Dict[str, Any],
        user_id: str
    ) -> str:
        """Store task execution context"""
        
        return await self.store_context(
            ContextType.TASK,
            task_id,
            task_data,
            metadata={"user_id": user_id, "task_id": task_id},
            ttl=7200  # 2 hours for tasks
        )
    
    async def get_task_context(
        self, 
        task_id: str,
        user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get task context"""
        
        context = await self.get_context(ContextType.TASK, task_id)
        if not context:
            return None
        
        if user_id and context.metadata.get("user_id") != user_id:
            return None
        
        return context.content
    
    async def cleanup_expired_contexts(self) -> int:
        """Clean up expired context entries"""
        
        cleaned_count = 0
        
        try:
            # Get all AI ERP keys
            pattern = "ai_erp:*"
            keys = self.redis_client.keys(pattern)
            
            for key in keys:
                try:
                    data = self.redis_client.get(key)
                    if data:
                        context = self._deserialize_context(data)
                        if context.expires_at and datetime.now() > context.expires_at:
                            self.redis_client.delete(key)
                            cleaned_count += 1
                except Exception as e:
                    logger.warning(f"Error checking expiry for {key}: {str(e)}")
                    continue
            
            logger.info(f"Cleaned up {cleaned_count} expired contexts")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return cleaned_count
    
    async def get_context_stats(self) -> Dict[str, Any]:
        """Get context storage statistics"""
        
        stats = {
            "total_contexts": 0,
            "by_type": {},
            "memory_usage": 0
        }
        
        try:
            pattern = "ai_erp:*"
            keys = self.redis_client.keys(pattern)
            stats["total_contexts"] = len(keys)
            
            for context_type in ContextType:
                type_pattern = f"ai_erp:{self.prefixes[context_type]}*"
                type_keys = self.redis_client.keys(type_pattern)
                stats["by_type"][context_type.value] = len(type_keys)
            
            # Estimate memory usage
            info = self.redis_client.info('memory')
            stats["memory_usage"] = info.get('used_memory', 0)
            
        except Exception as e:
            logger.error(f"Error getting context stats: {str(e)}")
        
        return stats
    
    async def clear_user_contexts(self, user_id: str) -> int:
        """Clear all contexts for a specific user"""
        
        cleared_count = 0
        
        try:
            pattern = "ai_erp:*"
            keys = self.redis_client.keys(pattern)
            
            for key in keys:
                try:
                    data = self.redis_client.get(key)
                    if data:
                        context = self._deserialize_context(data)
                        if context.metadata.get("user_id") == user_id:
                            self.redis_client.delete(key)
                            cleared_count += 1
                except Exception:
                    continue
            
            logger.info(f"Cleared {cleared_count} contexts for user {user_id}")
            return cleared_count
            
        except Exception as e:
            logger.error(f"Error clearing user contexts: {str(e)}")
            return cleared_count


# Factory function
def create_context_manager(redis_config: Optional[Dict] = None, **kwargs) -> ContextManager:
    """Factory function to create context manager"""
    
    redis_client = None
    if redis_config:
        redis_client = redis.Redis(**redis_config, decode_responses=True)
    
    return ContextManager(redis_client=redis_client, config=kwargs)