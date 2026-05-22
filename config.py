import os
from dotenv import load_dotenv

load_dotenv()

class Config:

	SECRET_KEY = os.getenv('SECRET_KEY')

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///career_os.db')

	SQLALCHEMY_TRACK_NOTIFICATIONS = False

	BASE_DIR = os.path.abspath(os.path.dirname(__file__))
