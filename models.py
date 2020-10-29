from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Person(db.Model):
    __tablename__ = 'Person'
    idPerson = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    maternalSurname = db.Column(db.String(60), nullable=False)
    paternalSurname = db.Column(db.String(60), nullable=False)
    def save(self):
        if not self.idPerson:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idPerson):
        return Person.query.get(idPerson)

class User(db.Model):
    __tablename__ = 'User'
    idUser = db.Column(db.Integer, primary_key=True)
    idPerson = db.Column(db.Integer, db.ForeignKey('Person.idPerson'), nullable=False)
    idRol = db.Column(db.Integer, db.ForeignKey('Rol.idRol'), nullable=False)    
    email = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    nameCharge = db.Column(db.String(150), nullable=True)
    registerDate = db.Column(db.DateTime, nullable=False)
    @staticmethod
    def get_by_id(idUser):
        return User.query.get(idUser)

class Rol(db.Model):
    __tablename__ = 'Rol'
    idRol = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    @staticmethod
    def get_by_id(idRol):
        return Rol.query.get(idRol)

class Permission(db.Model):
    __tablename__ = 'Permission'
    idPermission = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(60), nullable=False)
    @staticmethod
    def get_by_id(idPermission):
        return Permission.query.get(idPermission)

class Rol_X_Permission(db.Model):
    __tablename__ = 'Rol_X_Permission'
    idRol_X_Permission = db.Column(db.Integer, primary_key=True)
    idRol = db.Column(db.Integer, db.ForeignKey('Rol.idRol'), nullable=False)
    idPermission = db.Column(db.Integer, db.ForeignKey('Permission.idPermission'), nullable=False)
    @staticmethod
    def get_by_id(idRol_X_Permission):
        return Rol_X_Permission.query.get(idRol_X_Permission)

class Entity(db.Model):
    __tablename__ = 'Entity'
    idEntity = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    @staticmethod
    def get_by_id(idEntity):
        return Entity.query.get(idEntity)

class Plan(db.Model):
    __tablename__ = 'Plan'
    idPlan = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(2500), nullable=False)
    @staticmethod
    def get_by_id(idPlan):
        return Plan.query.get(idPlan)

class Criterion(db.Model):
    __tablename__ = 'Criterion'
    idCriterion = db.Column(db.Integer, primary_key=True)
    idPlan = db.Column(db.Integer, db.ForeignKey('Plan.idPlan'), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    def save(self):
        if not self.idCriterion:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idCriterion):
        return Criterion.query.get(idCriterion)

class ObjectiveStrategic(db.Model):
    __tablename__ = 'ObjectiveStrategic'
    idObjectiveStrategic = db.Column(db.Integer, primary_key=True)
    idCriterion = db.Column(db.Integer, db.ForeignKey('Criterion.idCriterion'), nullable=False)
    idEvaluation = db.Column(db.Integer, db.ForeignKey('Evaluation.idEvaluation'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    def save(self):
        if not self.idObjectiveStrategic:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idObjectiveStrategic):
        return ObjectiveStrategic.query.get(idObjectiveStrategic)

class Evaluation(db.Model):
    __tablename__ = 'Evaluation'
    idEvaluation = db.Column(db.Integer, primary_key=True)
    idEntity = db.Column(db.Integer, db.ForeignKey('Entity.idEntity'), nullable=False)
    idPlan = db.Column(db.Integer, db.ForeignKey('Plan.idPlan'), nullable=False)
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'), nullable=False)
    initialDate = db.Column(db.DateTime, nullable=False)
    finalDate = db.Column(db.DateTime, nullable=True)
    @staticmethod
    def get_by_id(idEvaluation):
        return Evaluation.query.get(idEvaluation)

class Evaluation_X_Indicator(db.Model):
    __tablename__ = 'Evaluation_X_Indicator'
    idEvaluation_X_Indicator = db.Column(db.Integer, primary_key=True)
    idEvaluation = db.Column(db.Integer, db.ForeignKey('Evaluation.idEvaluation'), nullable=False)
    idIndicator = db.Column(db.Integer, db.ForeignKey('Indicator.idIndicator'), nullable=False)
    amountSpent = db.Column(db.Numeric(10,2), nullable=True)
    amountRequired = db.Column(db.Numeric(10,2), nullable=True)
    unitMeasure = db.Column(db.String(4), nullable=True)
    frequencyYear = db.Column(db.Integer, nullable=True)
    standard = db.Column(db.String(200), nullable=True)
    interpretation = db.Column(db.String(200), nullable=True)
    @staticmethod
    def get_by_id(idEvaluation_X_Indicator):
        return Evaluation_X_Indicator.query.get(idEvaluation_X_Indicator)

class Indicator(db.Model):
    __tablename__ = 'Indicator'
    idIndicator = db.Column(db.Integer, primary_key=True)
    idCriticalVariable = db.Column(db.Integer, db.ForeignKey('CriticalVariable.idCriticalVariable'), nullable=False)
    name = db.Column(db.String(200), nullable=True)
    def save(self):
        if not self.idIndicator:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idIndicator):
        return Indicator.query.get(idIndicator)

