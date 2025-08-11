"""
AI ERP 시스템 팀 관리 데이터 모델

팀, 멤버, 초대 및 역할 기반 접근 제어를 위한 데이터 구조를 정의합니다.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import uuid


class UserRole(Enum):
    """계층적 권한을 가진 표준 사용자 역할"""
    OWNER = "owner"           # 모든 권한, 결제 관리 가능
    ADMIN = "admin"           # 결제 제외 모든 권한
    MANAGER = "manager"       # 부서 관리
    USER = "user"             # 일반 사용자 권한
    VIEWER = "viewer"         # 읽기 전용 접근
    GUEST = "guest"           # 제한된 임시 접근


class TeamStatus(Enum):
    ACTIVE = "active"      # 활성
    INACTIVE = "inactive"  # 비활성
    SUSPENDED = "suspended" # 일시정지
    DELETED = "deleted"    # 삭제됨


class InvitationStatus(Enum):
    PENDING = "pending"      # 대기중
    ACCEPTED = "accepted"    # 수락됨
    DECLINED = "declined"    # 거절됨
    EXPIRED = "expired"      # 만료됨
    CANCELLED = "cancelled"  # 취소됨


class SubscriptionTier(Enum):
    FREE = "free"             # 최대 5명
    BASIC = "basic"           # 최대 25명
    PRO = "pro"               # 무제한
    ENTERPRISE = "enterprise" # 맞춤 제한


@dataclass
class Permission:
    """개별 권한 정의"""
    name: str
    module: str
    action: str  # create, read, update, delete, execute
    resource: Optional[str] = None
    conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RoleDefinition:
    """권한을 포함한 역할 정의"""
    name: str
    display_name: str
    description: str
    permissions: List[Permission] = field(default_factory=list)
    is_system_role: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class TeamMember:
    """역할과 권한을 가진 팀 멤버"""
    id: str
    user_id: str
    team_id: str
    email: str
    name: str
    role: UserRole
    custom_permissions: List[Permission] = field(default_factory=list)
    status: str = "active"
    joined_at: datetime = field(default_factory=datetime.now)
    last_active: Optional[datetime] = None
    profile_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())


@dataclass
class Invitation:
    """팀 초대 모델"""
    id: str
    team_id: str
    invited_by: str
    email: str
    role: UserRole
    token: str
    status: InvitationStatus = InvitationStatus.PENDING
    message: Optional[str] = None
    expires_at: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=7))
    created_at: datetime = field(default_factory=datetime.now)
    accepted_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.token:
            self.token = str(uuid.uuid4()).replace('-', '')


@dataclass
class Team:
    """팀/조직 모델"""
    id: str
    name: str
    description: Optional[str]
    owner_id: str
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    status: TeamStatus = TeamStatus.ACTIVE
    settings: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Members and invitations
    members: List[TeamMember] = field(default_factory=list)
    pending_invitations: List[Invitation] = field(default_factory=list)
    
    # Subscription and billing
    subscription_id: Optional[str] = None
    billing_email: Optional[str] = None
    payment_status: str = "active"
    
    # AI-powered features
    ai_settings: Dict[str, Any] = field(default_factory=lambda: {
        "auto_role_assignment": True,
        "smart_permissions": True,
        "collaboration_insights": True,
        "usage_analytics": True
    })
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
    
    @property
    def member_count(self) -> int:
        """Get current active member count"""
        return len([m for m in self.members if m.status == "active"])
    
    @property
    def member_limit(self) -> int:
        """Get member limit based on subscription tier"""
        limits = {
            SubscriptionTier.FREE: 5,
            SubscriptionTier.BASIC: 25,
            SubscriptionTier.PRO: 999999,
            SubscriptionTier.ENTERPRISE: 999999
        }
        return limits.get(self.subscription_tier, 5)
    
    @property
    def can_add_members(self) -> bool:
        """Check if team can add more members"""
        return self.member_count < self.member_limit
    
    def get_member(self, user_id: str) -> Optional[TeamMember]:
        """Get team member by user ID"""
        return next((m for m in self.members if m.user_id == user_id), None)
    
    def get_member_by_email(self, email: str) -> Optional[TeamMember]:
        """Get team member by email"""
        return next((m for m in self.members if m.email.lower() == email.lower()), None)
    
    def add_member(self, member: TeamMember) -> bool:
        """Add member to team"""
        if not self.can_add_members:
            return False
        
        # Check if member already exists
        existing = self.get_member(member.user_id)
        if existing:
            return False
        
        self.members.append(member)
        self.updated_at = datetime.now()
        return True
    
    def remove_member(self, user_id: str) -> bool:
        """Remove member from team"""
        member = self.get_member(user_id)
        if member:
            self.members.remove(member)
            self.updated_at = datetime.now()
            return True
        return False
    
    def update_member_role(self, user_id: str, new_role: UserRole) -> bool:
        """Update member role"""
        member = self.get_member(user_id)
        if member:
            member.role = new_role
            self.updated_at = datetime.now()
            return True
        return False
    
    def create_invitation(self, email: str, role: UserRole, invited_by: str, message: str = None) -> Invitation:
        """Create new invitation"""
        invitation = Invitation(
            id=str(uuid.uuid4()),
            team_id=self.id,
            invited_by=invited_by,
            email=email,
            role=role,
            token=str(uuid.uuid4()).replace('-', ''),
            message=message
        )
        
        self.pending_invitations.append(invitation)
        self.updated_at = datetime.now()
        return invitation
    
    def get_invitation(self, token: str) -> Optional[Invitation]:
        """Get invitation by token"""
        return next((inv for inv in self.pending_invitations if inv.token == token), None)
    
    def accept_invitation(self, token: str, user_id: str, name: str) -> Optional[TeamMember]:
        """Accept invitation and create team member"""
        invitation = self.get_invitation(token)
        
        if not invitation or invitation.status != InvitationStatus.PENDING:
            return None
        
        if invitation.expires_at < datetime.now():
            invitation.status = InvitationStatus.EXPIRED
            return None
        
        if not self.can_add_members:
            return None
        
        # Create new member
        member = TeamMember(
            id=str(uuid.uuid4()),
            user_id=user_id,
            team_id=self.id,
            email=invitation.email,
            name=name,
            role=invitation.role
        )
        
        if self.add_member(member):
            invitation.status = InvitationStatus.ACCEPTED
            invitation.accepted_at = datetime.now()
            return member
        
        return None
    
    def get_role_permissions(self, role: UserRole) -> List[Permission]:
        """Get permissions for a specific role"""
        
        # Define base permissions for each role
        role_permissions = {
            UserRole.OWNER: [
                # Full system access
                Permission("full_access", "*", "*"),
                Permission("billing", "billing", "*"),
                Permission("team_management", "team", "*"),
            ],
            
            UserRole.ADMIN: [
                # Administrative access except billing
                Permission("system_admin", "system", "*"),
                Permission("user_management", "users", "*"),
                Permission("team_management", "team", "read,update"),
                Permission("all_modules", "erp", "*"),
            ],
            
            UserRole.MANAGER: [
                # Departmental management
                Permission("department_management", "department", "*"),
                Permission("team_read", "team", "read"),
                Permission("erp_modules", "erp", "create,read,update"),
                Permission("reports", "reports", "*"),
            ],
            
            UserRole.USER: [
                # Standard user access
                Permission("personal_data", "user", "read,update", resource="own"),
                Permission("erp_basic", "erp", "create,read,update", resource="assigned"),
                Permission("reports", "reports", "read"),
            ],
            
            UserRole.VIEWER: [
                # Read-only access
                Permission("read_only", "erp", "read"),
                Permission("basic_reports", "reports", "read"),
            ],
            
            UserRole.GUEST: [
                # Very limited access
                Permission("limited_read", "erp", "read", resource="public"),
            ]
        }
        
        return role_permissions.get(role, [])
    
    def get_member_permissions(self, user_id: str) -> List[Permission]:
        """Get all permissions for a team member"""
        member = self.get_member(user_id)
        if not member:
            return []
        
        # Base role permissions
        permissions = self.get_role_permissions(member.role)
        
        # Add custom permissions
        permissions.extend(member.custom_permissions)
        
        return permissions
    
    def has_permission(self, user_id: str, module: str, action: str, resource: str = None) -> bool:
        """Check if user has specific permission"""
        permissions = self.get_member_permissions(user_id)
        
        for perm in permissions:
            # Check for wildcard permissions
            if perm.module == "*" and perm.action == "*":
                return True
            
            # Check module and action match
            if (perm.module == module or perm.module == "*") and \
               (perm.action == action or perm.action == "*" or action in perm.action.split(",")):
                
                # Check resource constraints
                if perm.resource is None or perm.resource == resource:
                    return True
        
        return False


@dataclass
class TeamAnalytics:
    """팀 분석 및 인사이트"""
    team_id: str
    period_start: datetime
    period_end: datetime
    
    # Member activity
    active_members: int
    total_logins: int
    avg_session_duration: float
    
    # Usage statistics
    documents_processed: int
    ai_queries: int
    reports_generated: int
    
    # Collaboration metrics
    shared_files: int
    team_discussions: int
    approval_workflows: int
    
    # AI insights
    productivity_score: float
    collaboration_rating: float
    recommendations: List[str] = field(default_factory=list)
    
    generated_at: datetime = field(default_factory=datetime.now)


def get_default_roles() -> List[RoleDefinition]:
    """Get default system roles"""
    
    return [
        RoleDefinition(
            name="owner",
            display_name="Owner",
            description="Full system access including billing and team management",
            is_system_role=True
        ),
        
        RoleDefinition(
            name="admin", 
            display_name="Administrator",
            description="Administrative access to all modules except billing",
            is_system_role=True
        ),
        
        RoleDefinition(
            name="manager",
            display_name="Manager", 
            description="Departmental management with reporting capabilities",
            is_system_role=True
        ),
        
        RoleDefinition(
            name="user",
            display_name="User",
            description="Standard user with access to assigned modules and data",
            is_system_role=True
        ),
        
        RoleDefinition(
            name="viewer",
            display_name="Viewer",
            description="Read-only access to reports and data",
            is_system_role=True
        ),
        
        RoleDefinition(
            name="guest",
            display_name="Guest",
            description="Limited temporary access for external collaborators",
            is_system_role=True
        )
    ]


def create_default_team_settings() -> Dict[str, Any]:
    """Create default team settings"""
    
    return {
        # General settings
        "timezone": "UTC",
        "date_format": "YYYY-MM-DD",
        "currency": "USD",
        "language": "en",
        
        # Security settings
        "two_factor_required": False,
        "password_policy": {
            "min_length": 8,
            "require_uppercase": True,
            "require_numbers": True,
            "require_symbols": False
        },
        "session_timeout": 480,  # 8 hours
        
        # Notification settings
        "email_notifications": True,
        "push_notifications": True,
        "digest_frequency": "weekly",
        
        # Collaboration settings
        "file_sharing": True,
        "external_sharing": False,
        "comment_permissions": "all_members",
        "approval_workflows": True,
        
        # AI settings
        "ai_assistance": True,
        "auto_insights": True,
        "smart_recommendations": True,
        "usage_analytics": True,
        
        # Module access (can be customized per team)
        "enabled_modules": [
            "dashboard",
            "files",
            "contacts",
            "tasks",
            "reports"
        ],
        
        # Branding
        "custom_logo": None,
        "brand_colors": {
            "primary": "#007bff",
            "secondary": "#6c757d"
        }
    }