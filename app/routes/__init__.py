from .main import main_bp
from .auth import auth_bp  
from .dashboard import dashboard_bp
from .applications import applications_bp
from .interview_prep import interview_prep_bp
from .mock_interview import mock_interviews_bp
from .resume_analysis import resume_analysis_bp

__all__ = [
"main_bp",
"auth_bp",
"dashboard_bp",
"applications_bp",
"interview_prep_bp",
"resume_analysis_bp",
"mock_interviews_bp",
]