import os

from dotenv import load_dotenv

"""
This Python script imports the os and dotenv libraries to load all the environment variables from the .env file
and check the type of environment. If the environment is set to 'production', it loads the production database
credentials and start date. If it is set to 'development', it loads the development database credentials and start date.
The environment variables are then assigned to respective variables for use in the program.

The following environment variables are expected to be present in the .env file:

ENVIRONMENT: Type of environment ('production' or 'development')
DB_PASSWORD: Password for production database
DB_USER: Username for production database
DB_HOST: Host for production database
DB_PORT: Port for production database
DB_DATABASE: Database name for production database
START_DATE: Start date for production database
DEV_DB_PASSWORD: Password for development database
DEV_DB_USER: Username for development database
DEV_DB_HOST: Host for development database
DEV_DB_PORT: Port for development database
DEV_DB_DATABASE: Database name for development database
DEV_START_DATE: Start date for development database
ORGANIZATION_NAMES: Name of organizations for API keys
ORGANIZATION_IDS: IDs of organizations for API keys
API_KEYS: API keys for organizations
"""

#Import all .env variables and check type of environment
load_dotenv()
ENVIRONMENT = os.getenv('ENVIRONMENT')

if ENVIRONMENT == 'production':
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_DATABASE = os.getenv('DB_DATABASE')
    START_DATE = os.getenv('START_DATE')

elif ENVIRONMENT == 'development':
    DB_PASSWORD = os.getenv('DEV_DB_PASSWORD')
    DB_USER = os.getenv('DEV_DB_USER')
    DB_HOST = os.getenv('DEV_DB_HOST')
    DB_PORT = os.getenv('DEV_DB_PORT')
    DB_DATABASE = os.getenv('DEV_DB_DATABASE')
    START_DATE = os.getenv('DEV_START_DATE')

ORGANIZATION_NAMES = os.getenv('ORGANIZATION_NAMES')
ORGANIZATION_IDS = os.getenv('ORGANIZATION_IDS')
API_KEYS = os.getenv('API_KEYS')
