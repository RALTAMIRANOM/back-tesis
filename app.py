from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import json
import atexit

import os
import sys
import platform

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@db-tesis2.csgxfrcls4o7.us-east-1.rds.amazonaws.com/db-tesis2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 

db = SQLAlchemy(app)
from models import Person,User,Permission,Rol,Rol_X_Permission,Entity,Plan,Criterion,ObjectiveStrategic
from models import Evaluation,Evaluation_X_Indicator,Indicator,NivelComponentVariable,Evaluation_X_Question
from models import EvaluationModifiedWeight,Criterion_X_CriticalVariable,Weight,Metric,CriticalVariable,KeyComponent
from models import Question,Process
ma = Marshmallow(app)

@app.route("/createPerson", methods=["POST"])
def create_Person():
    data=request.get_json()
    name_test=data['name']
    maternalSurname_test=data['maternalSurname']
    paternalSurname_test=data['paternalSurname']
    person = Person(name=name_test, maternalSurname=maternalSurname_test,paternalSurname=paternalSurname_test)
    person.save()
    return jsonify(result={"status": 200})

@app.route("/",methods=["GET"])
def hello_world():
    return 'Hello, World!'