from os import getenv
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PORT = 53
PROXY_SERVER_TIMEOUT = 5
LEVEL = getenv('LEVEL')
REDIS_PORT = getenv('REDIS_PORT')
REDIS_HOST = getenv('REDIS_HOST')
UPSTREAM = getenv('UPSTREAM')
ENV_NAME= getenv('ENV_NAME')
SERVER_TYPE = getenv("SERVER_TYPE")
LOG_HOST = getenv("LOG_HOST")
LOG_PORT = getenv("LOG_PORT")
LOG_INDEX = getenv("LOG_INDEX")
LOG_LEVEL = getenv("LOG_LEVEL")