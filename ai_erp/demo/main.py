"""
AI ERP System Demo Application

Demonstrates the complete AI-powered ERP system functionality
including LLM integration, file management, team operations, and more.
"""

import asyncio
import os
import sys
from pathlib import Path
import json
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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


class AIERPDemo:
    """
    Demo application showcasing AI ERP capabilities
    """
    
    def __init__(self):
        self.llm_client = None
        self.context_manager = None
        self.task_router = None
        self.document_processor = None
        self.content_analyzer = None
        self.team_service = None
        self.storage_manager = None
        self.subscription_service = None
        
        # Demo data
        self.demo_team_id = None
        self.demo_user_id = "user_demo_123"
        self.demo_user_email = "demo@ai-erp.com"
        self.demo_user_name = "Demo User"
    
    async def initialize(self):
        """Initialize all AI ERP components"""
        
        print("🚀 Initializing AI ERP Demo System...")
        
        try:
            # Initialize LLM client (using mock for demo)
            print("  📡 Setting up LLM client...")
            self.llm_client = await self._create_mock_llm_client()
            
            # Initialize context manager
            print("  🧠 Setting up context manager...")
            self.context_manager = create_context_manager()
            
            # Initialize task router
            print("  🛣️  Setting up task router...")
            self.task_router = create_task_router()
            
            # Initialize document processor
            print("  📄 Setting up document processor...")
            self.document_processor = create_document_processor()
            
            # Initialize content analyzer
            print("  🔍 Setting up content analyzer...")
            self.content_analyzer = create_content_analyzer(llm_client=self.llm_client)
            
            # Initialize team service
            print("  👥 Setting up team service...")
            self.team_service = create_team_service(llm_client=self.llm_client)
            
            # Initialize storage manager
            print("  ☁️  Setting up cloud storage...")
            storage_config = self._get_demo_storage_config()
            self.storage_manager = create_storage_manager(
                config=storage_config, 
                llm_client=self.llm_client
            )
            
            # Initialize subscription service
            print("  💳 Setting up subscription service...")
            self.subscription_service = create_subscription_service()
            
            print("✅ AI ERP System initialized successfully!\n")
            
        except Exception as e:
            print(f"❌ Error initializing AI ERP system: {str(e)}")
            raise
    
    async def run_demo(self):
        """Run the complete demo workflow"""
        
        print("🎯 Starting AI ERP Demo Workflow\n")
        
        try:
            # 1. Team Setup Demo
            await self._demo_team_setup()
            
            # 2. File Management Demo
            await self._demo_file_management()
            
            # 3. AI Processing Demo
            await self._demo_ai_processing()
            
            # 4. Subscription Management Demo
            await self._demo_subscription_management()
            
            # 5. Analytics and Insights Demo
            await self._demo_analytics_insights()
            
            print("\n🎉 Demo completed successfully!")
            print("💡 AI ERP System is ready for production deployment!")
            
        except Exception as e:
            print(f"❌ Demo error: {str(e)}")
            raise
    
    async def _demo_team_setup(self):
        """Demonstrate team setup and management"""
        
        print("👥 DEMO 1: Team Setup and Management")
        print("=" * 50)
        
        # Create a team
        print("Creating demo team...")
        team, owner = await self.team_service.create_team(
            name="AI ERP Demo Company",
            owner_id=self.demo_user_id,
            owner_email=self.demo_user_email,
            owner_name=self.demo_user_name,
            description="Demo company for AI ERP system",
            subscription_tier=SubscriptionTier.FREE
        )
        
        self.demo_team_id = team.id
        print(f"✅ Created team: {team.name} (ID: {team.id})")
        print(f"   Owner: {owner.name} ({owner.role.value})")
        print(f"   Members: {team.member_count}/{team.member_limit}")
        
        # Invite team members
        print("\nInviting team members...")
        
        # Invite a manager
        invitation = await self.team_service.invite_member(
            team_id=team.id,
            email="manager@ai-erp.com",
            invited_by=self.demo_user_id,
            role=UserRole.MANAGER,
            message="Welcome to our AI ERP demo team!"
        )
        
        print(f"✅ Invited manager: {invitation.email}")
        print(f"   Role: {invitation.role.value}")
        print(f"   Invitation expires: {invitation.expires_at}")
        
        # Simulate accepting invitation
        team, member = await self.team_service.accept_invitation(
            token=invitation.token,
            user_id="user_manager_456",
            user_name="Demo Manager",
            user_email="manager@ai-erp.com"
        )
        
        print(f"✅ Invitation accepted by: {member.name}")
        print(f"   Team now has {team.member_count} members")
        
        # Get team analytics
        print("\nGenerating team analytics...")
        analytics = await self.team_service.get_team_analytics(
            team_id=team.id,
            user_id=self.demo_user_id,
            days=30
        )
        
        if analytics:
            print(f"✅ Team Analytics Generated:")
            print(f"   Active members: {analytics.active_members}")
            print(f"   Productivity score: {analytics.productivity_score:.2f}")
            print(f"   Collaboration rating: {analytics.collaboration_rating:.2f}")
            
            if analytics.recommendations:
                print("   Recommendations:")
                for rec in analytics.recommendations[:3]:
                    print(f"   • {rec}")
        
        print("\n✅ Team setup demo completed!\n")
    
    async def _demo_file_management(self):
        """Demonstrate file management capabilities"""
        
        print("📁 DEMO 2: AI-Powered File Management")
        print("=" * 50)
        
        # Create sample files
        sample_files = [
            ("invoice.txt", "INVOICE #INV-2024-001\n\nBill To: Demo Customer\nAmount: $1,500.00\nDue Date: 2024-02-15\n\nServices:\n- Consulting: $1,200.00\n- Setup Fee: $300.00\n\nTotal: $1,500.00\n\nThank you for your business!"),
            ("inventory.csv", "Item Code,Item Name,Quantity,Unit Price,Total Value\nIT001,Laptop,50,$800,$40000\nIT002,Monitor,100,$200,$20000\nIT003,Keyboard,200,$50,$10000\nIT004,Mouse,200,$25,$5000"),
            ("contract.txt", "SERVICE AGREEMENT\n\nThis agreement is between AI ERP Company and Demo Client.\n\nScope of Work:\n1. ERP System Implementation\n2. Data Migration\n3. User Training\n4. 6 months support\n\nContract Value: $25,000\nStart Date: 2024-01-01\nEnd Date: 2024-06-30\n\nUrgent: Please review and approve by end of week.")
        ]
        
        processed_files = []
        
        for filename, content in sample_files:
            print(f"\nProcessing file: {filename}")
            
            # Process document
            file_data = content.encode('utf-8')
            doc_info, extracted_content = await self.document_processor.process_document(
                file_data=file_data,
                filename=filename,
                user_id=self.demo_user_id
            )
            
            print(f"✅ Document processed:")
            print(f"   Type: {doc_info.file_type.value}")
            print(f"   Size: {doc_info.size} bytes")
            print(f"   Status: {doc_info.status.value}")
            
            if extracted_content:
                print(f"   Text length: {len(extracted_content.text)} characters")
                if extracted_content.structured_data:
                    print(f"   Structured data: {len(extracted_content.structured_data)} items")
                
                # Analyze content with AI
                print("   Analyzing content with AI...")
                analysis = await self.content_analyzer.analyze_content(
                    content=extracted_content.text,
                    document_type=doc_info.file_type.value
                )
                
                print(f"   📊 Analysis Results:")
                print(f"      Category: {analysis.category.value}")
                print(f"      Confidence: {analysis.confidence:.2f}")
                print(f"      Urgency: {analysis.urgency_level}/5")
                print(f"      Sentiment: {analysis.sentiment}")
                
                if analysis.key_insights:
                    print("      Key Insights:")
                    for insight in analysis.key_insights[:2]:
                        print(f"      • {insight}")
                
                if analysis.recommendations:
                    print("      Recommendations:")
                    for rec in analysis.recommendations[:2]:
                        print(f"      • {rec}")
                
                processed_files.append((filename, file_data, analysis))
        
        # Upload to cloud storage
        print(f"\n☁️  Uploading files to cloud storage...")
        
        for filename, file_data, analysis in processed_files:
            success, storage_file, error = await self.storage_manager.upload_file(
                file_data=file_data,
                filename=filename,
                user_id=self.demo_user_id,
                team_id=self.demo_team_id,
                content_type="text/plain",
                metadata={
                    'category': analysis.category.value,
                    'urgency': str(analysis.urgency_level),
                    'analysis_timestamp': datetime.now().isoformat()
                }
            )
            
            if success:
                print(f"✅ Uploaded: {filename}")
                print(f"   File ID: {storage_file.id}")
                print(f"   Provider: {storage_file.provider.value}")
                print(f"   Access pattern: {storage_file.access_pattern.value}")
            else:
                print(f"❌ Upload failed: {error}")
        
        print("\n✅ File management demo completed!\n")
    
    async def _demo_ai_processing(self):
        """Demonstrate AI processing capabilities"""
        
        print("🤖 DEMO 3: AI Processing and Task Routing")
        print("=" * 50)
        
        # Sample user queries
        queries = [
            "Show me all pending invoices from this month",
            "Generate a sales report for Q1 2024", 
            "Check inventory levels for laptops",
            "Analyze the uploaded contract document",
            "Create a new customer record for ABC Corp"
        ]
        
        for query in queries:
            print(f"\nProcessing query: '{query}'")
            
            # Create and route task
            task, result = await self.task_router.process_user_request(
                user_input=query,
                user_id=self.demo_user_id,
                context={'team_id': self.demo_team_id}
            )
            
            print(f"✅ Task created:")
            print(f"   Type: {task.type.value}")
            print(f"   Priority: {task.priority.value}")
            print(f"   Confidence: {task.parameters.get('confidence', 0):.2f}")
            print(f"   Status: {task.status}")
            
            if task.parameters.get('entities'):
                entities = task.parameters['entities']
                if entities.get('numbers'):
                    print(f"   Detected numbers: {entities['numbers']}")
                if entities.get('dates'): 
                    print(f"   Detected dates: {entities['dates']}")
            
            print(f"   Result: {result.get('message', 'Task completed')}")
        
        # Store conversation context
        print(f"\n💭 Managing conversation context...")
        
        messages = []
        for query in queries[:3]:
            messages.append({
                'role': 'user',
                'content': query,
                'timestamp': datetime.now().isoformat()
            })
            messages.append({
                'role': 'assistant', 
                'content': f"I'll help you with: {query}",
                'timestamp': datetime.now().isoformat()
            })
        
        conversation_id = await self.context_manager.store_conversation(
            user_id=self.demo_user_id,
            messages=messages
        )
        
        print(f"✅ Stored conversation: {conversation_id}")
        print(f"   Messages: {len(messages)}")
        
        # Retrieve conversation
        retrieved_messages = await self.context_manager.get_conversation(
            conversation_id, self.demo_user_id
        )
        
        print(f"✅ Retrieved conversation with {len(retrieved_messages)} messages")
        
        print("\n✅ AI processing demo completed!\n")
    
    async def _demo_subscription_management(self):
        """Demonstrate subscription and billing management"""
        
        print("💳 DEMO 4: Subscription and Billing Management")
        print("=" * 50)
        
        # Get available plans
        print("Available billing plans:")
        plans = self.subscription_service.get_billing_plans()
        
        for plan in plans:
            print(f"\n📋 {plan.display_name} Plan:")
            print(f"   Price: ${plan.price_monthly}/month, ${plan.price_yearly}/year")
            print(f"   Tier: {plan.tier.value}")
            if plan.popular:
                print("   🌟 Most Popular!")
            
            # Show key limits
            team_limit = plan.usage_quotas.get('team_members', 'Unlimited')
            storage_limit = plan.usage_quotas.get('storage_gb', 'Unlimited')
            print(f"   Team members: {team_limit}")
            print(f"   Storage: {storage_limit}GB")
        
        # Create subscription
        print(f"\n🎫 Creating subscription for demo team...")
        
        success, subscription, error = await self.subscription_service.create_subscription(
            team_id=self.demo_team_id,
            plan_id="free",
            billing_period=BillingPeriod.MONTHLY,
            customer_info={
                'email': self.demo_user_email,
                'name': self.demo_user_name
            }
        )
        
        if success:
            print(f"✅ Subscription created:")
            print(f"   Plan: {subscription.tier.value}")
            print(f"   Status: {subscription.status.value}")
            print(f"   Amount: ${subscription.amount}/month")
            print(f"   Current period: {subscription.current_period_start.date()} - {subscription.current_period_end.date()}")
            
            # Track usage
            print(f"\n📊 Tracking usage...")
            
            # Simulate some usage
            usage_scenarios = [
                (UsageMetric.AI_QUERIES, 5, "User queries"),
                (UsageMetric.FILES_PROCESSED, 3, "File uploads"),
                (UsageMetric.REPORTS_GENERATED, 1, "Report generation"),
            ]
            
            for metric, amount, description in usage_scenarios:
                success, result = await self.subscription_service.track_usage(
                    team_id=self.demo_team_id,
                    metric=metric,
                    amount=amount,
                    metadata={'description': description}
                )
                
                if success:
                    quota = result.get('quota')
                    if quota:
                        print(f"✅ {description}: {quota.used}/{quota.limit} ({quota.usage_percentage:.1f}%)")
                    else:
                        print(f"✅ {description}: Tracked successfully")
                    
                    if result.get('warning'):
                        print(f"⚠️  Warning: {result['message']}")
                else:
                    print(f"❌ Usage tracking failed: {result.get('error')}")
            
            # Get usage analytics
            print(f"\n📈 Generating usage analytics...")
            
            analytics = await self.subscription_service.get_usage_analytics(
                team_id=self.demo_team_id,
                period_days=30
            )
            
            if 'error' not in analytics:
                print(f"✅ Usage Analytics:")
                print(f"   Plan: {analytics['plan']}")
                print(f"   Total records: {analytics['total_records']}")
                
                quota_status = analytics.get('quota_status', {})
                for metric, status in quota_status.items():
                    if status['used'] > 0:
                        print(f"   {metric}: {status['used']}/{status['limit']} ({status['percentage']:.1f}%)")
                
                insights = analytics.get('insights', [])
                if insights:
                    print("   Insights:")
                    for insight in insights:
                        print(f"   • {insight}")
            
        else:
            print(f"❌ Subscription creation failed: {error}")
        
        print("\n✅ Subscription management demo completed!\n")
    
    async def _demo_analytics_insights(self):
        """Demonstrate analytics and AI insights"""
        
        print("📊 DEMO 5: Analytics and AI Insights")
        print("=" * 50)
        
        # Storage analytics
        print("Getting storage analytics...")
        
        storage_analytics = await self.storage_manager.get_storage_analytics(
            user_id=self.demo_user_id,
            team_id=self.demo_team_id
        )
        
        print(f"✅ Storage Analytics:")
        print(f"   Total files: {storage_analytics.get('total_files', 0)}")
        print(f"   Total size: {storage_analytics.get('total_size_bytes', 0) / 1024:.1f} KB")
        
        by_content_type = storage_analytics.get('by_content_type', {})
        if by_content_type:
            print("   By content type:")
            for content_type, stats in by_content_type.items():
                print(f"     {content_type}: {stats['count']} files")
        
        recommendations = storage_analytics.get('recommendations', [])
        if recommendations:
            print("   AI Recommendations:")
            for rec in recommendations[:3]:
                print(f"   • {rec}")
        
        # Team suggestions
        print(f"\nGenerating team improvement suggestions...")
        
        suggestions = await self.team_service.suggest_team_improvements(
            team_id=self.demo_team_id,
            user_id=self.demo_user_id
        )
        
        if suggestions:
            print(f"✅ Team Improvement Suggestions:")
            for suggestion in suggestions:
                priority_icon = "🔴" if suggestion['priority'] == 'high' else "🟡" if suggestion['priority'] == 'medium' else "🟢"
                print(f"   {priority_icon} {suggestion['title']}")
                print(f"      {suggestion['description']}")
                print(f"      Action: {suggestion['action']}")
                print()
        
        # Context manager stats
        print("Getting context management statistics...")
        
        context_stats = await self.context_manager.get_context_stats()
        
        print(f"✅ Context Statistics:")
        print(f"   Total contexts: {context_stats.get('total_contexts', 0)}")
        
        by_type = context_stats.get('by_type', {})
        for context_type, count in by_type.items():
            if count > 0:
                print(f"   {context_type}: {count}")
        
        # Subscription stats
        print(f"\nGetting subscription statistics...")
        
        sub_stats = await self.subscription_service.get_subscription_stats()
        
        print(f"✅ Subscription Statistics:")
        print(f"   Total subscriptions: {sub_stats.get('total_subscriptions', 0)}")
        print(f"   Active subscriptions: {sub_stats.get('active_subscriptions', 0)}")
        print(f"   Monthly revenue: ${sub_stats.get('monthly_revenue', 0):.2f}")
        
        by_tier = sub_stats.get('by_tier', {})
        if by_tier:
            print("   By tier:")
            for tier, count in by_tier.items():
                print(f"     {tier}: {count}")
        
        print("\n✅ Analytics and insights demo completed!\n")
    
    # Helper methods
    
    async def _create_mock_llm_client(self):
        """Create a mock LLM client for demo purposes"""
        
        class MockLLMClient:
            """Mock LLM client that returns realistic responses"""
            
            async def generate_response(self, messages, **kwargs):
                # Mock response object
                class MockResponse:
                    def __init__(self, content):
                        self.content = content
                        self.tokens_used = 150
                        self.model = "mock-model"
                        self.cost_estimate = 0.001
                
                # Generate response based on input
                if isinstance(messages, str):
                    prompt = messages.lower()
                else:
                    prompt = str(messages).lower()
                
                if "role" in prompt or "suggest" in prompt:
                    return MockResponse("Based on the team structure and requirements, I recommend assigning the USER role for standard access to ERP modules.")
                
                elif "recommendation" in prompt or "improve" in prompt:
                    return MockResponse("1. Set up regular team meetings\n2. Implement automated workflows\n3. Review access permissions quarterly")
                
                elif "analyze" in prompt or "insight" in prompt:
                    return MockResponse("Key insights: This document shows strong financial performance with 15% revenue growth. Recommend focusing on customer retention strategies.")
                
                elif "storage" in prompt or "file" in prompt:
                    return MockResponse("1. Consider implementing automated file tiering\n2. Review access patterns for cost optimization\n3. Set up regular cleanup policies")
                
                else:
                    return MockResponse("I understand your request and I'm processing the information to provide the most helpful response.")
        
        return MockLLMClient()
    
    def _get_demo_storage_config(self):
        """Get demo storage configuration"""
        
        return {
            'default_provider': 'aws_s3',
            'aws': {
                'enabled': False,  # Disabled for demo
                'aws_access_key': 'demo_key',
                'aws_secret_key': 'demo_secret',
                'aws_region': 'us-east-1',
                'bucket_name': 'ai-erp-demo'
            },
            'quotas': {
                'total_limit_gb': 10,
            },
            'cost_optimization': True,
            'intelligent_routing': True
        }


async def main():
    """Main demo function"""
    
    print("🎬 AI ERP System - Complete Demo")
    print("=" * 60)
    print("This demo showcases the full AI-powered ERP system")
    print("including all major components and features.\n")
    
    try:
        # Create and initialize demo
        demo = AIERPDemo()
        await demo.initialize()
        
        # Run complete demo
        await demo.run_demo()
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n👋 Thank you for trying AI ERP!")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())