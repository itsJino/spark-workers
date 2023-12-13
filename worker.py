from flask import Flask
from flask import request
from flask import render_template
import requests
import os
import json
from google.cloud import secretmanager
app = Flask(__name__)

def get_api_key() -> str:
    # secret = os.environ.get("compute-api-key")
    # 
    # if secret:
    #     return secret
    # else:
    #     #local testing
    #     with open('.key') as f:
    #         return f.read()
    
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/635007151197/secrets/compute-api-key/versions/2"
    
    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')
      
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/test")
def test():
    #return "Test" # testing 
    return(get_api_key())

@app.route("/add",methods=['GET','POST'])
def add():
  if request.method=='GET':
    return "Use post to add" # replace with form template
  else:
    token= get_api_key()
    ret = addWorker(token,request.form['num'])
    return ret

def addWorker(token, num):
    with open('payload.json') as p:
      tdata=json.load(p)
    tdata['name']='slave'+str(num)
    data=json.dumps(tdata)
    url='https://www.googleapis.com/compute/v1/projects/warm-rookery-400321/zones/europe-west1-b/instances'
    headers={"Authorization": "Bearer "+token}
    resp=requests.post(url,headers=headers, data=data)
    if resp.status_code==200:     
      return "Done"
    else:
      print(resp.content)
      return "Error\n"+resp.content.decode('utf-8') + '\n\n\n'+data



if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')
