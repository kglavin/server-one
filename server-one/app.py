import os
import json
from datetime import datetime
from flask import Flask
import requests
import urllib
import google.auth
import google.auth.transport.requests
import google.oauth2.id_token
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
import pprint

creds = None
oid_creds = None
sa_key = None
id_token = None
oid_token = None


def list_project_instances(project_id = 'planar-night-391421', zone='us-west2-a', creds=None):
    ret = []
    compute = discovery.build('compute', 'v1', credentials=creds)
    result = compute.instances().list(project=project_id,  zone=zone).execute()
    instances = result.get('items', [])
    if not instances:
        print('No instances found.')
        ret.append("No instances found")
    else:
        print('Instances:')
        ret.append("Instances:")
        for instance in instances:
            print(f'- {instance["name"]}')
            ret.append(f'- {instance["name"]}')
    return "<p>" + "\n".join(ret) + "</p>"
    
def run_cloud_run():
    return "done nothing!"
    
def run_cloud_run2():
    req = urllib.request.Request('https://us-central1-planar-night-391421.cloudfunctions.net/function-1')
    auth_req = google.auth.transport.requests.Request()
    _id_token = google.oauth2.id_token.fetch_id_token(auth_req, 'https://us-central1-planar-night-391421.cloudfunctions.net/function-1')
    bearer = f"Bearer {_id_token}"
    print(bearer)
    req.add_header("Authorization", bearer)
    response = urllib.request.urlopen(req)
    print(response.code)
    if response.code != 200:
        return f'cloud-run invocation failed, response is : {response.code}'
    else:
        return f'cloud-run invocation success, response is : {response.code}, {bearer }, {response.read()}'

def fibonacci(n=10):
    num1 = 0
    num2 = 1
    next_number = num2 
    count = 1
 
    while count <= n:
       count += 1
       num1, num2 = num2, next_number
       next_number = num1 + num2
    return next_number

def do_work_and_respond():
    ret = []
    ret.append("<H1>This is a server-one pplication</H1>" )
    ret.append("<p>" + str(datetime.now()) + "</p>")
    ret.append("<H2>trying accessing google services</H2>")
    ret.append(" GA_creds = " + os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 
    #with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as file:
    #    data = file.read()
    #    ret.append("<p>" + data + "</p>") 
    ret.append("<p> pp creds = " + pprint.pformat(creds, indent=4) + "</p>")
    for attr in dir(creds):
        if not attr.startswith("__"):
            ret.append("<p>" + attr + "=" + getattr(creds, attr) + "</p>")

    #ret.append("<p>" + str(list_project_instances(creds=creds)) + "</p>")
    ret.append("<H2>trying accessing cloud run lambda function<H2>")
    #ret.append("<p>" + str(run_cloud_run()) + "</p>")
    ret.append("<H2>end of data</H2>")
    ret.append("\n")
    return "\n".join(ret)

app = Flask(__name__)
@app.route("/")
def rootdir():
    fibonacci(n=150000)
    return do_work_and_respond()
      
@app.route("/100")
def onehdir():
        return do_work_and_respond()

@app.route("/1000")
def onetdir():
    return do_work_and_respond()

if __name__ == "__main__":
    #proxy = 'http://10.168.0.2:3128'
    #os.environ['https_proxy'] = proxy
    print(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) 
    key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    #key_path='/tmp/key.json'
    #credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
    #credentials = service_account.Credentials.from_service_account_file(key_path)
    #id_token = credentials.token

    #auth_req = google.auth.transport.requests.Request()
    # credentials.refresh(auth_req)
    #audience = 'https://hello-yvx5f5cjfq-uc.a.run.app'
    creds = Credentials.from_service_account_file(key_path)
    #oid_creds = service_account.IDTokenCredentials.from_service_account_file(
    #   key_path, target_audience=audience)

    #sa_key = os.environ['gkey']
    #sa_info = json.loads(sa_key)
    #creds = Credentials.from_service_account_info(sa_info)
    app.run(host='0.0.0.0', debug=True)
