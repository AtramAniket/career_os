from flask import Flask
from config import Config
from app.extensions import db, migrate, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app import models

    from app.api import api_bp

    from app.routes import main_bp
    from app.routes import auth_bp
    from app.routes import dashboard_bp
    from app.routes import applications_bp
    from app.routes import interview_prep_bp
    from app.routes import resume_analysis_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(interview_prep_bp)
    app.register_blueprint(resume_analysis_bp)

    return app
