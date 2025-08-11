"""
Subscription and Billing Models for AI ERP System

Defines data structures for subscription management, usage tracking,
and billing operations with feature restrictions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import uuid


class SubscriptionTier(Enum):
    """Subscription tiers with different feature sets"""
    FREE = "free"
    BASIC = "basic" 
    PRO = "pro"
    ENTERPRISE = "enterprise"


class BillingPeriod(Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class SubscriptionStatus(Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    TRIALING = "trialing"
    PAUSED = "paused"


class UsageMetric(Enum):
    """Types of usage metrics to track"""
    TEAM_MEMBERS = "team_members"
    STORAGE_GB = "storage_gb"
    AI_QUERIES = "ai_queries"
    FILES_PROCESSED = "files_processed"
    REPORTS_GENERATED = "reports_generated"
    API_CALLS = "api_calls"
    WORKFLOW_EXECUTIONS = "workflow_executions"
    INTEGRATIONS = "integrations"


@dataclass
class FeatureLimit:
    """Feature limitation definition"""
    feature: str
    limit_type: str  # "count", "boolean", "storage", "rate"
    limit_value: Union[int, bool, str, float]
    soft_limit: Optional[Union[int, float]] = None  # Warning threshold
    description: str = ""


@dataclass
class UsageQuota:
    """Usage quota for a specific metric"""
    metric: UsageMetric
    limit: Union[int, float]
    used: Union[int, float] = 0
    period: str = "monthly"  # monthly, daily, total
    reset_date: Optional[datetime] = None
    
    @property
    def remaining(self) -> Union[int, float]:
        return max(0, self.limit - self.used)
    
    @property
    def usage_percentage(self) -> float:
        if self.limit == 0:
            return 0.0
        return min((self.used / self.limit) * 100, 100.0)
    
    @property
    def is_exceeded(self) -> bool:
        return self.used >= self.limit


@dataclass
class BillingPlan:
    """Billing plan definition"""
    id: str
    name: str
    tier: SubscriptionTier
    display_name: str
    description: str
    price_monthly: float
    price_yearly: float
    currency: str = "USD"
    
    # Feature limits
    feature_limits: List[FeatureLimit] = field(default_factory=list)
    usage_quotas: Dict[UsageMetric, int] = field(default_factory=dict)
    
    # Features included
    features: Dict[str, bool] = field(default_factory=dict)
    
    # Plan metadata
    popular: bool = False
    trial_days: int = 0
    setup_fee: float = 0.0
    
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Subscription:
    """User/Team subscription"""
    id: str
    team_id: str
    plan_id: str
    tier: SubscriptionTier
    status: SubscriptionStatus
    
    # Billing information
    billing_period: BillingPeriod
    amount: float
    currency: str = "USD"
    
    # Subscription lifecycle
    created_at: datetime
    current_period_start: datetime
    current_period_end: datetime
    trial_start: Optional[datetime] = None
    trial_end: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    
    # Usage tracking
    usage_quotas: Dict[UsageMetric, UsageQuota] = field(default_factory=dict)
    
    # Payment information
    payment_method_id: Optional[str] = None
    last_payment_date: Optional[datetime] = None
    next_payment_date: Optional[datetime] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is currently active"""
        return self.status == SubscriptionStatus.ACTIVE
    
    @property
    def is_trial(self) -> bool:
        """Check if subscription is in trial period"""
        return (self.status == SubscriptionStatus.TRIALING or
                (self.trial_start and self.trial_end and
                 self.trial_start <= datetime.now() <= self.trial_end))
    
    @property
    def days_until_renewal(self) -> int:
        """Days until next billing period"""
        if self.current_period_end:
            delta = self.current_period_end - datetime.now()
            return max(0, delta.days)
        return 0
    
    @property
    def is_past_due(self) -> bool:
        """Check if subscription is past due"""
        return self.status == SubscriptionStatus.PAST_DUE
    
    def get_quota(self, metric: UsageMetric) -> Optional[UsageQuota]:
        """Get usage quota for a specific metric"""
        return self.usage_quotas.get(metric)
    
    def update_usage(self, metric: UsageMetric, amount: Union[int, float]):
        """Update usage for a specific metric"""
        if metric in self.usage_quotas:
            self.usage_quotas[metric].used += amount
    
    def reset_usage(self, metric: UsageMetric):
        """Reset usage for a specific metric"""
        if metric in self.usage_quotas:
            self.usage_quotas[metric].used = 0
            self.usage_quotas[metric].reset_date = datetime.now()
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled for this subscription"""
        # This would check against the plan's feature limits
        # For now, return basic tier-based logic
        
        if self.tier == SubscriptionTier.FREE:
            free_features = [
                'basic_erp', 'basic_reports', 'file_upload',
                'basic_ai', 'team_collaboration'
            ]
            return feature in free_features
        
        elif self.tier == SubscriptionTier.BASIC:
            basic_features = [
                'basic_erp', 'advanced_reports', 'file_upload',
                'enhanced_ai', 'team_collaboration', 'integrations',
                'workflow_automation', 'custom_fields'
            ]
            return feature in basic_features
        
        elif self.tier in [SubscriptionTier.PRO, SubscriptionTier.ENTERPRISE]:
            # Pro and Enterprise have all features
            return True
        
        return False
    
    def check_usage_limit(self, metric: UsageMetric) -> Dict[str, Any]:
        """Check usage against limits"""
        quota = self.get_quota(metric)
        if not quota:
            return {'allowed': True, 'message': 'No quota defined'}
        
        if quota.is_exceeded:
            return {
                'allowed': False,
                'message': f'{metric.value} limit exceeded ({quota.used}/{quota.limit})',
                'quota': quota
            }
        
        # Check if approaching limit (90% threshold)
        if quota.usage_percentage >= 90:
            return {
                'allowed': True,
                'warning': True,
                'message': f'Approaching {metric.value} limit ({quota.used}/{quota.limit})',
                'quota': quota
            }
        
        return {
            'allowed': True,
            'quota': quota
        }


@dataclass
class UsageRecord:
    """Individual usage record for analytics"""
    id: str
    subscription_id: str
    team_id: str
    metric: UsageMetric
    amount: Union[int, float]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Invoice:
    """Billing invoice"""
    id: str
    subscription_id: str
    team_id: str
    
    # Invoice details
    amount_total: float
    amount_paid: float
    currency: str
    
    # Status and dates
    status: str  # draft, open, paid, void, uncollectible
    created_at: datetime
    due_date: datetime
    paid_at: Optional[datetime] = None
    
    # Line items
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    
    # Payment information
    payment_intent_id: Optional[str] = None
    payment_method: Optional[str] = None
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


def get_default_billing_plans() -> List[BillingPlan]:
    """Get default billing plans for AI ERP"""
    
    plans = []
    
    # FREE PLAN
    free_plan = BillingPlan(
        id="free",
        name="free",
        tier=SubscriptionTier.FREE,
        display_name="Free",
        description="Perfect for small teams getting started",
        price_monthly=0.0,
        price_yearly=0.0,
        features={
            'team_members': True,
            'basic_erp': True,
            'file_upload': True,
            'basic_ai': True,
            'basic_reports': True,
            'email_support': True,
        },
        usage_quotas={
            UsageMetric.TEAM_MEMBERS: 5,
            UsageMetric.STORAGE_GB: 5,
            UsageMetric.AI_QUERIES: 100,
            UsageMetric.FILES_PROCESSED: 50,
            UsageMetric.REPORTS_GENERATED: 10,
        }
    )
    
    free_plan.feature_limits = [
        FeatureLimit("team_members", "count", 5, 4, "Maximum team members"),
        FeatureLimit("storage", "storage", "5GB", None, "Storage limit"),
        FeatureLimit("ai_queries", "count", 100, 80, "AI queries per month"),
        FeatureLimit("advanced_features", "boolean", False, None, "Advanced features disabled"),
        FeatureLimit("priority_support", "boolean", False, None, "No priority support"),
    ]
    
    plans.append(free_plan)
    
    # BASIC PLAN  
    basic_plan = BillingPlan(
        id="basic",
        name="basic",
        tier=SubscriptionTier.BASIC,
        display_name="Basic",
        description="Enhanced features for growing teams",
        price_monthly=29.0,
        price_yearly=290.0,  # 2 months free
        trial_days=14,
        features={
            'team_members': True,
            'advanced_erp': True,
            'file_upload': True,
            'enhanced_ai': True,
            'advanced_reports': True,
            'integrations': True,
            'workflow_automation': True,
            'priority_email_support': True,
        },
        usage_quotas={
            UsageMetric.TEAM_MEMBERS: 25,
            UsageMetric.STORAGE_GB: 100,
            UsageMetric.AI_QUERIES: 1000,
            UsageMetric.FILES_PROCESSED: 500,
            UsageMetric.REPORTS_GENERATED: 50,
            UsageMetric.INTEGRATIONS: 5,
        }
    )
    
    basic_plan.feature_limits = [
        FeatureLimit("team_members", "count", 25, 20, "Maximum team members"),
        FeatureLimit("storage", "storage", "100GB", None, "Storage limit"),
        FeatureLimit("ai_queries", "count", 1000, 800, "AI queries per month"),
        FeatureLimit("integrations", "count", 5, 4, "Maximum integrations"),
        FeatureLimit("advanced_features", "boolean", True, None, "Advanced features enabled"),
    ]
    
    plans.append(basic_plan)
    
    # PRO PLAN
    pro_plan = BillingPlan(
        id="pro",
        name="pro",
        tier=SubscriptionTier.PRO,
        display_name="Pro",
        description="Full-featured plan for professional teams",
        price_monthly=99.0,
        price_yearly=990.0,  # 2 months free
        trial_days=14,
        popular=True,
        features={
            'unlimited_members': True,
            'full_erp_suite': True,
            'unlimited_storage': True,
            'advanced_ai': True,
            'custom_reports': True,
            'unlimited_integrations': True,
            'advanced_workflows': True,
            'phone_support': True,
            'custom_branding': True,
            'api_access': True,
        },
        usage_quotas={
            UsageMetric.TEAM_MEMBERS: 999999,  # Unlimited
            UsageMetric.STORAGE_GB: 1000,
            UsageMetric.AI_QUERIES: 10000,
            UsageMetric.FILES_PROCESSED: 5000,
            UsageMetric.REPORTS_GENERATED: 500,
            UsageMetric.INTEGRATIONS: 999999,  # Unlimited
        }
    )
    
    pro_plan.feature_limits = [
        FeatureLimit("team_members", "count", 999999, None, "Unlimited team members"),
        FeatureLimit("storage", "storage", "1TB", None, "Storage limit"),
        FeatureLimit("ai_queries", "count", 10000, 8000, "AI queries per month"),
        FeatureLimit("all_features", "boolean", True, None, "All features enabled"),
    ]
    
    plans.append(pro_plan)
    
    # ENTERPRISE PLAN
    enterprise_plan = BillingPlan(
        id="enterprise",
        name="enterprise",
        tier=SubscriptionTier.ENTERPRISE,
        display_name="Enterprise",
        description="Custom solutions for large organizations",
        price_monthly=299.0,
        price_yearly=2990.0,
        trial_days=30,
        features={
            'everything_in_pro': True,
            'dedicated_support': True,
            'sso_integration': True,
            'advanced_security': True,
            'custom_development': True,
            'on_premise_option': True,
            'compliance_tools': True,
            'dedicated_account_manager': True,
        },
        usage_quotas={
            UsageMetric.TEAM_MEMBERS: 999999,
            UsageMetric.STORAGE_GB: 999999,  # Unlimited
            UsageMetric.AI_QUERIES: 50000,
            UsageMetric.FILES_PROCESSED: 999999,
            UsageMetric.REPORTS_GENERATED: 999999,
            UsageMetric.INTEGRATIONS: 999999,
        }
    )
    
    enterprise_plan.feature_limits = [
        FeatureLimit("everything", "boolean", True, None, "All features unlimited"),
        FeatureLimit("custom_limits", "boolean", True, None, "Custom limits available"),
        FeatureLimit("dedicated_support", "boolean", True, None, "Dedicated support included"),
    ]
    
    plans.append(enterprise_plan)
    
    return plans


def create_subscription_from_plan(
    team_id: str,
    plan: BillingPlan,
    billing_period: BillingPeriod = BillingPeriod.MONTHLY
) -> Subscription:
    """Create subscription instance from billing plan"""
    
    now = datetime.now()
    
    # Calculate period dates
    if billing_period == BillingPeriod.MONTHLY:
        period_end = now + timedelta(days=30)
        amount = plan.price_monthly
    elif billing_period == BillingPeriod.YEARLY:
        period_end = now + timedelta(days=365)
        amount = plan.price_yearly
    else:  # LIFETIME
        period_end = now + timedelta(days=36500)  # 100 years
        amount = plan.price_yearly * 10  # Lifetime = 10x yearly
    
    # Create usage quotas from plan
    usage_quotas = {}
    for metric, limit in plan.usage_quotas.items():
        usage_quotas[metric] = UsageQuota(
            metric=metric,
            limit=limit,
            used=0,
            period="monthly",
            reset_date=now
        )
    
    # Determine initial status
    initial_status = SubscriptionStatus.ACTIVE
    trial_start = None
    trial_end = None
    
    if plan.trial_days > 0 and amount > 0:  # Free plans don't have trials
        initial_status = SubscriptionStatus.TRIALING
        trial_start = now
        trial_end = now + timedelta(days=plan.trial_days)
        period_end = trial_end
    
    subscription = Subscription(
        id=str(uuid.uuid4()),
        team_id=team_id,
        plan_id=plan.id,
        tier=plan.tier,
        status=initial_status,
        billing_period=billing_period,
        amount=amount,
        currency=plan.currency,
        created_at=now,
        current_period_start=now,
        current_period_end=period_end,
        trial_start=trial_start,
        trial_end=trial_end,
        usage_quotas=usage_quotas,
        metadata={
            'plan_name': plan.name,
            'plan_display_name': plan.display_name
        }
    )
    
    return subscription


class SubscriptionManager:
    """Helper class for subscription operations"""
    
    def __init__(self):
        self.plans = {plan.id: plan for plan in get_default_billing_plans()}
    
    def get_plan(self, plan_id: str) -> Optional[BillingPlan]:
        """Get billing plan by ID"""
        return self.plans.get(plan_id)
    
    def get_plans_by_tier(self, tier: SubscriptionTier) -> List[BillingPlan]:
        """Get all plans for a specific tier"""
        return [plan for plan in self.plans.values() if plan.tier == tier]
    
    def calculate_upgrade_cost(
        self,
        current_subscription: Subscription,
        target_plan: BillingPlan,
        prorate: bool = True
    ) -> Dict[str, Any]:
        """Calculate cost for subscription upgrade"""
        
        current_plan = self.get_plan(current_subscription.plan_id)
        if not current_plan:
            return {'error': 'Current plan not found'}
        
        # Calculate target cost
        target_amount = (target_plan.price_monthly if 
                        current_subscription.billing_period == BillingPeriod.MONTHLY
                        else target_plan.price_yearly)
        
        current_amount = current_subscription.amount
        
        # Calculate proration if enabled
        upgrade_cost = target_amount - current_amount
        
        if prorate and current_subscription.billing_period == BillingPeriod.MONTHLY:
            days_remaining = current_subscription.days_until_renewal
            days_in_period = 30
            proration_factor = days_remaining / days_in_period
            upgrade_cost = upgrade_cost * proration_factor
        
        return {
            'current_plan': current_plan.display_name,
            'target_plan': target_plan.display_name,
            'current_amount': current_amount,
            'target_amount': target_amount,
            'upgrade_cost': max(0, upgrade_cost),
            'effective_date': datetime.now(),
            'proration_applied': prorate
        }
    
    def get_feature_comparison(self) -> Dict[str, Any]:
        """Get feature comparison across all plans"""
        
        comparison = {
            'plans': [],
            'features': []
        }
        
        all_features = set()
        
        # Collect all features
        for plan in self.plans.values():
            all_features.update(plan.features.keys())
        
        # Build comparison matrix
        for plan in sorted(self.plans.values(), key=lambda p: p.price_monthly):
            plan_data = {
                'id': plan.id,
                'name': plan.display_name,
                'price_monthly': plan.price_monthly,
                'price_yearly': plan.price_yearly,
                'popular': plan.popular,
                'trial_days': plan.trial_days,
                'features': {}
            }
            
            for feature in all_features:
                plan_data['features'][feature] = plan.features.get(feature, False)
            
            comparison['plans'].append(plan_data)
        
        comparison['features'] = sorted(list(all_features))
        
        return comparison