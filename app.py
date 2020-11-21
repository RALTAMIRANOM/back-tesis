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
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@db-tesis2.csgxfrcls4o7.us-east-1.rds.amazonaws.com/db-tesis2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 

db = SQLAlchemy(app)
from models import Person,User,Permission,Rol,Rol_X_Permission,Entity,Plan,Criterion,ObjectiveStrategic
from models import Evaluation,Evaluation_X_Indicator,Indicator,NivelComponentVariable,Evaluation_X_Question
from models import EvaluationModifiedWeight,Criterion_X_CriticalVariable,Weight,Metric,CriticalVariable,KeyComponent
from models import Question,Process
from sqlalchemy.orm.exc import NoResultFound

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
    try:
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
        lastEvaluation=Evaluation.get_last_registration()
        criterionList = db.session.query(Criterion_X_CriticalVariable,Criterion).\
            join(Criterion_X_CriticalVariable.criterion).filter(Criterion.idPlan==idPlan).all()
        for criterion in criterionList :
            modifyWeight = EvaluationModifiedWeight(idCriterion_X_CriticalVariable=criterion[0].idCriterion_X_CriticalVariable,
            idEvaluation=lastEvaluation.idEvaluation,
            idModifiedWeight=criterion[0].idWeight
            )
            modifyWeight.save()
        indicatorList = db.session.query(Indicator).order_by(Indicator.idIndicator.asc()).all()
        for indicator in indicatorList :
            evaluation_indicator = Evaluation_X_Indicator(idIndicator=indicator.idIndicator,
            idEvaluation=lastEvaluation.idEvaluation)
            evaluation_indicator.save()
        questionList = db.session.query(Question).order_by(Question.idQuestion.asc()).all()
        for question in questionList :
            evaluation_question = Evaluation_X_Question(idQuestion=question.idQuestion,
            idEvaluation=lastEvaluation.idEvaluation,answer=-1)
            evaluation_question.save()
        
        return jsonify(result={"status": 200})
    except Exception as e:
        return jsonify(result={"error": 400})

