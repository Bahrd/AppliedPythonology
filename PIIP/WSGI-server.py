##  https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
#   https://realpython.com/primer-on-python-decorators/

from flask import Flask, request, send_file
import json

app = Flask(__name__)
# 'Are you alive?'
@app.route('/')
def AYA():
    docs = 'https://pythonbasics.org/flask-rest-api/' 
    return 'Go for <a href ="{0}">docu\'drama<a/>...'.format(docs)

# Request for a file with GET
@app.route('/apps/<converter>', methods = ['GET'])
def download_file(converter):
    return send_file('./WSGI-form.html', as_attachment = False)
# Request form with GET
@app.route('/converter')
def edge_form():
    value = request.args.get('MPG')
    mpg2lkm = 3.78541178/1.609344 * 100 #gallon/mile * km
    return 'Gotcha {:.3}l/100km!'.format(mpg2lkm/eval(value))

# Web service with POST & JSON
@app.route('/JSON-EX', methods = ['POST'])
def JSNX():
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