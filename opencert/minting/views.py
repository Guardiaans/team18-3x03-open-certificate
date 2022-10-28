# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import imghdr
import json
import os
import re
from wsgiref.util import request_uri

import requests
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import login_required
from flask_session import Session
from werkzeug.utils import secure_filename

from opencert.minting.forms import MintingForm
from opencert.utils import flash_errors

# Folder for NFT Image
UPLOAD_IMAGE_FOLDER = "./opencert/uploads/"

# Folder for NFT metadata
UPLOAD_METADATA_FOLDER = "./opencert/metadataUploads/"

# accepted file format
ACCEPTED_FILE_FORMAT = [".jpg", ".png"]


# check file content
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


blueprint = Blueprint("minting", __name__, static_folder="../static")


@blueprint.route("/minting", methods=["GET", "POST"])
@login_required
def mint1():
    "Upload Image Page"
    if request.method == "POST":
        # Save the file to the server first
        file = request.files["file"]
        filename = secure_filename(file.filename)

        # check file ext n content
        if filename != "":
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ACCEPTED_FILE_FORMAT or file_ext != validate_image(
                file.stream
            ):
                return render_template("minting/mintingImageUpload.html")
            else:
                fileLoc = os.path.join(UPLOAD_IMAGE_FOLDER, filename)
                file.save(fileLoc)

                # Upload the file to Pinata
                url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                payload = {}
                #open file reader
                uploadimagepinatafile = open(fileLoc, "rb")
                files = [
                    (
                        "file",
                        (filename, uploadimagepinatafile, "application/octet-stream"),
                    )
                ]
                headers = {"Authorization": "Bearer " + os.environ.get("JWT_KEY")}
                response = requests.request(
                    "POST", url, headers=headers, data=payload, files=files
                )
                json_data = json.loads(response.text)
                #close file reader
                uploadimagepinatafile.close()
                #remove image file
                if os.path.exists(fileLoc):
                    os.remove(fileLoc)
                else:
                    print("The file does not exist")
                cid = json_data["IpfsHash"]
                session["cid"] = cid
                return redirect(url_for("minting.mint2"))
        else:
            return render_template("minting/mintingImageUpload.html")
    else:
        return render_template("minting/mintingImageUpload.html")


@blueprint.route("/mintingMetadataUpload", methods=["GET", "POST"])
@login_required
def mint2():
    "Upload Metadata Page"
    m = re.compile(r"[()$%_.+@!#^&*;:{}~ `]*$")
    c = re.compile(r"[()$%_.+@!#^&*;:{}~`]*$")
    if request.method == "POST":
        # Save the file to the server first
        imageCID = str(request.form.get("imageHash"))
        certNum = str(request.form.get("certNum"))
        breed = str(request.form.get("breed"))
        generation = str(request.form.get("generation"))
        farm = str(request.form.get("farm"))
        CITESTag = str(request.form.get("CITESTag"))
        DOI = str(request.form.get("DOI"))

        # if len(imageCID) != 0 or len(certNum) != 0 or len(breed) != 0 or len(generation) != 0 or len(farm) != 0 or len(CITESTag) != 0 or len(DOI) != 0 :
        if len(imageCID) < 46 or len(imageCID) > 46 or imageCID.isalnum() == False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(certNum) < 7 or len(certNum) > 7 or certNum.isalnum() == False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(breed) < 6 or len(breed) > 15 or c.match(breed):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(generation) < 5 or len(generation) > 10 or generation.isalnum() == False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(farm) < 5 or len(farm) > 30 or c.match(farm):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(CITESTag) < 6 or len(CITESTag) > 6 or CITESTag.isalnum() == False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(DOI) < 10 or len(DOI) > 10 or m.match(DOI):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)

        metadataString = (
            '{"description":"Arowana Certificate","external_url":"","image":"https://gateway.pinata.cloud/ipfs/'
            + imageCID
            + '","name":"Test Patent","attributes":[{"trait_type":"Certificate Number","value":"'
            + certNum
            + '"},{"trait_type":"Breed","value":"'
            + breed
            + '"},{"trait_type":"Generation","value":"'
            + generation
            + '"},{"trait_type":"Farm","value":"'
            + farm
            + '"},{"trait_type":"CITES Tag Number","value":"'
            + CITESTag
            + '"},{"trait_type":"Date Of Issue","value":"'
            + DOI
            + '"}]}'
        )

        try:
            with open("opencert/metadataUploads/" + imageCID + ".json", "w") as f:
                f.write(metadataString)
                f.close()
        except FileNotFoundError:
            print("The 'docs' directory does not exist")
        # Save the file to the server first
        file = str(imageCID) + ".json"
        filename = secure_filename(file)
        fileLoc2 = os.path.join(UPLOAD_METADATA_FOLDER, filename)

        # Upload the file to Pinata
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        payload = {}
        #open file reader
        uploadmetadatapinatafile = open(fileLoc2, "rb")
        files = [("file", (filename, uploadmetadatapinatafile, "application/octet-stream"))]
        headers = {"Authorization": "Bearer " + os.environ.get("JWT_KEY")}
        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )
        #close file reader
        json_data = json.loads(response.text)
        uploadmetadatapinatafile.close()
        #remove metadatafile
        if os.path.exists(fileLoc2):
            os.remove(fileLoc2)
        else:
            print("The file does not exist")
        cid2 = json_data["IpfsHash"]
        session["cid2"] = cid2
        return redirect(url_for("minting.mint3"))
    else:
        cid = session.get("cid")
        return render_template("minting/mintingMetadataUpload.html", cid=cid)


@blueprint.route("/mintNFT", methods=["GET", "POST"])
@login_required
def mint3():
    "Mint Arowana Cert/ NFT"
    cid2 = session.get("cid2")
    return render_template("minting/mintNFT.html", cid2=cid2)


@blueprint.route("/mintfail", methods=["GET"])
def deletefail():
    """Mint failed page"""
    session.pop('cid', None)
    session.pop('cid2', None)
    return render_template("minting/mintfail.html")


@blueprint.route("/mintsuccess", methods=["GET"])
def deletesucces():
    """Mint succeeded page"""
    session.pop('cid', None)
    session.pop('cid2', None)
    return render_template("minting/mintsuccess.html")
