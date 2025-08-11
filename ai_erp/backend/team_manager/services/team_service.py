"""
Team Service for AI ERP System

Business logic for team management, AI-powered role assignment,
and intelligent collaboration features.
"""

import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import secrets
import hashlib

from ..models.team_models import (
    Team, TeamMember, Invitation, UserRole, TeamStatus, 
    InvitationStatus, SubscriptionTier, TeamAnalytics,
    get_default_roles, create_default_team_settings
)

logger = logging.getLogger(__name__)


class TeamService:
    """
    Service layer for team management operations
    """
    
    def __init__(self, llm_client=None, email_service=None, storage=None, config: Dict[str, Any] = None):
        self.llm_client = llm_client
        self.email_service = email_service
        self.storage = storage  # Database/storage abstraction
        self.config = config or {}
        
        # Configuration
        self.invitation_expiry_days = self.config.get('invitation_expiry_days', 7)
        self.max_invitation_attempts = self.config.get('max_invitation_attempts', 3)
        self.ai_role_assignment = self.config.get('ai_role_assignment', True)
        
        # In-memory cache for demo (replace with Redis in production)
        self._teams_cache = {}
        self._invitations_cache = {}
    
    async def create_team(
        self, 
        name: str, 
        owner_id: str, 
        owner_email: str,
        owner_name: str,
        description: str = None,
        subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    ) -> Tuple[Team, TeamMember]:
        """
        Create new team with owner
        """
        
        try:
            # Validate team name
            if not name or len(name.strip()) < 2:
                raise ValueError("Team name must be at least 2 characters")
            
            # Create team
            team = Team(
                id=self._generate_id(),
                name=name.strip(),
                description=description,
                owner_id=owner_id,
                subscription_tier=subscription_tier,
                settings=create_default_team_settings()
            )
            
            # Create owner member
            owner_member = TeamMember(
                id=self._generate_id(),
                user_id=owner_id,
                team_id=team.id,
                email=owner_email,
                name=owner_name,
                role=UserRole.OWNER
            )
            
            # Add owner to team
            team.add_member(owner_member)
            
            # Store team
            await self._store_team(team)
            
            # Generate welcome insights using AI if available
            if self.llm_client:
                try:
                    await self._generate_team_setup_recommendations(team)
                except Exception as e:
                    logger.warning(f"Failed to generate setup recommendations: {str(e)}")
            
            logger.info(f"Created team '{name}' with owner {owner_email}")
            return team, owner_member
            
        except Exception as e:
            logger.error(f"Error creating team: {str(e)}")
            raise
    
    async def invite_member(
        self, 
        team_id: str, 
        email: str, 
        invited_by: str,
        role: UserRole = None,
        message: str = None
    ) -> Invitation:
        """
        Invite new member to team with AI-powered role suggestion
        """
        
        try:
            team = await self._get_team(team_id)
            if not team:
                raise ValueError("Team not found")
            
            # Check permissions
            if not team.has_permission(invited_by, "team", "invite"):
                raise PermissionError("User does not have permission to invite members")
            
            # Check if team can add more members
            if not team.can_add_members:
                raise ValueError(f"Team has reached member limit ({team.member_limit})")
            
            # Check if user is already a member
            existing_member = team.get_member_by_email(email)
            if existing_member:
                raise ValueError("User is already a team member")
            
            # Check for existing pending invitation
            existing_invitation = next(
                (inv for inv in team.pending_invitations 
                 if inv.email.lower() == email.lower() and inv.status == InvitationStatus.PENDING),
                None
            )
            
            if existing_invitation:
                # Update existing invitation
                existing_invitation.invited_by = invited_by
                existing_invitation.message = message
                existing_invitation.created_at = datetime.now()
                existing_invitation.expires_at = datetime.now() + timedelta(days=self.invitation_expiry_days)
                existing_invitation.token = self._generate_invitation_token()
                
                invitation = existing_invitation
            else:
                # Suggest role using AI if not provided
                if not role:
                    role = await self._suggest_member_role(team, email, message)
                
                # Create new invitation
                invitation = team.create_invitation(email, role, invited_by, message)
            
            # Store updated team
            await self._store_team(team)
            
            # Send invitation email
            if self.email_service:
                try:
                    await self._send_invitation_email(team, invitation)
                except Exception as e:
                    logger.warning(f"Failed to send invitation email: {str(e)}")
            
            logger.info(f"Created invitation for {email} to team {team.name}")
            return invitation
            
        except Exception as e:
            logger.error(f"Error creating invitation: {str(e)}")
            raise
    
    async def accept_invitation(
        self, 
        token: str, 
        user_id: str, 
        user_name: str,
        user_email: str
    ) -> Tuple[Team, TeamMember]:
        """
        Accept team invitation
        """
        
        try:
            # Find team with this invitation token
            team = await self._find_team_by_invitation(token)
            if not team:
                raise ValueError("Invalid invitation token")
            
            invitation = team.get_invitation(token)
            if not invitation:
                raise ValueError("Invitation not found")
            
            # Validate invitation
            if invitation.status != InvitationStatus.PENDING:
                raise ValueError("Invitation is no longer valid")
            
            if invitation.expires_at < datetime.now():
                invitation.status = InvitationStatus.EXPIRED
                await self._store_team(team)
                raise ValueError("Invitation has expired")
            
            # Check email match
            if invitation.email.lower() != user_email.lower():
                raise ValueError("Email address does not match invitation")
            
            # Accept invitation and create member
            member = team.accept_invitation(token, user_id, user_name)
            if not member:
                raise ValueError("Failed to accept invitation")
            
            # Store updated team
            await self._store_team(team)
            
            # Generate onboarding recommendations
            if self.llm_client:
                try:
                    await self._generate_onboarding_recommendations(team, member)
                except Exception as e:
                    logger.warning(f"Failed to generate onboarding recommendations: {str(e)}")
            
            logger.info(f"User {user_name} joined team {team.name}")
            return team, member
            
        except Exception as e:
            logger.error(f"Error accepting invitation: {str(e)}")
            raise
    
    async def update_member_role(
        self, 
        team_id: str, 
        member_user_id: str, 
        new_role: UserRole,
        updated_by: str
    ) -> bool:
        """
        Update team member role with validation
        """
        
        try:
            team = await self._get_team(team_id)
            if not team:
                raise ValueError("Team not found")
            
            # Check permissions
            if not team.has_permission(updated_by, "team", "manage"):
                raise PermissionError("User does not have permission to manage team members")
            
            # Cannot demote the owner
            member = team.get_member(member_user_id)
            if member and member.role == UserRole.OWNER:
                raise ValueError("Cannot change owner role")
            
            # Update role
            success = team.update_member_role(member_user_id, new_role)
            
            if success:
                await self._store_team(team)
                logger.info(f"Updated member {member_user_id} role to {new_role.value}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating member role: {str(e)}")
            raise
    
    async def remove_member(
        self, 
        team_id: str, 
        member_user_id: str,
        removed_by: str
    ) -> bool:
        """
        Remove team member
        """
        
        try:
            team = await self._get_team(team_id)
            if not team:
                raise ValueError("Team not found")
            
            # Check permissions
            if not team.has_permission(removed_by, "team", "manage"):
                raise PermissionError("User does not have permission to remove team members")
            
            # Cannot remove owner
            member = team.get_member(member_user_id)
            if member and member.role == UserRole.OWNER:
                raise ValueError("Cannot remove team owner")
            
            # Remove member
            success = team.remove_member(member_user_id)
            
            if success:
                await self._store_team(team)
                logger.info(f"Removed member {member_user_id} from team {team.name}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error removing member: {str(e)}")
            raise
    
    async def get_team_analytics(
        self, 
        team_id: str, 
        user_id: str,
        days: int = 30
    ) -> Optional[TeamAnalytics]:
        """
        Generate team analytics and insights
        """
        
        try:
            team = await self._get_team(team_id)
            if not team:
                return None
            
            # Check permissions
            if not team.has_permission(user_id, "reports", "read"):
                raise PermissionError("User does not have permission to view analytics")
            
            period_end = datetime.now()
            period_start = period_end - timedelta(days=days)
            
            # Generate analytics (in production, this would query actual usage data)
            analytics = TeamAnalytics(
                team_id=team_id,
                period_start=period_start,
                period_end=period_end,
                active_members=len([m for m in team.members if m.status == "active"]),
                total_logins=sum([self._mock_login_count(m) for m in team.members]),
                avg_session_duration=self._mock_avg_session_duration(team),
                documents_processed=self._mock_documents_processed(team, days),
                ai_queries=self._mock_ai_queries(team, days),
                reports_generated=self._mock_reports_generated(team, days),
                shared_files=self._mock_shared_files(team, days),
                team_discussions=self._mock_team_discussions(team, days),
                approval_workflows=self._mock_approval_workflows(team, days),
                productivity_score=self._calculate_productivity_score(team),
                collaboration_rating=self._calculate_collaboration_rating(team)
            )
            
            # Generate AI recommendations
            if self.llm_client:
                try:
                    recommendations = await self._generate_team_recommendations(team, analytics)
                    analytics.recommendations = recommendations
                except Exception as e:
                    logger.warning(f"Failed to generate recommendations: {str(e)}")
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating team analytics: {str(e)}")
            return None
    
    async def suggest_team_improvements(
        self, 
        team_id: str, 
        user_id: str
    ) -> List[Dict[str, Any]]:
        """
        AI-powered team improvement suggestions
        """
        
        try:
            team = await self._get_team(team_id)
            if not team:
                return []
            
            # Check permissions
            if not team.has_permission(user_id, "team", "read"):
                return []
            
            suggestions = []
            
            # Analyze team structure
            role_distribution = self._analyze_role_distribution(team)
            if role_distribution["imbalance"]:
                suggestions.append({
                    "type": "role_balance",
                    "priority": "medium",
                    "title": "Role Distribution Imbalance",
                    "description": "Consider rebalancing team roles for better collaboration",
                    "action": "Review member roles and adjust as needed"
                })
            
            # Check subscription limits
            if team.member_count >= team.member_limit * 0.9:
                suggestions.append({
                    "type": "subscription",
                    "priority": "high",
                    "title": "Approaching Member Limit",
                    "description": f"Team is using {team.member_count}/{team.member_limit} member slots",
                    "action": "Consider upgrading subscription tier"
                })
            
            # AI-powered suggestions
            if self.llm_client:
                try:
                    ai_suggestions = await self._get_ai_team_suggestions(team)
                    suggestions.extend(ai_suggestions)
                except Exception as e:
                    logger.warning(f"Failed to get AI suggestions: {str(e)}")
            
            return suggestions[:10]  # Limit to top 10 suggestions
            
        except Exception as e:
            logger.error(f"Error generating team suggestions: {str(e)}")
            return []
    
    # Helper methods
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return secrets.token_hex(16)
    
    def _generate_invitation_token(self) -> str:
        """Generate secure invitation token"""
        return secrets.token_urlsafe(32)
    
    async def _store_team(self, team: Team):
        """Store team (in production, this would use database)"""
        self._teams_cache[team.id] = team
    
    async def _get_team(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        return self._teams_cache.get(team_id)
    
    async def _find_team_by_invitation(self, token: str) -> Optional[Team]:
        """Find team by invitation token"""
        for team in self._teams_cache.values():
            if team.get_invitation(token):
                return team
        return None
    
    async def _suggest_member_role(
        self, 
        team: Team, 
        email: str, 
        message: str
    ) -> UserRole:
        """
        AI-powered role suggestion based on context
        """
        
        if not self.llm_client or not self.ai_role_assignment:
            return UserRole.USER  # Default role
        
        try:
            prompt = f"""
            Analyze the following information and suggest the most appropriate role for a new team member:
            
            Team: {team.name}
            Team size: {team.member_count} members
            Current roles: {[m.role.value for m in team.members]}
            
            New member email: {email}
            Invitation message: {message or "No message provided"}
            
            Available roles:
            - owner: Full access (reserved for team creator)
            - admin: Administrative access
            - manager: Departmental management
            - user: Standard user access
            - viewer: Read-only access
            - guest: Limited temporary access
            
            Suggest the most appropriate role and explain why in one sentence.
            Format: ROLE: explanation
            """
            
            response = await self.llm_client.generate_response(prompt)
            
            # Parse response
            content = response.content.lower()
            if "admin:" in content:
                return UserRole.ADMIN
            elif "manager:" in content:
                return UserRole.MANAGER
            elif "viewer:" in content:
                return UserRole.VIEWER
            elif "guest:" in content:
                return UserRole.GUEST
            else:
                return UserRole.USER
                
        except Exception as e:
            logger.warning(f"AI role suggestion failed: {str(e)}")
            return UserRole.USER
    
    async def _send_invitation_email(self, team: Team, invitation: Invitation):
        """Send invitation email"""
        if not self.email_service:
            return
        
        # In production, this would use a proper email template
        subject = f"Invitation to join {team.name}"
        body = f"""
        You've been invited to join {team.name} as a {invitation.role.value}.
        
        {invitation.message or ""}
        
        Click here to accept: [invitation_link]?token={invitation.token}
        
        This invitation expires on {invitation.expires_at.strftime('%Y-%m-%d %H:%M')}.
        """
        
        await self.email_service.send_email(
            to=invitation.email,
            subject=subject,
            body=body
        )
    
    async def _generate_team_setup_recommendations(self, team: Team):
        """Generate AI-powered setup recommendations for new team"""
        if not self.llm_client:
            return
        
        try:
            prompt = f"""
            A new team "{team.name}" has been created with 1 owner.
            Provide 5 specific recommendations for setting up and organizing this team effectively.
            
            Consider:
            1. Team structure and roles
            2. Initial workflows
            3. Communication practices
            4. Security settings
            5. Productivity tools
            
            Format as numbered list with brief explanations.
            """
            
            response = await self.llm_client.generate_response(prompt)
            
            # Store recommendations in team metadata
            if "recommendations" not in team.settings:
                team.settings["recommendations"] = []
            
            team.settings["recommendations"].append({
                "type": "setup",
                "generated_at": datetime.now().isoformat(),
                "content": response.content
            })
            
        except Exception as e:
            logger.error(f"Error generating setup recommendations: {str(e)}")
    
    async def _generate_onboarding_recommendations(self, team: Team, member: TeamMember):
        """Generate personalized onboarding recommendations"""
        if not self.llm_client:
            return
        
        try:
            prompt = f"""
            Generate personalized onboarding recommendations for a new team member:
            
            Team: {team.name} ({team.member_count} members)
            New member: {member.name} ({member.role.value})
            
            Provide 3-5 specific next steps this person should take to get started effectively.
            Focus on their role and current team structure.
            """
            
            response = await self.llm_client.generate_response(prompt)
            
            # Store in member profile
            member.profile_data["onboarding_recommendations"] = {
                "generated_at": datetime.now().isoformat(),
                "content": response.content
            }
            
        except Exception as e:
            logger.error(f"Error generating onboarding recommendations: {str(e)}")
    
    # Mock data methods (replace with real data in production)
    
    def _mock_login_count(self, member: TeamMember) -> int:
        """Mock login count for demo"""
        import random
        return random.randint(5, 30)
    
    def _mock_avg_session_duration(self, team: Team) -> float:
        """Mock average session duration"""
        import random
        return random.uniform(45.0, 180.0)  # minutes
    
    def _mock_documents_processed(self, team: Team, days: int) -> int:
        """Mock documents processed"""
        import random
        return random.randint(days * 2, days * 10)
    
    def _mock_ai_queries(self, team: Team, days: int) -> int:
        """Mock AI queries count"""
        import random
        return random.randint(days * 5, days * 25)
    
    def _mock_reports_generated(self, team: Team, days: int) -> int:
        """Mock reports generated"""
        import random
        return random.randint(days // 7, days // 2)
    
    def _mock_shared_files(self, team: Team, days: int) -> int:
        """Mock shared files count"""
        import random
        return random.randint(days * 3, days * 15)
    
    def _mock_team_discussions(self, team: Team, days: int) -> int:
        """Mock team discussions"""
        import random
        return random.randint(days * 2, days * 8)
    
    def _mock_approval_workflows(self, team: Team, days: int) -> int:
        """Mock approval workflows"""
        import random
        return random.randint(days // 5, days // 2)
    
    def _calculate_productivity_score(self, team: Team) -> float:
        """Calculate team productivity score"""
        import random
        # In production, this would be based on real metrics
        base_score = 0.7
        member_factor = min(team.member_count / 10.0, 1.0) * 0.2
        return min(base_score + member_factor + random.uniform(-0.1, 0.1), 1.0)
    
    def _calculate_collaboration_rating(self, team: Team) -> float:
        """Calculate team collaboration rating"""
        import random
        # In production, this would be based on interaction metrics
        base_rating = 0.75
        return min(base_rating + random.uniform(-0.15, 0.15), 1.0)
    
    def _analyze_role_distribution(self, team: Team) -> Dict[str, Any]:
        """Analyze team role distribution"""
        
        role_counts = {}
        for member in team.members:
            role_counts[member.role.value] = role_counts.get(member.role.value, 0) + 1
        
        total_members = team.member_count
        
        # Check for imbalances
        admin_ratio = (role_counts.get("admin", 0) + role_counts.get("owner", 0)) / total_members
        viewer_ratio = role_counts.get("viewer", 0) / total_members
        
        imbalance = admin_ratio > 0.5 or viewer_ratio > 0.7
        
        return {
            "role_counts": role_counts,
            "admin_ratio": admin_ratio,
            "viewer_ratio": viewer_ratio,
            "imbalance": imbalance
        }
    
    async def _generate_team_recommendations(
        self, 
        team: Team, 
        analytics: TeamAnalytics
    ) -> List[str]:
        """Generate AI-powered team recommendations"""
        
        if not self.llm_client:
            return []
        
        try:
            prompt = f"""
            Analyze this team data and provide 3-5 specific recommendations:
            
            Team: {team.name}
            Members: {analytics.active_members}
            Productivity Score: {analytics.productivity_score:.2f}
            Collaboration Rating: {analytics.collaboration_rating:.2f}
            
            Recent Activity:
            - Documents processed: {analytics.documents_processed}
            - AI queries: {analytics.ai_queries}
            - Reports generated: {analytics.reports_generated}
            - Shared files: {analytics.shared_files}
            
            Provide actionable recommendations to improve team performance and collaboration.
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
            logger.error(f"Error generating team recommendations: {str(e)}")
            return []
    
    async def _get_ai_team_suggestions(self, team: Team) -> List[Dict[str, Any]]:
        """Get AI-powered team improvement suggestions"""
        
        if not self.llm_client:
            return []
        
        try:
            role_distribution = self._analyze_role_distribution(team)
            
            prompt = f"""
            Analyze this team and suggest improvements:
            
            Team: {team.name}
            Size: {team.member_count} members
            Role distribution: {role_distribution["role_counts"]}
            Subscription: {team.subscription_tier.value}
            
            Suggest 2-3 specific improvements with priority level (high/medium/low).
            Format as JSON-like structure with type, priority, title, description, action fields.
            """
            
            response = await self.llm_client.generate_response(prompt)
            
            # For demo purposes, return mock suggestions
            # In production, parse the AI response properly
            return [
                {
                    "type": "communication",
                    "priority": "medium", 
                    "title": "Improve Team Communication",
                    "description": "Set up regular team meetings and communication channels",
                    "action": "Schedule weekly team sync meetings"
                },
                {
                    "type": "workflow",
                    "priority": "high",
                    "title": "Streamline Approval Process",
                    "description": "Implement automated approval workflows for common tasks",
                    "action": "Configure approval templates for routine processes"
                }
            ]
            
        except Exception as e:
            logger.error(f"Error getting AI suggestions: {str(e)}")
            return []


def create_team_service(llm_client=None, email_service=None, **config) -> TeamService:
    """Factory function to create team service"""
    return TeamService(
        llm_client=llm_client,
        email_service=email_service,
        config=config
    )