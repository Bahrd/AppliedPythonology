##  https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
#   Docs: https://pythonbasics.org/flask-rest-api/ 

import requests
import json

def invoke(url, data):
    print('Sent-to a server: ' + json.dumps(data, indent = 3))
    answer = requests.post(url, json = data).content
    return_value = json.loads(answer)
    return return_value['ID']

# A target "namespace" and...   function name... 
url = 'http://localhost:8006/' + 'KT6'
# ... and arguments
data = {'ID':0b1010, 
        'sender': 'Train Driver',
        'receiver': 'Traffic Controller',
        'action': 'Python On Rails',
        'flag': True}
## Invoke a service and wait... for a response
print('Reply-from a server: ', invoke(url, data))