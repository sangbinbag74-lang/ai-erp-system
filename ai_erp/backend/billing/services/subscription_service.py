"""
Subscription Service for AI ERP System

Manages subscription lifecycle, billing operations, usage tracking,
and feature access control with payment gateway integration.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import json

from ..models.subscription_models import (
    Subscription, BillingPlan, SubscriptionTier, SubscriptionStatus,
    BillingPeriod, UsageMetric, UsageQuota, UsageRecord, Invoice,
    get_default_billing_plans, create_subscription_from_plan, SubscriptionManager
)

logger = logging.getLogger(__name__)


class PaymentGateway:
    """Payment gateway abstraction (Stripe, etc.)"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get('provider', 'stripe')
        
    async def create_customer(self, email: str, name: str, metadata: Dict = None) -> Dict[str, Any]:
        """Create customer in payment gateway"""
        # Mock implementation - would integrate with actual payment provider
        return {
            'id': f'cust_{email.replace("@", "_")}',
            'email': email,
            'name': name
        }
    
    async def create_subscription(
        self, 
        customer_id: str, 
        price_id: str,
        trial_days: int = 0
    ) -> Dict[str, Any]:
        """Create subscription in payment gateway"""
        # Mock implementation
        return {
            'id': f'sub_{customer_id}_{price_id}',
            'status': 'trialing' if trial_days > 0 else 'active',
            'current_period_start': datetime.now().timestamp(),
            'current_period_end': (datetime.now() + timedelta(days=30)).timestamp(),
            'trial_end': (datetime.now() + timedelta(days=trial_days)).timestamp() if trial_days > 0 else None
        }
    
    async def update_subscription(
        self,
        subscription_id: str,
        price_id: str = None,
        prorate: bool = True
    ) -> Dict[str, Any]:
        """Update subscription in payment gateway"""
        # Mock implementation
        return {
            'id': subscription_id,
            'status': 'active',
            'updated': True
        }
    
    async def cancel_subscription(
        self,
        subscription_id: str,
        at_period_end: bool = True
    ) -> Dict[str, Any]:
        """Cancel subscription in payment gateway"""
        # Mock implementation
        return {
            'id': subscription_id,
            'status': 'canceled' if not at_period_end else 'active',
            'canceled_at': datetime.now().timestamp(),
            'cancel_at_period_end': at_period_end
        }
    
    async def create_invoice(
        self,
        customer_id: str,
        amount: float,
        description: str
    ) -> Dict[str, Any]:
        """Create one-time invoice"""
        # Mock implementation
        return {
            'id': f'inv_{customer_id}_{int(datetime.now().timestamp())}',
            'amount_total': amount,
            'status': 'open',
            'hosted_invoice_url': f'https://invoice.stripe.com/fake-url'
        }


