# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import imghdr
import json
import os
import re

import requests
from flask import Blueprint, abort, redirect, render_template, request, session, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from opencert.recaptcha.forms import recaptcha
from opencert.utils import requires_access_level

# Folder for NFT Image
UPLOAD_IMAGE_FOLDER = "./opencert/uploads/"

# Folder for NFT metadata
UPLOAD_METADATA_FOLDER = "./opencert/metadataUploads/"

# accepted file format
ACCEPTED_FILE_FORMAT = [".jpg", ".png"]

blueprint = Blueprint("minting", __name__, static_folder="../static")

# check file content
def validate_image(stream):
    """Validate image."""
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return "." + (format if format != "jpeg" else "jpg")


@blueprint.route("/minting", methods=["GET", "POST"])
@login_required
@requires_access_level(3)
def mint1():
    """Upload Image Page."""
    if request.method == "POST":
        if recaptcha() is not True:
            abort(401)
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
                file_loc = os.path.join(UPLOAD_IMAGE_FOLDER, filename)
                file.save(file_loc)

                # Upload the file to Pinata
                url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
                payload = {}
                # open file reader
                uploadimagepinatafile = open(file_loc, "rb")
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
                # close file reader
                uploadimagepinatafile.close()
                # remove image file
                if os.path.exists(file_loc):
                    os.remove(file_loc)
                else:
                    print("The file does not exist")
                cid = json_data["IpfsHash"]
                session["cid"] = cid
                return redirect(url_for("minting.mint2"))
        else:
            return render_template("minting/mintingImageUpload.html")
    else:
        return render_template(
            "minting/mintingImageUpload.html",
            site_key=os.environ.get("RECAPTCHA_SITE_KEY"),
        )


@blueprint.route("/mintingMetadataUpload", methods=["GET", "POST"])
@login_required
@requires_access_level(3)
def mint2():
    """Upload Metadata Page."""
    m = re.compile(r"[()$%_.+@!#^&*;:{}~ `]*$")
    c = re.compile(r"[()$%_.+@!#^&*;:{}~`]*$")
    if request.method == "POST":
        if recaptcha() is not True:
            abort(401)
        # Save the file to the server first
        image_cid = str(request.form.get("imageHash"))
        cert_num = str(request.form.get("certNum"))
        breed = str(request.form.get("breed"))
        generation = str(request.form.get("generation"))
        farm = str(request.form.get("farm"))
        CITESTag = str(request.form.get("CITESTag"))
        doi = str(request.form.get("DOI"))

        if len(image_cid) < 46 or len(image_cid) > 46 or image_cid.isalnum() is False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(cert_num) < 7 or len(cert_num) > 7 or cert_num.isalnum() is False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(breed) < 6 or len(breed) > 15 or c.match(breed):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(generation) < 5 or len(generation) > 10 or generation.isalnum() is False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(farm) < 5 or len(farm) > 30 or c.match(farm):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(CITESTag) < 6 or len(CITESTag) > 6 or CITESTag.isalnum() is False:
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)
        if len(doi) < 10 or len(doi) > 10 or m.match(doi):
            cid = session.get("cid")
            return render_template("minting/mintingMetadataUpload.html", cid=cid)

        metadataString = (
            '{"description":"Arowana Certificate","external_url":"","image":"https://gateway.pinata.cloud/ipfs/'
            + image_cid
            + '","name":"Test Patent","attributes":[{"trait_type":"Certificate Number","value":"'
            + cert_num
            + '"},{"trait_type":"Breed","value":"'
            + breed
            + '"},{"trait_type":"Generation","value":"'
            + generation
            + '"},{"trait_type":"Farm","value":"'
            + farm
            + '"},{"trait_type":"CITES Tag Number","value":"'
            + CITESTag
            + '"},{"trait_type":"Date Of Issue","value":"'
            + doi
            + '"}]}'
        )

        try:
            with open("opencert/metadataUploads/" + image_cid + ".json", "w") as f:
                f.write(metadataString)
                f.close()
        except FileNotFoundError:
            print("The 'docs' directory does not exist")
        # Save the file to the server first
        file = str(image_cid) + ".json"
        filename = secure_filename(file)
        file_loc2 = os.path.join(UPLOAD_METADATA_FOLDER, filename)

        # Upload the file to Pinata
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        payload = {}
        # open file reader
        uploadmetadatapinatafile = open(file_loc2, "rb")
        files = [
            ("file", (filename, uploadmetadatapinatafile, "application/octet-stream"))
        ]
        headers = {"Authorization": "Bearer " + os.environ.get("JWT_KEY")}
        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files
        )
        # close file reader
        json_data = json.loads(response.text)
        uploadmetadatapinatafile.close()
        # remove metadatafile
        if os.path.exists(file_loc2):
            os.remove(file_loc2)
        else:
            print("The file does not exist")
        cid2 = json_data["IpfsHash"]
        session["cid2"] = cid2
        session.pop("cid", None)
        return redirect(url_for("minting.mint3"))
    else:
        cid = session.get("cid")
        return render_template(
            "minting/mintingMetadataUpload.html",
            cid=cid,
            site_key=os.environ.get("RECAPTCHA_SITE_KEY"),
        )


@blueprint.route("/mintNFT", methods=["GET", "POST"])
@login_required
@requires_access_level(3)
def mint3():
    """Mint Arowana Cert/ NFT."""
    cid2 = session.get("cid2")
    return render_template("minting/mintNFT.html", cid2=cid2)


@blueprint.route("/mintfail", methods=["GET"])
@login_required
@requires_access_level(3)
def deletefail():
    """Mint failed page."""
    session.pop("cid2", None)
    return render_template("minting/mintfail.html")


@blueprint.route("/mintsuccess", methods=["GET"])
@login_required
@requires_access_level(3)
def deletesucces():
    """Mint succeeded page."""
    session.pop("cid2", None)
    return render_template("minting/mintsuccess.html")
