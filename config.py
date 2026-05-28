import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_url = os.environ.get("DATABASE_URL", "sqlite:///career_os.db")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)


class Config:

	SECRET_KEY = os.getenv('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = db_url

	SQLALCHEMY_TRACK_NOTIFICATIONS = False

	UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
