from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
from web3.middleware import geth_poa_middleware

import os
#import jsonpickle
import webbrowser
import hashlib
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
app = Flask(__name__)


url = "https://api.pinata.cloud/pinning/pinFileToIPFS"


# @app.route('/',methods = ['GET','POST'])
# def first():
#   w3 = Web3(Web3.HTTPProvider("https://skilled-silent-season.matic-testnet.discover.quiknode.pro/04037f06cf629f68a224078ac4cbfffcc2a5d013/"))
#   deployerPrivateKey = os.getenv("ACCOUNT_PRIVATE_KEY")
#   w3.middleware_onion.inject(geth_poa_middleware, layer=0)
#   #account.address='0x09752c5BE00a4820dFa94eD54Da8a07F18f20E14'
#   account = w3.eth.account.privateKeyToAccount(deployerPrivateKey)
#   contract = w3.eth.contract(address = os.getenv("Address") , abi = os.getenv("ABI"))
#   #token_name=contract.functions.set('a','b').transact({ 'from' : '0x09752c5BE00a4820dFa94eD54Da8a07F18f20E14'})
#   #token_name=contract.functions.get_cid('b5a00ba2f885304909f89c30ac55cad1f64c7c77494e4501b8da4681779adb43').call()
#   return account.address

@app.route('/',methods = ['GET','POST'])
def first():
  return render_template("index.html")

@app.route('/getter', methods = ['GET', 'POST'])
def get_files():
  if request.method == 'POST':
    URL = request.form.get("Text")
   
    return webbrowser.open('https://ipfs.io/ipfs/'+URL)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      payload={'pinataOptions': '{"cidVersion": 1}','pinataMetadata': '{"name": "MyFile", "keyvalues": {"company": "Pinata"}}'}
      files=[('file',(f.filename,open(os.getcwd()+'\\'+f.filename,'rb'),'application/octet-stream'))]
      headers = {'Authorization': os.getenv('JWT')}

      response = requests.request("POST", url, headers=headers, data=payload, files=files)

      response=response.json()
      sha256_hash = hashlib.sha256()
      with open(f.filename,"rb") as f:
    # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
          sha256_hash.update(byte_block)
        print(sha256_hash.hexdigest())
      return response['IpfsHash']
    
if __name__ == '__main__':
   app.run(debug = True)