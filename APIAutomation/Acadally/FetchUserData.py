#API URL
import requests
import json
import jsonpath
from urllib3 import request

url= "https://reqres.in/api/users?page=2"

#Send Get Requests
response= requests.get(url)
#Parse response to Json format
json_response=json.loads(response.text)
#print(json_response)

#Fetch value using Jsonpath
pages=jsonpath.jsonpath(json_response, 'total_pages')
assert (pages[0]) == 2
