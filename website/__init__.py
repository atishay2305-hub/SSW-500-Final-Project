import logging 
from flask import Flask

logging.basicConfig(filename='web_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='sswfivehundred'
    
    logging.info("Curently in init.py. App config done.")
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
