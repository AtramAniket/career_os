import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

	SECRET_KEY = os.getenv('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///career_os.db')

	SQLALCHEMY_TRACK_NOTIFICATIONS = False

	UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

	MAX_CONTENT_LENGTH = 16 * 1024 * 1024