class NivelComponentVariable(db.Model):
    __tablename__ = 'NivelComponentVariable'
    idNivelComponentVariable = db.Column(db.Integer, primary_key=True)
    minimum = db.Column(db.Float, nullable=False)
    maximum = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    def save(self):
        if not self.idNivelComponentVariable:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idNivelComponentVariable):
        return NivelComponentVariable.query.get(idNivelComponentVariable)

class Evaluation_X_Question(db.Model):
    __tablename__ = 'Evaluation_X_Question'
    idEvaluation_X_Question = db.Column(db.Integer, primary_key=True)
    idEvaluation = db.Column(db.Integer, db.ForeignKey('Evaluation.idEvaluation'), nullable=False)
    idQuestion = db.Column(db.Integer, db.ForeignKey('Question.idQuestion'), nullable=False)
    answer = db.Column(db.Integer, nullable=False)
    @staticmethod
    def get_by_id(idEvaluation_X_Question):
        return Evaluation_X_Question.query.get(idEvaluation_X_Question)

class EvaluationModifiedWeight(db.Model):
    __tablename__ = 'EvaluationModifiedWeight'
    idEvaluationModifiedWeight = db.Column(db.Integer, primary_key=True)
    idEvaluation = db.Column(db.Integer, db.ForeignKey('Evaluation.idEvaluation'), nullable=False)
    idCriticalVariable = db.Column(db.Integer, db.ForeignKey('CriticalVariable.idCriticalVariable'), nullable=False)
    idModifiedWeight = db.Column(db.Integer, db.ForeignKey('Weight.idWeight'), nullable=False)
    @staticmethod
    def get_by_id(idEvaluationModifiedWeight):
        return EvaluationModifiedWeight.query.get(idEvaluationModifiedWeight)

class Criterion_X_CriticalVariable(db.Model):
    __tablename__ = 'Criterion_X_CriticalVariable'
    idCriterion_X_CriticalVariable = db.Column(db.Integer, primary_key=True)
    idCriterion = db.Column(db.Integer, db.ForeignKey('Criterion.idCriterion'), nullable=False)
    idCriticalVariable = db.Column(db.Integer, db.ForeignKey('CriticalVariable.idCriticalVariable'), nullable=False)
    idWeight = db.Column(db.Integer, db.ForeignKey('Weight.idWeight'), nullable=False)
    def save(self):
        if not self.idCriterion_X_CriticalVariable:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idCriterion_X_CriticalVariable):
        return Criterion_X_CriticalVariable.query.get(idCriterion_X_CriticalVariable)

class Weight(db.Model):
    __tablename__ = 'Weight'
    idWeight = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    def save(self):
        if not self.idWeight:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idWeight):
        return Weight.query.get(idWeight)

class Metric(db.Model):
    __tablename__ = 'Metric'
    idMetric = db.Column(db.Integer, primary_key=True)
    idCriticalVariable = db.Column(db.Integer, db.ForeignKey('CriticalVariable.idCriticalVariable'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    def save(self):
        if not self.idMetric:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idMetric):
        return Metric.query.get(idMetric)

class CriticalVariable(db.Model):
    __tablename__ = 'CriticalVariable'
    idCriticalVariable = db.Column(db.Integer, primary_key=True)
    idKeyComponent = db.Column(db.Integer, db.ForeignKey('KeyComponent.idKeyComponent'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    def save(self):
        if not self.idCriticalVariable:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idCriticalVariable):
        return CriticalVariable.query.get(idCriticalVariable)

class KeyComponent(db.Model):
    __tablename__ = 'KeyComponent'
    idKeyComponent = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    def save(self):
        if not self.idKeyComponent:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idKeyComponent):
        return KeyComponent.query.get(idKeyComponent)

class Question(db.Model):
    __tablename__ = 'Question'
    idQuestion = db.Column(db.Integer, primary_key=True)
    idCriticalVariable = db.Column(db.Integer, db.ForeignKey('CriticalVariable.idCriticalVariable'), nullable=False)
    idProcess = db.Column(db.Integer, db.ForeignKey('Process.idProcess'), nullable=True)
    name = db.Column(db.Text(), nullable=False)
    def save(self):
        if not self.idQuestion:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idQuestion):
        return Question.query.get(idQuestion)

class Process(db.Model):
    __tablename__ = 'Process'
    idProcess = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    def save(self):
        if not self.idProcess:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(idProcess):
        return Process.query.get(idProcess)


''' email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit() '''


'''     @staticmethod
    def get_by_email(email):
        return Person.query.filter_by(email=email).first() '''