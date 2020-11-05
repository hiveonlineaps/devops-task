import os
from dotenv import load_dotenv, find_dotenv

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

headers = {"accept": "application/json",
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDUyMzI2NjQsInN1YiI6IjEifQ.PrLfAr2v2hu5jb_FFqRUFkq9-flYx6ydYtdXOcWlTfs"
        }

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

auth = {"user": os.getenv("FIRST_SUPERUSER"),
        "password": os.getenv("FIRST_SUPERUSER_PASSWORD")
    }

payload = {
        "grant_type": "password",
        "username": os.getenv("FIRST_SUPERUSER",
        "password": os.getenv("FIRST_SUPERUSER_PASSWORD")
      }

token_url = url+'/api/v1/login/access-token'
resp = session.post(api, payload)
token = resp.json()["access_token"]