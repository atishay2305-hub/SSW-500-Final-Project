from flask import Flask
from flask_pymongo import PyMongo
from views import views

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://myuser:mypassword@localhost:8000/SSW-500-project'

mongo = PyMongo(app)

app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
