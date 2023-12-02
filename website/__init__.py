import logging 
from flask import Flask
from pymongo import MongoClient

logging.basicConfig(filename='web_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

client = MongoClient('localhost', 27017)
db = client.ssw_db
user = db.user #TODO: remove this


print("DB created")
app=None

def create_app():
    global app
    app=Flask(__name__)
    app.config['SECRET_KEY']='sswfivehundred'
    
    logging.info("Curently in init.py. App config done.")
    
    from .views import views
    from .auth import auth

    # Configure MongoDB
    app.config['MONGO_URI'] = "mongodb://localhost:27017/SSW-500"

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app


