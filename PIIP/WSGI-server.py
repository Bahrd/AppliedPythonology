##  https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
docs = 'https://pythonbasics.org/flask-rest-api/' 

from flask import Flask, request
import json

app = Flask(__name__)
@app.route('/')
def AYA():
    return 'Go for <a href ="{0}">docu-drama<a/>...'.format(docs)
@app.route('/KT6', methods = ['POST'])
def KT6():
    print('RAW request', request)
    content = request.json
    # Do what you gotta do...
    content['ID'] = 0o52
    print('Reply-to a client: ', json.dumps(content, indent = 3))
    # send a result back to a client
    return content
## Run a server and wait... and wait... for invocation
if __name__ == '__main__':
    app.run(host = 'localhost', port = '8006', debug = True)