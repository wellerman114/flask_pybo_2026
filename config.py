import os

# 데이터베이스 접근 환경변수
BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'pybo.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 폼모듈 환경변수
SECRET_KEY = "dev"