#@app.route("/validatedUser", methods=["GET"])
@app.route("/validatedUser", methods=["POST"])
def validated_User():
    try:
        data=request.get_json()
        email=data['email']
        password=data['password']
        print(platform.system())
        user = User.get_by_email(email)
        
        if (user.password == password and user.email == email): 
            person = Person.query.get(user.idPerson)
            """ return json.dumps({'result':{"idPerson":person.idPerson, "name":person.name,
            "maternalSurname":person.maternalSurname, "paternalSurname":person.paternalSurname,
            "documentNumber":person.documentNumber,"email": user.email,"nameCharge":user.nameCharge,"idRol":user.idRol}}) """
            response = app.response_class(
            response=json.dumps({'result':{"idPerson":person.idPerson, "name":person.name,
            "maternalSurname":person.maternalSurname, "paternalSurname":person.paternalSurname,
            "documentNumber":person.documentNumber,"email": user.email,"nameCharge":user.nameCharge,"idRol":user.idRol}}),
            status=200,
            mimetype='application/json'
            )

        else:
            response = app.response_class(
            response=json.dumps({'result':{"idPerson": -1}}),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
            response = app.response_class(
            response=json.dumps({'result':{"idPerson": -1}}),
            status=200,
            mimetype='application/json'
            )
            return  response

@app.route("/registerObjectives", methods=["POST"])
def register_Objectives():
    data=request.get_json()
    print(data)
    for objective in data['objectives']:
        objective_row = ObjectiveStrategic(idCriterion=objective['idCriterion'],
                                           idEvaluation=objective['idEvaluation'],
                                           description=objective['description'])
        objective_row.save()
    return jsonify(result={"status": 200})

#consultar la tabla pesos modificados
#@app.route("/consultWeightModify", methods=["GET"])
@app.route("/consultWeightModify", methods=["POST"])
def consult_Weight_Modify():
    data=request.get_json()
    idEvaluation = data['idEvaluation']
    weightModifys = db.session.query(EvaluationModifiedWeight,
    Criterion_X_CriticalVariable,Criterion,CriticalVariable,
    KeyComponent,Weight).\
        join(EvaluationModifiedWeight.criterion_X_CriticalVariable,
        Criterion_X_CriticalVariable.criterion,
        Criterion_X_CriticalVariable.criticalVariable,CriticalVariable.keyComponent,
        EvaluationModifiedWeight.weight).\
            filter(EvaluationModifiedWeight.idEvaluation == idEvaluation).\
                order_by(CriticalVariable.idCriticalVariable.asc()).all()    
    weightModify_list = []
    criticalVariable_list = []
    first_time = True
    for weightModify in weightModifys:
       
        if(first_time):
            weight_dict = {}
            weight_dict['keyComponent'] = weightModify[4].code
            weight_dict['criticalVariableId'] = weightModify[3].idCriticalVariable
            weight_dict['criticalVariableName'] = weightModify[3].name
            #lista de id de pesos
            weightList=[]
            weightList.append(weightModify[0].idModifiedWeight - 1)
            weight_dict['weights'] =  weightList
            #lista de id de evaluacionModifiedWeight
            evaluationModifiedWeightList=[]
            evaluationModifiedWeightList.append(weightModify[0].idEvaluationModifiedWeight)
            weight_dict['evaluationModifiedWeightId']=evaluationModifiedWeightList
            weightModify_list.append(weight_dict)
            first_time=False
            criticalVariable_list.append(weightModify[3])
        else:
            #se valida la variable critica
            if(weightModify[3] in criticalVariable_list):
                weightModify_list[-1]['weights'].append(weightModify[0].idModifiedWeight - 1)
                weightModify_list[-1]['evaluationModifiedWeightId'].append(weightModify[0].idEvaluationModifiedWeight)
            else:
                criticalVariable_list.append(weightModify[3])
                weight_dict = {}
                weight_dict['keyComponent'] = weightModify[4].code
                weight_dict['criticalVariableId'] = weightModify[3].idCriticalVariable
                weight_dict['criticalVariableName'] = weightModify[3].name
                #lista de id de pesos
                weightList=[]
                weightList.append(weightModify[0].idModifiedWeight - 1)
                weight_dict['weights'] =  weightList
                #lista de id de evaluacionModifiedWeight
                evaluationModifiedWeightList=[]
                evaluationModifiedWeightList.append(weightModify[0].idEvaluationModifiedWeight)
                weight_dict['evaluationModifiedWeightId']=evaluationModifiedWeightList
                weightModify_list.append(weight_dict)
    print(weightModify_list)
    return jsonify({'weightModify':weightModify_list})

#modificar la tabla pesos modificados
@app.route("/modifyWeight", methods=["POST"])
def modify_Weight():
    try:
        data=request.get_json()
        listids=data['evaluationModifiedWeightId']
        listweights=data['weights']
        cont= 0
        for listid in listids:
            x = db.session.query(EvaluationModifiedWeight).get(listid)
            x.idModifiedWeight = listweights[cont] + 1
            cont += 1
        db.session.commit()
        return jsonify(result={"status": 200})
    except Exception as e:
        db.session.rollback()
        return jsonify(result={"error": 400})

#mandar componentes clave, variable critica -> preguntas con respuestas guardadas
@app.route("/consultQuestionary", methods=["POST"])
def consult_Questionary():
    try:
        data=request.get_json()
        idEvaluation = data['idEvaluation']
        #realizar los cruces
        questionaries = db.session.query(Evaluation_X_Question,
        Question,CriticalVariable,KeyComponent).\
            join(Evaluation_X_Question.question,
            Question.criticalVariable,CriticalVariable.keyComponent).\
                filter(Evaluation_X_Question.idEvaluation == idEvaluation).\
                    order_by(Evaluation_X_Question.idEvaluation_X_Question.asc()).all()
        
        questionary_list = []
        keyComponent_list = []
        variableCritical_list = []
        first_time = True
        #codigo
        #nombre de key
        #subcategorias
            #nombre de vc
            #preguntas :[{texto:,respuesta:, codigo:}]

        for questionary in questionaries:
            
            if(first_time):
                questionary_dict = {}
                questionary_dict['codigo'] = questionary[3].idKeyComponent
                questionary_dict['nombre'] = questionary[3].name
                #lista de vc
                variableCritical_dict = {}
                variableCritical_dict['nombre'] = questionary[2].name
                variableCritical_dict['preguntas'] = []
                #lista de preguntas
                question_dict = {}
                question_dict['texto'] = questionary[1].name
                question_dict['respuesta'] = questionary[0].answer
                question_dict['id'] = questionary[0].idEvaluation_X_Question
                variableCritical_dict['preguntas'].append(question_dict)
                #Se agrupa en subcategoria    
                subcategory_list = []  
                subcategory_list.append(variableCritical_dict)

                questionary_dict['subcategorias'] = subcategory_list
                questionary_list.append(questionary_dict)
                first_time=False
                keyComponent_list.append(questionary[3])
                variableCritical_list.append(questionary[2])
            else:
                #se valida la variable critica
                if(questionary[3] in keyComponent_list):
                    if(questionary[2] in variableCritical_list):
                        #lista de preguntas
                        question_dict = {}
                        question_dict['texto'] = questionary[1].name
                        question_dict['respuesta'] = questionary[0].answer
                        question_dict['id'] = questionary[0].idEvaluation_X_Question
                        questionary_list[-1]['subcategorias'][-1]['preguntas'].append(question_dict)
                    else:
                        variableCritical_list.append(questionary[2])
                        variableCritical_dict = {}
                        variableCritical_dict['nombre'] = questionary[2].name
                        variableCritical_dict['preguntas'] = []
                        #lista de preguntas
                        question_dict = {}
                        question_dict['texto'] = questionary[1].name
                        question_dict['respuesta'] = questionary[0].answer
                        question_dict['id'] = questionary[0].idEvaluation_X_Question
                        variableCritical_dict['preguntas'].append(question_dict)
                        #Se agrupa en subcategoria 
                        questionary_list[-1]['subcategorias'].append(variableCritical_dict)

                else:
                    keyComponent_list.append(questionary[3])
                    variableCritical_list.append(questionary[2])
                    #lista de vc
                    questionary_dict = {}
                    questionary_dict['codigo'] = questionary[3].idKeyComponent
                    questionary_dict['nombre'] = questionary[3].name
                    #lista de vc
                    variableCritical_dict = {}
                    variableCritical_dict['nombre'] = questionary[2].name
                    variableCritical_dict['preguntas'] = []
                    #lista de preguntas
                    question_dict = {}
                    question_dict['texto'] = questionary[1].name
                    question_dict['respuesta'] = questionary[0].answer
                    question_dict['id'] = questionary[0].idEvaluation_X_Question
                    variableCritical_dict['preguntas'].append(question_dict)
                    #Se agrupa en subcategoria 
                    subcategory_list = []  
                    subcategory_list.append(variableCritical_dict)

                    questionary_dict['subcategorias'] = subcategory_list
                    questionary_list.append(questionary_dict)
        
        print(questionary_list)
        print(questionaries)
        return jsonify({'questionary':questionary_list})
    except Exception as e:
        return jsonify({'questionary':[ {"codigo":-1}]})


#guardar las respuestas x variable critica
@app.route("/saveAnswer", methods=["POST"])
def save_Answer():
    try:
        data=request.get_json()
        listids=data['questiontId']
        listanswers=data['answers']
        cont= 0
        for listid in listids:
            x = db.session.query(Evaluation_X_Question).get(listid)
            x.answer = listanswers[cont]
            cont += 1
        db.session.commit()
        return jsonify(result={"status": 200})
    except Exception as e:
        db.session.rollback()
        return jsonify(result={"error": 400})

#consulta de evaluaciones
#Enviar resultados de criterio x objetivo
#Enviar resultado global
#Envair Resultado por grafico
#@app.route("/getCriterion", methods=["GET"])
@app.route("/getCriterion", methods=["POST"])
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

@app.route("/test",methods=["POST"])
def test():
    prueba = db.session.query(Criterion_X_CriticalVariable,Criterion).\
        join(Criterion_X_CriticalVariable.criterion).filter(Criterion.idPlan==1).all()
    print (prueba[0][0].idWeight)
    return jsonify(prueba[0][0].idWeight)

@app.route("/",methods=["GET"])
def hello_world():
    return 'Hello, World!'
    

if __name__ == "__main__":
    
    app.run(debug=True,host="0.0.0.0", port=80)