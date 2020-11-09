import os

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

headers = {"accept": "application/json",
            "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDUyMzI2NjQsInN1YiI6IjEifQ.PrLfAr2v2hu5jb_FFqRUFkq9-flYx6ydYtdXOcWlTfs"
        }
env = os.environ.get("IDENTITY_DOMAIN__ENV")

url = ""

if env == "development":
    url = "https://"+os.environ.get("IDENTITY_DOMAIN_STAGING_AUTH")+'/api/v1/'
if env == "staging":
    url = "https://"+os.environ.get("IDENTITY_DOMAIN_STAGING_AUTH")+'/api/v1/'
if env == "uat":
    url = "https://"+os.environ.get("IDENTITY_DOMAIN_UAT_AUTH")+'/api/v1/'
if env == "production":
    url = "https://"+os.environ.get("IDENTITY_DOMAIN_PROD_AUTH")+'/api/v1/'

payload = {
        "grant_type": "password",
        "username": os.environ.get("IDENTITY_USER"),
        "password": os.environ.get("IDENTITY_USER_PASSWORD")
      }

print (os.environ.get("IDENTITY_USER"))
token_url = url+'login/access-token'
resp = session.post(token_url, payload)
os.environ["BEARER_TOKEN"]=resp.json()["access_token"]
token = "Bearer "+resp.json()["access_token"]