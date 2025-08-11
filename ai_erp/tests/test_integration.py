"""
Integration Tests for AI ERP System

Comprehensive integration tests covering all major components
and their interactions.
"""

import pytest
import asyncio
import tempfile
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import modules to test
from backend.ai_core.llm.api_client import create_llm_client
from backend.ai_core.context.manager import create_context_manager
from backend.ai_core.tasks.router import create_task_router

from backend.file_manager.processors.document_processor import create_document_processor
from backend.file_manager.analyzers.content_analyzer import create_content_analyzer

from backend.team_manager.services.team_service import create_team_service
from backend.team_manager.models.team_models import UserRole, SubscriptionTier

from backend.cloud_storage.managers.storage_manager import create_storage_manager

from backend.billing.services.subscription_service import create_subscription_service
from backend.billing.models.subscription_models import BillingPeriod, UsageMetric


class MockLLMClient:
    """Mock LLM client for testing"""
    
    async def generate_response(self, messages, **kwargs):
        class MockResponse:
            def __init__(self, content):
                self.content = content
                self.tokens_used = 100
                self.model = "test-model"
                self.cost_estimate = 0.001
        
        return MockResponse("Test response from mock LLM")
    
    async def analyze_file(self, content, file_type, **kwargs):
        return await self.generate_response("Analyze this file", **kwargs)
    
    async def process_query(self, query, context=None, **kwargs):
        return await self.generate_response(f"Query: {query}", **kwargs)


@pytest.fixture
def mock_llm_client():
    """Provide mock LLM client"""
    return MockLLMClient()


@pytest.fixture
def test_config():
    """Provide test configuration"""
    return {
        'test_mode': True,
        'storage': {
            'default_provider': 'aws_s3',
            'aws': {
                'enabled': False,  # Disabled for tests
                'bucket_name': 'test-bucket'
            }
        }
    }


class TestAICoreIntegration:
    """Test AI core functionality integration"""
    
    @pytest.mark.asyncio
    async def test_llm_client_creation(self, mock_llm_client):
        """Test LLM client creation and basic operation"""
        
        # Test response generation
        response = await mock_llm_client.generate_response("Hello, AI!")
        
        assert response is not None
        assert response.content == "Test response from mock LLM"
        assert response.tokens_used > 0
        assert response.cost_estimate > 0
    
    @pytest.mark.asyncio
    async def test_context_manager_basic_operations(self):
        """Test context manager basic operations"""
        
        context_manager = create_context_manager()
        
        # Test user session storage
        from backend.ai_core.context.manager import UserSession, ContextType
        
        session = UserSession(
            user_id="test_user",
            session_id="test_session",
            company_id="test_company",
            role="user",
            permissions=["read", "write"],
            preferences={},
            active_modules=["erp"]
        )
        
        session_id = await context_manager.store_user_session(session)
        assert session_id is not None
        
        # Retrieve session
        retrieved_session = await context_manager.get_user_session("test_session")
        assert retrieved_session is not None
        assert retrieved_session.user_id == "test_user"
    
    @pytest.mark.asyncio
    async def test_task_router_integration(self):
        """Test task router with various inputs"""
        
        task_router = create_task_router()
        
        test_queries = [
            "Show me all customers",
            "Generate a sales report", 
            "Upload and analyze this file",
            "Create a new team member"
        ]
        
        for query in test_queries:
            task, result = await task_router.process_user_request(
                user_input=query,
                user_id="test_user"
            )
            
            assert task is not None
            assert task.description == query
            assert task.user_id == "test_user"
            assert result is not None


