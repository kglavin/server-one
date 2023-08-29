import os
import json
from datetime import datetime
from flask import Flask
import requests
import urllib
import google.auth
import google.auth.transport.requests
import google.oauth2.id_token
#from google.oauth2 import service_account
#from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
import pprint
from google.cloud import bigquery

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
        ret.append("No instances found")
    else:
        ret.append("Cluster Nodes:")
        for instance in instances:
            print(f'- {instance["name"]}')
            ret.append(f'- {instance["name"]}\n')
    return "<br/>".join(ret)
    
def run_cloud_run2():
    req = urllib.request.Request('https://function-2-yvx5f5cjfq-lz.a.run.app')
    auth_req = google.auth.transport.requests.Request()
    _id_token = google.oauth2.id_token.fetch_id_token(auth_req, 'https://function-2-yvx5f5cjfq-lz.a.run.app')
    bearer = f"Bearer {_id_token}"
    req.add_header("Authorization", bearer)
    response = urllib.request.urlopen(req)
    print(response.code)
    if response.code != 200:
        return f'cloud-run invocation failed, response is : {response.code}'
    else:
        return response.read()
    
def run_cloud_run():
    req = urllib.request.Request('https://function-1-yvx5f5cjfq-uc.a.run.app')
    auth_req = google.auth.transport.requests.Request()
    _id_token = google.oauth2.id_token.fetch_id_token(auth_req, 'https://function-1-yvx5f5cjfq-uc.a.run.app')
    bearer = f"Bearer {_id_token}"
    req.add_header("Authorization", bearer)
    response = urllib.request.urlopen(req)
    print(response.code)
    if response.code != 200:
        return f'cloud-run invocation failed, response is : {response.code}'
    else:
        return response.read()
    
def do_bigquery():
    ret = []
    ret = ['<img src="https://storage.cloud.google.com/website-bucket-kevin/BedrockSystems.png" alt="bedrocksystems">']
    ret.append("<H1>This is a business application running on a Bedrocked Worker Node.</H1>" )
    ret.append("<H2>" + str(datetime.now()) + "</H2>")
    ret.append("<H1>This is a call to Big Query</H1>" )
    client = bigquery.Client()
    QUERY = (
        'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "CA" '
        'LIMIT 10')
    query_job = client.query(QUERY)
    rows = query_job.result()
    ret.append(f'<H2> {QUERY} </H2>')
    answer = ""
    for row in rows:
        answer = answer + "," + row.name
    #ret.append(f'<H3>{row.name}\n</H3>')
    #ret.append(f'<H3> {str(rows)} </H3>')
    ret.append ("result = {answer}")
    ret.append('<img src="https://storage.cloud.google.com/website-bucket-kevin/uscensus.png" alt="census">')
    return "\n".join(ret)

def fibonacci(n=10):
    ret = []
    ret.append(f'<H1>This is a call to fibonacci {n} </H1>' )
    num1 = 0
    num2 = 1
    next_number = num2 
    count = 1
    while count <= n:
       count += 1
       num1, num2 = num2, next_number
       next_number = num1 + num2
    ret.append(f'<p> fib({n}) == {next_number} </p>')
    return "\n".join(ret)

def do_work_and_respond(i):
    ret = [ '<html>',
            '<meta charset="UTF-8">',
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />',
            '<title> Protected by Bedrock UltraSecurity</title>', 
            '<img src="https://storage.cloud.google.com/website-bucket-kevin/BedrockSystems.png" alt="bedrocksystems">']
    ret.append("<H1>This is a business application running on a Bedrocked Worker Node.</H1>" )
    ret.append("<H2>" + str(datetime.now()) + "</H2>")
    if i == 0:
        ret.append("<H2>Acessing GKE API. List of other cluster nodes</H2>")
        ret.append("<H2>" + str(list_project_instances(creds=creds)) + "</H2>")
    if i == 1: 
        ret.append("<H2>Accessing Google CloudRun in US-CENTRAL Region<H2>")
        ret.append("<H2>" + str(run_cloud_run()) + "<H2>")
        ret.append('<img src="https://storage.cloud.google.com/website-bucket-kevin/Flag_of_Iowa.svg.png" alt="iowa">')
    if i == 2: 
        ret.append("<H2>Accessing Google CloudRun in NORTH-EUROPE Region<H2>")
        ret.append("<H2>" + str(run_cloud_run2()) + "</H2>")
        ret.append('<img src="https://storage.cloud.google.com/website-bucket-kevin/Flag_of_Finland.svg.png" alt="finland">')
    ret.append("<p>end of data</p></html>")
    ret.append("\n")
    return "\n".join(ret)

app = Flask(__name__)
@app.route("/")
def rootdir():
    return do_work_and_respond(0)
      
@app.route("/function-1")
def onehdir():
        return do_work_and_respond(1)

@app.route("/function-2")
def onetdir():
    return do_work_and_respond(2)

@app.route("/bigquery")
def obigquery():
    return do_bigquery()

@app.route("/100")
def ofibhundred():
    return fibonacci(100)

@app.route("/1000")
def ofibthousand():
    return fibonacci(1000)

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
