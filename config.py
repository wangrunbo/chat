# App
DEBUG = True
BCRYPT_LEVEL = 13

# Session
SECRET_KEY = "Z'Nf91\x07wL\xf5\x12\x87~:#\x8aLpZW95\xdc\x1d"
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = 'dump/session'
PERMANENT_SESSION_LIFETIME = 3600

# DataResource
SQLALCHEMY_DATABASE_URI = 'sqlite:///chat.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False