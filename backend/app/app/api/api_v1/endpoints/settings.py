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


from updates import url

print (url)




# pw_url = os.getenv("IDENTITY_DOMAIN_STAGING_AUTH")

# url = "https://"+pw_url

# results = url+'/api/v1/users/?limit=100'

# resp = requests.get(results,  
#             auth = HTTPDigestAuth('dev@hivenetwork.online', 'b6e1b95b4014b48746eff931d16fb3d4a53279600c06605f8397d9962e0a6ad9'))
# if resp.status_code != 200:
# #     # This means something went wrong.
#     print ("failed")
# #     # raise ApiError('GET results {}'.format(resp.status_code))
# # for todo_item in resp.json():
#     # print('{} {}'.format(todo_item['id'], todo_item['summary']))
#     # print (todo_item)
# print (resp.status_code)
# # print (results)