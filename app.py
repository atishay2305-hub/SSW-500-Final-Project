from flask import Flask, redirect, url_for, request
import json
import requests

API_URL = ""


app = Flask(__name__)


#for posting the answers to the questions
@app.route("/post", methods=["POST"])
def post_request():

    #Write post here

#also add return values
    return 


