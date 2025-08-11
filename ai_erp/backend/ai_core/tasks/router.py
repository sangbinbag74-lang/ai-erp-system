"""
Task Router for AI ERP System

Intelligent routing system that analyzes user requests and routes them 
to appropriate ERP modules and AI handlers.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple, Callable
from enum import Enum
from dataclasses import dataclass
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks the AI can handle"""
    FILE_ANALYSIS = "file_analysis"
    DATA_QUERY = "data_query" 
    REPORT_GENERATION = "report_generation"
    INVENTORY_MANAGEMENT = "inventory_management"
    ACCOUNTING = "accounting"
    SALES = "sales"
    PURCHASING = "purchasing"
    MANUFACTURING = "manufacturing"
    HR = "hr"
    PROJECT_MANAGEMENT = "project_management"
    CRM = "crm"
    SYSTEM_ADMIN = "system_admin"
    GENERAL_INQUIRY = "general_inquiry"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Task:
    """Represents a task to be executed"""
    id: str
    type: TaskType
    description: str
    user_id: str
    parameters: Dict[str, Any]
    priority: Priority = Priority.MEDIUM
    created_at: datetime = None
    status: str = "pending"
    result: Optional[Any] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class TaskPattern:
    """Pattern for matching and routing tasks"""
    keywords: List[str]
    task_type: TaskType
    priority: Priority
    handler: str
    confidence_threshold: float = 0.3


