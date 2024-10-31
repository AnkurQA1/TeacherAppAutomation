import requests
import json


from jsonpath import jsonpath


from Acadally.FetchUserData import response

#API URL

url= "https://reqres.in/api/users/2"

#Read input JSON File
file= open("C:\\API\\API File.json",'r')
json_input= file.read()
request_json= json.loads(json_input)

print(request_json)

#Make PUT request with JSON input body
response=requests.put(url, request_json)
print(response.content)

#Validating Response code
assert response.status_code==200

#Parse Response Content
response_json= json.loads(response.text)
updated_li= jsonpath.jsonpath(response_json, 'updatedAt')
print(updated_li[0])