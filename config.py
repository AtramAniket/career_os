import os
from dotenv import load_dotenv

load_dotenv()

class Config:

	SECRET_KEY = os.getenv('SECRET_KEY', '4526bed2012138f5930bd7c7bdd24b6b07ad8a14c7894407e8f4aaf547e3152448413707165fb2d0963265d5d6310eff3674269427975181')

	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///career_os.db')

	SQLALCHEMY_TRACK_NOTIFICATIONS = False