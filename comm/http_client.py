import requests
import json

def send(url, data):
    
    data_json = data if type(data) == str else json.dumps(data)

    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}

    response = requests.post(url=url, headers=headers, data=data_json)

    if response is None:
        print('Server status: Error')


    if response.status_code >= 200 and response.status_code < 300:
       print('Server status: OK')
       print('Server response: '+str(response.content))
    else:
        print(response.status_code, response.content)