class TaskRouter:
    """
    Intelligent task routing system for AI ERP
    """
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.handlers = {}
        self.middleware = []
        
    def _initialize_patterns(self) -> List[TaskPattern]:
        """Initialize task matching patterns"""
        
        return [
            # File Analysis
            TaskPattern(
                keywords=["analyze", "file", "document", "upload", "review", "scan", "process"],
                task_type=TaskType.FILE_ANALYSIS,
                priority=Priority.MEDIUM,
                handler="file_analysis_handler"
            ),
            
            # Data Queries
            TaskPattern(
                keywords=["show", "list", "find", "search", "query", "get", "display", "what", "how many"],
                task_type=TaskType.DATA_QUERY,
                priority=Priority.MEDIUM,
                handler="data_query_handler"
            ),
            
            # Reports
            TaskPattern(
                keywords=["report", "generate", "summary", "dashboard", "analytics", "statistics", "chart"],
                task_type=TaskType.REPORT_GENERATION,
                priority=Priority.HIGH,
                handler="report_handler"
            ),
            
            # Inventory Management
            TaskPattern(
                keywords=["inventory", "stock", "warehouse", "item", "product", "reorder", "shortage"],
                task_type=TaskType.INVENTORY_MANAGEMENT,
                priority=Priority.HIGH,
                handler="inventory_handler"
            ),
            
            # Accounting
            TaskPattern(
                keywords=["accounting", "ledger", "balance", "profit", "loss", "expense", "income", "tax", "financial"],
                task_type=TaskType.ACCOUNTING,
                priority=Priority.HIGH,
                handler="accounting_handler"
            ),
            
            # Sales
            TaskPattern(
                keywords=["sales", "customer", "order", "invoice", "quotation", "lead", "opportunity", "revenue"],
                task_type=TaskType.SALES,
                priority=Priority.HIGH,
                handler="sales_handler"
            ),
            
            # Purchasing
            TaskPattern(
                keywords=["purchase", "supplier", "vendor", "procurement", "buy", "order", "rfq", "receipt"],
                task_type=TaskType.PURCHASING,
                priority=Priority.HIGH,
                handler="purchasing_handler"
            ),
            
            # Manufacturing
            TaskPattern(
                keywords=["manufacturing", "production", "bom", "work order", "quality", "material", "planning"],
                task_type=TaskType.MANUFACTURING,
                priority=Priority.HIGH,
                handler="manufacturing_handler"
            ),
            
            # HR
            TaskPattern(
                keywords=["employee", "hr", "payroll", "attendance", "leave", "recruitment", "appraisal"],
                task_type=TaskType.HR,
                priority=Priority.MEDIUM,
                handler="hr_handler"
            ),
            
            # Project Management
            TaskPattern(
                keywords=["project", "task", "milestone", "timeline", "resource", "gantt", "planning"],
                task_type=TaskType.PROJECT_MANAGEMENT,
                priority=Priority.MEDIUM,
                handler="project_handler"
            ),
            
            # CRM
            TaskPattern(
                keywords=["crm", "contact", "communication", "campaign", "pipeline", "prospect"],
                task_type=TaskType.CRM,
                priority=Priority.MEDIUM,
                handler="crm_handler"
            ),
            
            # System Administration
            TaskPattern(
                keywords=["user", "permission", "role", "system", "setup", "configuration", "admin"],
                task_type=TaskType.SYSTEM_ADMIN,
                priority=Priority.LOW,
                handler="admin_handler"
            )
        ]
    
    def register_handler(self, handler_name: str, handler_func: Callable):
        """Register a task handler function"""
        self.handlers[handler_name] = handler_func
        logger.info(f"Registered handler: {handler_name}")
    
    def add_middleware(self, middleware_func: Callable):
        """Add middleware function that processes all tasks"""
        self.middleware.append(middleware_func)
        logger.info("Added middleware function")
    
    def analyze_request(self, user_input: str) -> Tuple[TaskType, float, Dict[str, Any]]:
        """
        Analyze user request and determine task type with confidence score
        """
        
        user_input_lower = user_input.lower()
        best_match = None
        best_score = 0.0
        extracted_params = {}
        
        for pattern in self.patterns:
            score = 0.0
            matched_keywords = []
            
            # Calculate keyword match score
            for keyword in pattern.keywords:
                if keyword in user_input_lower:
                    score += 1.0
                    matched_keywords.append(keyword)
                elif any(keyword in word for word in user_input_lower.split()):
                    score += 0.5
                    matched_keywords.append(keyword)
            
            # Normalize score by number of keywords
            if len(pattern.keywords) > 0:
                score = score / len(pattern.keywords)
            
            # Boost score for exact phrase matches
            for keyword in pattern.keywords:
                if len(keyword.split()) > 1 and keyword in user_input_lower:
                    score += 0.3
            
            if score > best_score and score >= pattern.confidence_threshold:
                best_score = score
                best_match = pattern
                extracted_params = {
                    "matched_keywords": matched_keywords,
                    "confidence": score,
                    "original_input": user_input
                }
        
        if best_match:
            return best_match.task_type, best_score, extracted_params
        else:
            return TaskType.GENERAL_INQUIRY, 0.1, {"original_input": user_input}
    
    def extract_entities(self, user_input: str) -> Dict[str, Any]:
        """
        Extract relevant entities from user input
        """
        
        entities = {}
        
        # Extract numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', user_input)
        if numbers:
            entities["numbers"] = [float(n) for n in numbers]
        
        # Extract dates (basic patterns)
        date_patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
            r'\b\d{2}/\d{2}/\d{4}\b',   # MM/DD/YYYY
            r'\b(?:today|yesterday|tomorrow)\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, user_input.lower()))
        
        if dates:
            entities["dates"] = dates
        
        # Extract common ERP entities
        erp_patterns = {
            "currencies": r'\b(?:USD|EUR|GBP|INR|JPY|\$|€|£|₹|¥)\b',
            "departments": r'\b(?:sales|accounting|hr|manufacturing|purchasing|admin)\b',
            "statuses": r'\b(?:draft|submitted|approved|cancelled|pending|completed)\b'
        }
        
        for entity_type, pattern in erp_patterns.items():
            matches = re.findall(pattern, user_input.lower())
            if matches:
                entities[entity_type] = matches
        
        return entities
    
    async def create_task(
        self, 
        user_input: str, 
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Task:
        """
        Create a task from user input
        """
        
        # Analyze the request
        task_type, confidence, params = self.analyze_request(user_input)
        
        # Extract entities
        entities = self.extract_entities(user_input)
        
        # Determine priority based on task type and keywords
        priority = self._determine_priority(user_input, task_type)
        
        # Create task
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{user_id[:8]}"
        
        task = Task(
            id=task_id,
            type=task_type,
            description=user_input,
            user_id=user_id,
            parameters={
                "confidence": confidence,
                "entities": entities,
                "context": context or {},
                **params
            },
            priority=priority
        )
        
        logger.info(f"Created task {task_id}: {task_type.value} (confidence: {confidence:.2f})")
        return task
    
    def _determine_priority(self, user_input: str, task_type: TaskType) -> Priority:
        """Determine task priority based on content and type"""
        
        urgent_keywords = ["urgent", "emergency", "asap", "immediately", "critical"]
        high_keywords = ["important", "priority", "needed", "required"]
        
        user_input_lower = user_input.lower()
        
        # Check for priority keywords
        if any(keyword in user_input_lower for keyword in urgent_keywords):
            return Priority.URGENT
        elif any(keyword in user_input_lower for keyword in high_keywords):
            return Priority.HIGH
        
        # Default priority based on task type
        high_priority_types = [
            TaskType.ACCOUNTING, 
            TaskType.INVENTORY_MANAGEMENT,
            TaskType.SALES,
            TaskType.PURCHASING,
            TaskType.MANUFACTURING
        ]
        
        if task_type in high_priority_types:
            return Priority.HIGH
        elif task_type in [TaskType.REPORT_GENERATION, TaskType.DATA_QUERY]:
            return Priority.MEDIUM
        else:
            return Priority.LOW
    
    async def route_task(self, task: Task) -> Any:
        """
        Route task to appropriate handler
        """
        
        try:
            # Apply middleware
            for middleware in self.middleware:
                task = await middleware(task) if asyncio.iscoroutinefunction(middleware) else middleware(task)
            
            # Find handler for task type
            handler_name = None
            for pattern in self.patterns:
                if pattern.task_type == task.type:
                    handler_name = pattern.handler
                    break
            
            if not handler_name or handler_name not in self.handlers:
                raise ValueError(f"No handler found for task type: {task.type.value}")
            
            # Execute handler
            handler = self.handlers[handler_name]
            
            logger.info(f"Routing task {task.id} to {handler_name}")
            
            if asyncio.iscoroutinefunction(handler):
                result = await handler(task)
            else:
                result = handler(task)
            
            task.status = "completed"
            task.result = result
            
            return result
            
        except Exception as e:
            logger.error(f"Error routing task {task.id}: {str(e)}")
            task.status = "failed"
            task.error = str(e)
            raise
    
    async def process_user_request(
        self, 
        user_input: str, 
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[Task, Any]:
        """
        Complete flow: create task and route it
        """
        
        # Create task from user input
        task = await self.create_task(user_input, user_id, context)
        
        # Route and execute task
        result = await self.route_task(task)
        
        return task, result
    
    def get_supported_task_types(self) -> List[str]:
        """Get list of supported task types"""
        return [task_type.value for task_type in TaskType]
    
    def get_task_examples(self) -> Dict[str, List[str]]:
        """Get example queries for each task type"""
        
        examples = {
            TaskType.FILE_ANALYSIS.value: [
                "Analyze this invoice file",
                "Process the uploaded document",
                "Review this customer data sheet"
            ],
            TaskType.DATA_QUERY.value: [
                "Show me all pending sales orders",
                "List customers from New York",
                "How many items are in stock?"
            ],
            TaskType.REPORT_GENERATION.value: [
                "Generate monthly sales report",
                "Create inventory summary dashboard",
                "Show profit and loss statement"
            ],
            TaskType.INVENTORY_MANAGEMENT.value: [
                "Check stock levels for Item X",
                "Update inventory quantities",
                "Create reorder report"
            ],
            TaskType.ACCOUNTING.value: [
                "Show general ledger",
                "Calculate tax liability",
                "Generate balance sheet"
            ],
            TaskType.SALES.value: [
                "Create sales order for customer ABC",
                "Show sales pipeline",
                "Update quotation status"
            ]
        }
        
        return examples


# Default handlers (to be implemented by specific modules)
async def default_file_analysis_handler(task: Task) -> Dict[str, Any]:
    """Default file analysis handler"""
    return {
        "message": "File analysis functionality not implemented yet",
        "task_id": task.id
    }

async def default_data_query_handler(task: Task) -> Dict[str, Any]:
    """Default data query handler"""
    return {
        "message": "Data query functionality not implemented yet", 
        "task_id": task.id
    }

async def default_general_handler(task: Task) -> Dict[str, Any]:
    """Default handler for unclassified tasks"""
    return {
        "message": f"I understand you want help with: {task.description}. This functionality is being developed.",
        "task_id": task.id,
        "suggestions": [
            "Try asking about specific ERP modules like 'sales', 'inventory', or 'accounting'",
            "Upload a file for analysis",
            "Ask for a specific report"
        ]
    }


# Factory function
def create_task_router() -> TaskRouter:
    """Factory function to create and configure task router"""
    
    router = TaskRouter()
    
    # Register default handlers
    router.register_handler("file_analysis_handler", default_file_analysis_handler)
    router.register_handler("data_query_handler", default_data_query_handler) 
    router.register_handler("report_handler", default_general_handler)
    router.register_handler("inventory_handler", default_general_handler)
    router.register_handler("accounting_handler", default_general_handler)
    router.register_handler("sales_handler", default_general_handler)
    router.register_handler("purchasing_handler", default_general_handler)
    router.register_handler("manufacturing_handler", default_general_handler)
    router.register_handler("hr_handler", default_general_handler)
    router.register_handler("project_handler", default_general_handler)
    router.register_handler("crm_handler", default_general_handler)
    router.register_handler("admin_handler", default_general_handler)
    
    return router