# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,

)

from opencert.minting.forms import MintingForm
from opencert.utils import flash_errors
from flask import Blueprint, render_template
from flask_login import login_required


import os
import json
from werkzeug.utils import secure_filename
import requests




#JWT token
JWT_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI2MTEzYjZhMS0wOGFmLTQ5N2EtODVjZS0xMzMzNzkzYzkzOTAiLCJlbWFpbCI6IjIwMDA1NDRAc2l0LnNpbmdhcG9yZXRlY2guZWR1LnNnIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjNmZGU4ZTMzMmQ5MmViY2UxNDk0Iiwic2NvcGVkS2V5U2VjcmV0IjoiNGMyMjVkYzA3OTU4MjYyMzExOTQ4NGJiMmFiZDRkYTU2NTk5M2M3ZjAxYzQ3YmNhM2ExMmY5MWMzMDBlYzhmMSIsImlhdCI6MTY2MjkwMTk4Mn0.WFA3sUCm3r_1_I7i56adA85oYIdQguYnzZdl-6s2qzk"

# Change for your own local uploads
#UPLOAD_FOLDER = 'team18-3x03-open-certificate/opencert/uploads'
UPLOAD_IMAGE_FOLDER = './opencert/uploads/'

#json format
metadata = {"description":"Arowana Certificate","external_url":"","image":"https://gateway.pinata.cloud/ipfs/","name":"Test Patent","attributes":[{"trait_type":"Certificate Number","value":""},{"trait_type":"Breed","value":""},{"trait_type":"Generation","value":""},{"trait_type":"Gender","value":""},{"trait_type":"Farm","value":""},{"trait_type":"AVA Tag Registred Number","value":""},{"trait_type":"CITES Tag Number","value":""},{"trait_type":"Date Of Issue","value":""}]}




blueprint = Blueprint("minting", __name__, static_folder="../static")


@blueprint.route("/minting",methods=["GET", "POST"])
#@login_required
def mint1():
    "Upload Image Page"
    if request.method == 'POST':
        # Save the file to the server first
        file = request.files['file']
        filename = secure_filename(file.filename)
        print(filename)
        fileLoc = os.path.join(UPLOAD_IMAGE_FOLDER, filename)
        file.save(fileLoc)

        # Upload the file to Pinata
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        payload = {}
        files=[('file',(filename ,open(fileLoc,'rb'),'application/octet-stream'))]
        headers = {'Authorization': 'Bearer ' + JWT_KEY}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        json_data = json.loads(response.text)
        cid = json_data['IpfsHash']
        return render_template("minting/mintingMetadataUpload.html", cid=cid )

    return render_template("minting/minting.html")
         

@blueprint.route("/mintingMetadataUpload",methods=["GET", "POST"])
#@login_required
def mint2():
    "Upload Metadata Page"
    if request.method == 'POST':
        # Save the file to the server first
        imageCID = str(request.form.get("imageHash"))
        certNum = str(request.form.get("certNum"))
        breed = str(request.form.get("breed"))
        generation = str(request.form.get("generation"))
        gender = str(request.form.get("gender"))
        farm = str(request.form.get("farm"))
        AVATag = str(request.form.get("AVATag"))
        CITESTag = str(request.form.get("CITESTag"))
        DOI = str(request.form.get("DOI"))

        try:
            with open('metadataUploads/' + imageCID + '.txt', 'w') as f:
                f.write('Create a new text !')
        except FileNotFoundError:
            print("The 'docs' directory does not exist")




        #file = request.files['file']
        #filename = secure_filename(file.filename)
       # fileLoc = os.path.join(UPLOAD_FOLDER, filename)
       # file.save(fileLoc)

        # Upload the file to Pinata
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        payload = {}
        #files=[('file',(filename ,open(fileLoc,'rb'),'application/octet-stream'))]
        headers = {'Authorization': 'Bearer ' + JWT_KEY}
        #response = requests.request("POST", url, headers=headers, data=payload, files=files)
        #json_data = json.loads(response.text)
        #cid = json_data['IpfsHash']
        #return render_template("minting/mintingMetadataUpload.html", cid=cid )

    return render_template("minting/minting.html")
    #form = MintingForm(request.form)

    
