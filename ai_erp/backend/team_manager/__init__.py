"""
Team Manager Module for AI ERP System

Simplified team management with AI-powered role assignment,
easy invitation system, and intelligent collaboration features.
"""

from .models.team_models import Team, TeamMember, Invitation
from .services.team_service import TeamService

__version__ = "1.0.0"
__all__ = ["Team", "TeamMember", "Invitation", "TeamService"]