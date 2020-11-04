import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
env = os.getenv("IDENTITY_DOMAIN__ENV")

url = ""

if env == "development":
    url = "https://"+os.getenv("IDENTITY_DOMAIN_DEV_AUTH")+'/api/v1/'
if env == "staging":
    url = "https://"+os.getenv("IDENTITY_DOMAIN_STAGING_AUTH")+'/api/v1/'
if env == "uat":
    url = "https://"+os.getenv("IDENTITY_DOMAIN_UAT_AUTH")+'/api/v1/'
if env == "production":
    url = "https://"+os.getenv("IDENTITY_DOMAIN_PROD_AUTH")+'/api/v1/'