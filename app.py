from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import atexit
from datetime import date

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

@app.route("/createUser", methods=["POST"])
def create_User():
    data=request.get_json()
    name=data['name']
    maternalSurname=data['maternalSurname']
    paternalSurname=data['paternalSurname']
    documentNumber=data['documentNumber']
    email=data['email']
    password=data['password']
    nameCharge=data['nameCharge']
    registerDate=date.today()
    idRol=data['idRol']
    #date.today().strftime("%d/%m/%Y")
    person = Person(name=name, maternalSurname=maternalSurname,paternalSurname=paternalSurname,documentNumber=documentNumber)
    person.save()
    #prueba = Person.get_by_documentNumber(documentNumber)
    #print(prueba.idPerson)
    person_user = Person.get_last_registration()
    #print(person_user.idPerson)
    user = User(idPerson=person_user.idPerson,idRol=idRol, email=email, password=password, nameCharge=nameCharge, registerDate=registerDate)
    user.save()

    return jsonify(result={"status": 200})

@app.route("/createEvaluation", methods=["POST"])
def create_Evaluation():
    data=request.get_json()
    nameEntity=data['nameEntity']
    addressEntity=data['addressEntity']
    idPlan=data['idPlan']
    idUser=data['idUser']
    initialDate=date.today()
    entity = Entity(name=nameEntity, address=addressEntity)
    entity.save()
    entity_evaluation= Entity.get_by_name(nameEntity)
    idEntity=entity_evaluation.idEntity
    #date.today().strftime("%d/%m/%Y")
    evaluation = Evaluation(idEntity=idEntity, idPlan=idPlan,idUser=idUser,initialDate=initialDate)
    evaluation.save()

    return jsonify(result={"status": 200})

@app.route("/validatedUser", methods=["GET"])
def validated_User():
    data=request.get_json()
    email=data['email']
    password=data['password']
    print(platform.system())
    user = User.get_by_email(email)
    if user.password == password: 
        person = Person.query.get(user.idPerson)
        return json.dumps({'result':{"idPerson":person.idPerson, "name":person.name,
        "maternalSurname":person.maternalSurname, "paternalSurname":person.paternalSurname,
        "documentNumber":person.documentNumber,"email": user.email,"nameCharge":user.nameCharge,"idRol":user.idRol}})
    else:
        return json.dumps({'result':{"idPerson":-1}})

@app.route("/registerObjetic", methods=["POST"])
def register_Objetic():
    data=request.get_json()

@app.route("/getCriterion", methods=["GET"])
def get_Crtierion():
    data=request.get_json()
    idPlan=data['idPlan']
    print(platform.system())
    criterions = Criterion.get_by_Plan(idPlan)
    criterions_list = []
    for criterion in criterions:
        criterion_dict={}
        criterion_dict['idCriterion']=criterion.idCriterion
        criterion_dict['code']=criterion.code
        criterion_dict['name']=criterion.name
        criterion_dict['description']=criterion.description
        criterions_list.append(criterion_dict)
    return jsonify({'criterions':criterions_list})
'''     if user.password == password: 
        person = Person.query.get(user.idPerson)
        return json.dumps({'result':{"idPerson":person.idPerson, "name":person.name,
        "maternalSurname":person.maternalSurname, "paternalSurname":person.paternalSurname,
        "documentNumber":person.documentNumber,"email": user.email,"nameCharge":user.nameCharge,"idRol":user.idRol}})
    else:
        return json.dumps({'result':{"idPerson":-1}}) '''

@app.route("/",methods=["GET"])
def hello_world():
    return 'Hello, World!'
    

if __name__ == "__main__":
    
        app.run(debug=True,host="0.0.0.0", port=80)