class TestFileManagementIntegration:
    """Test file management functionality"""
    
    @pytest.mark.asyncio
    async def test_document_processing_pipeline(self, mock_llm_client):
        """Test complete document processing pipeline"""
        
        # Create processor and analyzer
        document_processor = create_document_processor()
        content_analyzer = create_content_analyzer(llm_client=mock_llm_client)
        
        # Test document
        test_content = """
        INVOICE #INV-2024-001
        
        Bill To: Test Customer
        Amount: $1,500.00
        Due Date: 2024-02-15
        
        Description: Consulting services
        """
        
        # Process document
        doc_info, extracted_content = await document_processor.process_document(
            file_data=test_content.encode('utf-8'),
            filename="test_invoice.txt",
            user_id="test_user"
        )
        
        assert doc_info is not None
        assert doc_info.filename == "test_invoice.txt"
        assert extracted_content is not None
        assert len(extracted_content.text) > 0
        
        # Analyze content
        analysis = await content_analyzer.analyze_content(
            content=extracted_content.text,
            document_type="txt"
        )
        
        assert analysis is not None
        assert analysis.category is not None
        assert analysis.confidence >= 0
        assert isinstance(analysis.key_insights, list)
    
    @pytest.mark.asyncio
    async def test_batch_processing(self, mock_llm_client):
        """Test batch file processing"""
        
        document_processor = create_document_processor()
        content_analyzer = create_content_analyzer(llm_client=mock_llm_client)
        
        # Multiple test files
        test_files = [
            ("file1.txt", "This is test file 1 content"),
            ("file2.txt", "This is test file 2 content"),
            ("file3.txt", "This is test file 3 content")
        ]
        
        # Convert to bytes
        files_data = [(content.encode('utf-8'), filename) for filename, content in test_files]
        
        # Batch process
        results = await document_processor.batch_process(
            files=files_data,
            user_id="test_user"
        )
        
        assert len(results) == 3
        
        for doc_info, extracted_content in results:
            assert doc_info is not None
            if extracted_content:  # Some might fail in test environment
                assert len(extracted_content.text) > 0


class TestTeamManagementIntegration:
    """Test team management functionality"""
    
    @pytest.mark.asyncio
    async def test_complete_team_workflow(self, mock_llm_client):
        """Test complete team management workflow"""
        
        team_service = create_team_service(llm_client=mock_llm_client)
        
        # Create team
        team, owner = await team_service.create_team(
            name="Test Team",
            owner_id="owner_123",
            owner_email="owner@test.com",
            owner_name="Team Owner"
        )
        
        assert team is not None
        assert team.name == "Test Team"
        assert owner is not None
        assert owner.role == UserRole.OWNER
        
        # Invite member
        invitation = await team_service.invite_member(
            team_id=team.id,
            email="member@test.com",
            invited_by="owner_123",
            role=UserRole.USER
        )
        
        assert invitation is not None
        assert invitation.email == "member@test.com"
        assert invitation.role == UserRole.USER
        
        # Accept invitation
        updated_team, new_member = await team_service.accept_invitation(
            token=invitation.token,
            user_id="member_456",
            user_name="New Member",
            user_email="member@test.com"
        )
        
        assert updated_team is not None
        assert new_member is not None
        assert updated_team.member_count == 2
    
    @pytest.mark.asyncio
    async def test_team_analytics_generation(self, mock_llm_client):
        """Test team analytics generation"""
        
        team_service = create_team_service(llm_client=mock_llm_client)
        
        # Create team first
        team, owner = await team_service.create_team(
            name="Analytics Test Team",
            owner_id="owner_123",
            owner_email="owner@test.com",
            owner_name="Team Owner"
        )
        
        # Generate analytics
        analytics = await team_service.get_team_analytics(
            team_id=team.id,
            user_id="owner_123",
            days=30
        )
        
        assert analytics is not None
        assert analytics.team_id == team.id
        assert analytics.active_members >= 1
        assert 0 <= analytics.productivity_score <= 1
        assert 0 <= analytics.collaboration_rating <= 1


class TestStorageIntegration:
    """Test cloud storage integration"""
    
    @pytest.mark.asyncio
    async def test_storage_manager_operations(self, mock_llm_client, test_config):
        """Test storage manager basic operations"""
        
        storage_manager = create_storage_manager(
            config=test_config['storage'],
            llm_client=mock_llm_client
        )
        
        test_content = "This is test file content for storage"
        
        # Note: This test will use mock storage since AWS is disabled
        # In a real test environment, you'd use a test bucket
        
        # Test file listing (should work even with mock)
        files = await storage_manager.list_files(
            user_id="test_user",
            team_id="test_team"
        )
        
        assert isinstance(files, list)
    
    @pytest.mark.asyncio
    async def test_storage_analytics(self, mock_llm_client, test_config):
        """Test storage analytics generation"""
        
        storage_manager = create_storage_manager(
            config=test_config['storage'],
            llm_client=mock_llm_client
        )
        
        analytics = await storage_manager.get_storage_analytics(
            user_id="test_user",
            team_id="test_team"
        )
        
        assert isinstance(analytics, dict)
        assert 'total_files' in analytics
        assert 'total_size_bytes' in analytics


