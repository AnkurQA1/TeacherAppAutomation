from pyclbr import readmodule

import requests
import json


from jsonpath import jsonpath

from Acadally.FetchUserData import response

#API URL

url= "https://reqres.in/api/users"

#Read input JSON File
#file= open("C:\\API\\API File.json",'r')
#json_input= file.read()
#request_json= json.loads(json_input)

#print(request_json)

#Make POST request with JSON input body
#response=requests.post(url, request_json)
#print(response.content)

#Validating Response code
#assert response.status_code==201

#Fetch Header from response
#print(response.headers.get('Content-Length'))

#Parse response to JSON Format

#response_json= json.loads(response.text)
#Pick id using JSON Path
#id = jsonpath.jsonpath(response_json, 'id')
#print(id[0])