from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
PG_USER = "root"#os.environ['PG_USER']
PG_PWD = "TU&m2021"#os.environ['PG_PWD']
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_USER}:{PG_PWD}@localhost:5432/api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init DB
db = SQLAlchemy(app)

#Init Marshmallow
ma = Marshmallow(app)

@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'Hello World 2'})

#Run
if __name__ == '__main__':
    app.run(debug = True)