class TestBillingIntegration:
    """Test billing and subscription integration"""
    
    @pytest.mark.asyncio
    async def test_subscription_lifecycle(self):
        """Test complete subscription lifecycle"""
        
        subscription_service = create_subscription_service()
        
        # Create subscription
        success, subscription, error = await subscription_service.create_subscription(
            team_id="test_team_123",
            plan_id="free",
            billing_period=BillingPeriod.MONTHLY
        )
        
        assert success is True
        assert subscription is not None
        assert subscription.team_id == "test_team_123"
        assert error is None
        
        # Track usage
        success, result = await subscription_service.track_usage(
            team_id="test_team_123",
            metric=UsageMetric.AI_QUERIES,
            amount=5
        )
        
        assert success is True
        assert 'quota' in result or 'message' in result
        
        # Get usage analytics
        analytics = await subscription_service.get_usage_analytics(
            team_id="test_team_123",
            period_days=30
        )
        
        assert 'error' not in analytics
        assert 'subscription_id' in analytics
    
    @pytest.mark.asyncio
    async def test_subscription_upgrade(self):
        """Test subscription upgrade process"""
        
        subscription_service = create_subscription_service()
        
        # Create initial subscription
        success, subscription, error = await subscription_service.create_subscription(
            team_id="upgrade_test_team",
            plan_id="free"
        )
        
        assert success is True
        
        # Upgrade subscription
        success, upgraded_sub, error = await subscription_service.upgrade_subscription(
            team_id="upgrade_test_team",
            target_plan_id="basic"
        )
        
        assert success is True
        assert upgraded_sub is not None
        assert upgraded_sub.plan_id == "basic"
    
    def test_billing_plans_access(self):
        """Test billing plans access and comparison"""
        
        subscription_service = create_subscription_service()
        
        # Get all plans
        plans = subscription_service.get_billing_plans()
        assert len(plans) > 0
        
        # Get plan comparison
        comparison = subscription_service.get_plan_comparison()
        assert 'plans' in comparison
        assert 'features' in comparison
        assert len(comparison['plans']) > 0


class TestSystemIntegration:
    """Test complete system integration"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self, mock_llm_client, test_config):
        """Test end-to-end workflow"""
        
        # Initialize all components
        team_service = create_team_service(llm_client=mock_llm_client)
        subscription_service = create_subscription_service()
        document_processor = create_document_processor()
        task_router = create_task_router()
        
        # 1. Create team and subscription
        team, owner = await team_service.create_team(
            name="Integration Test Team",
            owner_id="integration_user",
            owner_email="integration@test.com",
            owner_name="Integration User"
        )
        
        success, subscription, error = await subscription_service.create_subscription(
            team_id=team.id,
            plan_id="free"
        )
        
        assert success is True
        
        # 2. Process a document
        test_document = "Test document content for integration testing"
        doc_info, extracted_content = await document_processor.process_document(
            file_data=test_document.encode('utf-8'),
            filename="integration_test.txt",
            user_id="integration_user"
        )
        
        assert doc_info is not None
        assert extracted_content is not None
        
        # 3. Process user queries
        queries = [
            "Show me team analytics",
            "Process the uploaded document",
            "Generate usage report"
        ]
        
        for query in queries:
            task, result = await task_router.process_user_request(
                user_input=query,
                user_id="integration_user",
                context={'team_id': team.id}
            )
            
            assert task is not None
            assert result is not None
        
        # 4. Track usage
        success, result = await subscription_service.track_usage(
            team_id=team.id,
            metric=UsageMetric.FILES_PROCESSED,
            amount=1
        )
        
        assert success is True
        
        # 5. Get team analytics
        analytics = await team_service.get_team_analytics(
            team_id=team.id,
            user_id="integration_user"
        )
        
        assert analytics is not None
    
    @pytest.mark.asyncio
    async def test_error_handling_and_recovery(self, mock_llm_client):
        """Test error handling and recovery mechanisms"""
        
        team_service = create_team_service(llm_client=mock_llm_client)
        
        # Test invalid operations
        
        # Try to create team with invalid data
        with pytest.raises(Exception):
            await team_service.create_team(
                name="",  # Invalid name
                owner_id="test_user",
                owner_email="invalid_email",  # Invalid email format might cause issues
                owner_name="Test User"
            )
        
        # Try to invite to non-existent team
        with pytest.raises(Exception):
            await team_service.invite_member(
                team_id="non_existent_team",
                email="test@test.com",
                invited_by="test_user"
            )
        
        # Test subscription service error handling
        subscription_service = create_subscription_service()
        
        # Try to create subscription with invalid plan
        success, subscription, error = await subscription_service.create_subscription(
            team_id="test_team",
            plan_id="non_existent_plan"
        )
        
        assert success is False
        assert error is not None


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])