class SubscriptionService:
    """
    Service for managing subscriptions and billing operations
    """
    
    def __init__(self, payment_gateway: PaymentGateway = None, config: Dict[str, Any] = None):
        self.config = config or {}
        self.payment_gateway = payment_gateway
        
        # Initialize subscription manager
        self.subscription_manager = SubscriptionManager()
        
        # Storage (in production, this would be a database)
        self._subscriptions = {}
        self._usage_records = []
        self._invoices = {}
        
        # Configuration
        self.grace_period_days = self.config.get('grace_period_days', 3)
        self.usage_tracking_enabled = self.config.get('usage_tracking_enabled', True)
        
    async def create_subscription(
        self,
        team_id: str,
        plan_id: str,
        billing_period: BillingPeriod = BillingPeriod.MONTHLY,
        customer_info: Dict[str, str] = None,
        payment_method_id: str = None
    ) -> Tuple[bool, Optional[Subscription], Optional[str]]:
        """
        Create new subscription for team
        """
        
        try:
            # Get billing plan
            plan = self.subscription_manager.get_plan(plan_id)
            if not plan:
                return False, None, "Billing plan not found"
            
            # Check if team already has subscription
            existing = await self._get_team_subscription(team_id)
            if existing and existing.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]:
                return False, None, "Team already has active subscription"
            
            # Create subscription instance
            subscription = create_subscription_from_plan(team_id, plan, billing_period)
            
            # Create customer in payment gateway if needed
            if self.payment_gateway and plan.price_monthly > 0:
                try:
                    customer_data = await self.payment_gateway.create_customer(
                        email=customer_info.get('email', ''),
                        name=customer_info.get('name', ''),
                        metadata={'team_id': team_id}
                    )
                    
                    # Create payment subscription
                    payment_subscription = await self.payment_gateway.create_subscription(
                        customer_id=customer_data['id'],
                        price_id=f"{plan.id}_{billing_period.value}",
                        trial_days=plan.trial_days
                    )
                    
                    # Update subscription with payment info
                    subscription.payment_method_id = payment_method_id
                    subscription.metadata['payment_customer_id'] = customer_data['id']
                    subscription.metadata['payment_subscription_id'] = payment_subscription['id']
                    
                except Exception as e:
                    logger.error(f"Payment gateway error: {str(e)}")
                    # For free plans, continue without payment setup
                    if plan.price_monthly > 0:
                        return False, None, f"Payment setup failed: {str(e)}"
            
            # Store subscription
            await self._store_subscription(subscription)
            
            logger.info(f"Created subscription {subscription.id} for team {team_id}")
            return True, subscription, None
            
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            return False, None, str(e)
    
    async def upgrade_subscription(
        self,
        team_id: str,
        target_plan_id: str,
        prorate: bool = True
    ) -> Tuple[bool, Optional[Subscription], Optional[str]]:
        """
        Upgrade subscription to higher tier
        """
        
        try:
            # Get current subscription
            current_subscription = await self._get_team_subscription(team_id)
            if not current_subscription:
                return False, None, "No active subscription found"
            
            # Get target plan
            target_plan = self.subscription_manager.get_plan(target_plan_id)
            if not target_plan:
                return False, None, "Target plan not found"
            
            # Validate upgrade path
            current_plan = self.subscription_manager.get_plan(current_subscription.plan_id)
            if not self._is_valid_upgrade(current_plan, target_plan):
                return False, None, "Invalid upgrade path"
            
            # Calculate upgrade cost
            cost_calculation = self.subscription_manager.calculate_upgrade_cost(
                current_subscription, target_plan, prorate
            )
            
            # Update subscription
            current_subscription.plan_id = target_plan.id
            current_subscription.tier = target_plan.tier
            current_subscription.amount = (target_plan.price_monthly if 
                                         current_subscription.billing_period == BillingPeriod.MONTHLY
                                         else target_plan.price_yearly)
            
            # Update usage quotas
            current_subscription.usage_quotas = {}
            for metric, limit in target_plan.usage_quotas.items():
                current_subscription.usage_quotas[metric] = UsageQuota(
                    metric=metric,
                    limit=limit,
                    used=0,  # Reset usage on upgrade
                    period="monthly",
                    reset_date=datetime.now()
                )
            
            # Update payment gateway
            if self.payment_gateway and cost_calculation['upgrade_cost'] > 0:
                try:
                    payment_subscription_id = current_subscription.metadata.get('payment_subscription_id')
                    if payment_subscription_id:
                        await self.payment_gateway.update_subscription(
                            subscription_id=payment_subscription_id,
                            price_id=f"{target_plan.id}_{current_subscription.billing_period.value}",
                            prorate=prorate
                        )
                except Exception as e:
                    logger.error(f"Payment gateway update error: {str(e)}")
                    return False, None, f"Payment update failed: {str(e)}"
            
            # Store updated subscription
            await self._store_subscription(current_subscription)
            
            logger.info(f"Upgraded subscription {current_subscription.id} to {target_plan.display_name}")
            return True, current_subscription, None
            
        except Exception as e:
            logger.error(f"Error upgrading subscription: {str(e)}")
            return False, None, str(e)
    
    async def cancel_subscription(
        self,
        team_id: str,
        at_period_end: bool = True,
        reason: str = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Cancel subscription
        """
        
        try:
            # Get subscription
            subscription = await self._get_team_subscription(team_id)
            if not subscription:
                return False, "No active subscription found"
            
            # Update subscription status
            if at_period_end:
                subscription.status = SubscriptionStatus.ACTIVE  # Keep active until period end
                subscription.metadata['cancel_at_period_end'] = True
                subscription.metadata['cancellation_reason'] = reason
            else:
                subscription.status = SubscriptionStatus.CANCELED
                subscription.canceled_at = datetime.now()
                subscription.ended_at = datetime.now()
            
            # Cancel in payment gateway
            if self.payment_gateway:
                try:
                    payment_subscription_id = subscription.metadata.get('payment_subscription_id')
                    if payment_subscription_id:
                        await self.payment_gateway.cancel_subscription(
                            subscription_id=payment_subscription_id,
                            at_period_end=at_period_end
                        )
                except Exception as e:
                    logger.warning(f"Payment gateway cancellation warning: {str(e)}")
            
            # Store updated subscription
            await self._store_subscription(subscription)
            
            logger.info(f"Canceled subscription {subscription.id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error canceling subscription: {str(e)}")
            return False, str(e)
    
    async def track_usage(
        self,
        team_id: str,
        metric: UsageMetric,
        amount: Union[int, float] = 1,
        metadata: Dict[str, Any] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Track usage and enforce limits
        """
        
        if not self.usage_tracking_enabled:
            return True, {'message': 'Usage tracking disabled'}
        
        try:
            # Get subscription
            subscription = await self._get_team_subscription(team_id)
            if not subscription:
                return False, {'error': 'No subscription found'}
            
            # Check current usage against limits
            usage_check = subscription.check_usage_limit(metric)
            
            # If limit would be exceeded, deny the action
            if not usage_check['allowed']:
                return False, usage_check
            
            # Update usage
            subscription.update_usage(metric, amount)
            
            # Create usage record
            usage_record = UsageRecord(
                id=f"{team_id}_{metric.value}_{int(datetime.now().timestamp())}",
                subscription_id=subscription.id,
                team_id=team_id,
                metric=metric,
                amount=amount,
                timestamp=datetime.now(),
                metadata=metadata or {}
            )
            
            # Store usage record
            self._usage_records.append(usage_record)
            
            # Store updated subscription
            await self._store_subscription(subscription)
            
            # Re-check usage after update for warnings
            final_check = subscription.check_usage_limit(metric)
            
            return True, final_check
            
        except Exception as e:
            logger.error(f"Error tracking usage: {str(e)}")
            return False, {'error': str(e)}
    
    async def get_usage_analytics(
        self,
        team_id: str,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Get comprehensive usage analytics
        """
        
        try:
            subscription = await self._get_team_subscription(team_id)
            if not subscription:
                return {'error': 'No subscription found'}
            
            # Get usage records for period
            cutoff_date = datetime.now() - timedelta(days=period_days)
            period_records = [
                record for record in self._usage_records
                if record.team_id == team_id and record.timestamp >= cutoff_date
            ]
            
            # Aggregate usage by metric
            usage_by_metric = {}
            for record in period_records:
                metric = record.metric.value
                if metric not in usage_by_metric:
                    usage_by_metric[metric] = {
                        'total': 0,
                        'records': [],
                        'daily_breakdown': {}
                    }
                
                usage_by_metric[metric]['total'] += record.amount
                usage_by_metric[metric]['records'].append({
                    'amount': record.amount,
                    'timestamp': record.timestamp.isoformat(),
                    'metadata': record.metadata
                })
                
                # Daily breakdown
                day_key = record.timestamp.strftime('%Y-%m-%d')
                if day_key not in usage_by_metric[metric]['daily_breakdown']:
                    usage_by_metric[metric]['daily_breakdown'][day_key] = 0
                usage_by_metric[metric]['daily_breakdown'][day_key] += record.amount
            
            # Current quota status
            quota_status = {}
            for metric, quota in subscription.usage_quotas.items():
                quota_status[metric.value] = {
                    'limit': quota.limit,
                    'used': quota.used,
                    'remaining': quota.remaining,
                    'percentage': quota.usage_percentage,
                    'is_exceeded': quota.is_exceeded
                }
            
            # Generate insights
            insights = []
            for metric, quota in subscription.usage_quotas.items():
                if quota.usage_percentage > 80:
                    insights.append(f"High usage detected for {metric.value}: {quota.usage_percentage:.1f}%")
                
                if quota.is_exceeded:
                    insights.append(f"Quota exceeded for {metric.value}: {quota.used}/{quota.limit}")
            
            return {
                'subscription_id': subscription.id,
                'plan': subscription.tier.value,
                'period_days': period_days,
                'total_records': len(period_records),
                'usage_by_metric': usage_by_metric,
                'quota_status': quota_status,
                'insights': insights,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting usage analytics: {str(e)}")
            return {'error': str(e)}
    
    async def process_subscription_renewal(self, subscription_id: str) -> Tuple[bool, Optional[str]]:
        """
        Process subscription renewal (called by scheduler)
        """
        
        try:
            subscription = self._subscriptions.get(subscription_id)
            if not subscription:
                return False, "Subscription not found"
            
            # Check if renewal is due
            if datetime.now() < subscription.current_period_end:
                return False, "Renewal not due yet"
            
            # Reset usage quotas
            for metric, quota in subscription.usage_quotas.items():
                quota.used = 0
                quota.reset_date = datetime.now()
            
            # Update period dates
            if subscription.billing_period == BillingPeriod.MONTHLY:
                subscription.current_period_start = subscription.current_period_end
                subscription.current_period_end = subscription.current_period_end + timedelta(days=30)
            elif subscription.billing_period == BillingPeriod.YEARLY:
                subscription.current_period_start = subscription.current_period_end
                subscription.current_period_end = subscription.current_period_end + timedelta(days=365)
            
            # Update next payment date
            subscription.next_payment_date = subscription.current_period_end
            subscription.last_payment_date = datetime.now()
            
            # Store updated subscription
            await self._store_subscription(subscription)
            
            logger.info(f"Processed renewal for subscription {subscription_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Error processing renewal: {str(e)}")
            return False, str(e)
    
    async def get_subscription_by_team(self, team_id: str) -> Optional[Subscription]:
        """Get active subscription for team"""
        return await self._get_team_subscription(team_id)
    
    async def check_feature_access(
        self,
        team_id: str,
        feature: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if team has access to specific feature
        """
        
        try:
            subscription = await self._get_team_subscription(team_id)
            if not subscription:
                return False, "No subscription found"
            
            # Check if subscription is active
            if not subscription.is_active and not subscription.is_trial:
                return False, "Subscription not active"
            
            # Check feature access
            has_access = subscription.is_feature_enabled(feature)
            
            if not has_access:
                # Get available plans that include this feature
                available_plans = []
                for plan in self.subscription_manager.plans.values():
                    if feature in plan.features and plan.features[feature]:
                        available_plans.append(plan.display_name)
                
                suggestion = ""
                if available_plans:
                    suggestion = f" Available in: {', '.join(available_plans)}"
                
                return False, f"Feature '{feature}' not available in current plan{suggestion}"
            
            return True, None
            
        except Exception as e:
            logger.error(f"Error checking feature access: {str(e)}")
            return False, str(e)
    
    def get_billing_plans(self) -> List[BillingPlan]:
        """Get all available billing plans"""
        return list(self.subscription_manager.plans.values())
    
    def get_plan_comparison(self) -> Dict[str, Any]:
        """Get feature comparison across plans"""
        return self.subscription_manager.get_feature_comparison()
    
    # Helper methods
    
    async def _get_team_subscription(self, team_id: str) -> Optional[Subscription]:
        """Get active subscription for team"""
        for subscription in self._subscriptions.values():
            if (subscription.team_id == team_id and 
                subscription.status in [SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIALING]):
                return subscription
        return None
    
    async def _store_subscription(self, subscription: Subscription):
        """Store subscription"""
        self._subscriptions[subscription.id] = subscription
    
    def _is_valid_upgrade(self, current_plan: BillingPlan, target_plan: BillingPlan) -> bool:
        """Check if upgrade path is valid"""
        
        tier_hierarchy = {
            SubscriptionTier.FREE: 0,
            SubscriptionTier.BASIC: 1,
            SubscriptionTier.PRO: 2,
            SubscriptionTier.ENTERPRISE: 3
        }
        
        current_level = tier_hierarchy.get(current_plan.tier, 0)
        target_level = tier_hierarchy.get(target_plan.tier, 0)
        
        return target_level > current_level
    
    async def get_subscription_stats(self) -> Dict[str, Any]:
        """Get overall subscription statistics"""
        
        stats = {
            'total_subscriptions': len(self._subscriptions),
            'active_subscriptions': 0,
            'trial_subscriptions': 0,
            'by_tier': {},
            'monthly_revenue': 0.0,
            'total_usage_records': len(self._usage_records)
        }
        
        for subscription in self._subscriptions.values():
            if subscription.is_active:
                stats['active_subscriptions'] += 1
            if subscription.is_trial:
                stats['trial_subscriptions'] += 1
            
            # Tier breakdown
            tier = subscription.tier.value
            if tier not in stats['by_tier']:
                stats['by_tier'][tier] = 0
            stats['by_tier'][tier] += 1
            
            # Revenue calculation
            if subscription.is_active and subscription.billing_period == BillingPeriod.MONTHLY:
                stats['monthly_revenue'] += subscription.amount
            elif subscription.is_active and subscription.billing_period == BillingPeriod.YEARLY:
                stats['monthly_revenue'] += subscription.amount / 12
        
        return stats


def create_subscription_service(payment_gateway_config: Dict = None, **config) -> SubscriptionService:
    """Factory function to create subscription service"""
    
    payment_gateway = None
    if payment_gateway_config:
        payment_gateway = PaymentGateway(payment_gateway_config)
    
    return SubscriptionService(payment_gateway=payment_gateway, config=config)