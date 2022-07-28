from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.Text(), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'User>>>{self.username}'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    phone_num = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def __repr__(self) -> str:
        return f'Customer>>>{self.name}'
    

class ExpenseType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    expense = db.Column(db.String(250), nullable = False)
    type = db.relationship('Expense', backref = 'expense_type')

    def __repr__(self) -> str:
        return f'Expense type>>>{self.expense}'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Integer, db.ForeignKey('expense_type.id'))
    description = db.Column(db.String(250), nullable = False)
    value = db.Column(db.Numeric(20,2), nullable = False)
    due_date = db.Column(db.Date, nullable = False)
    payment_date = db.Column(db.Date, nullable = False)
    past_due_fee = db.Column(db.Numeric(20,2), nullable = False)
    
    def __repr__(self) -> str:
        return f'Expense>>>{self.description}'

class Income(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    project = db.Column(db.Integer, db.ForeignKey('project.id'))
    value = db.Column(db.Numeric(20,2), nullable = False)
    date = db.Column(db.Date, nullable = False)
    
    def __repr__(self) -> str:
        return f'Income value>>>{self.value}'

class ProducerTaskType(db.Model):
    producer = db.Column(db.Integer, db.ForeignKey('producer.id'), primary_key = True)
    task = db.Column(db.Integer, db.ForeignKey('task_type.id'), primary_key = True)
    
    def __repr__(self) -> str:
        return f'{self.producer} - {self.task}'

class Producer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    area = db.Column(db.String(120), unique = True, nullable = False)
    task = db.relationship('Task', backref = 'producer')
    project_producer = db.relationship('ProjectProducer', backref = 'producer_id')
    producer_task_type = db.relationship('ProducerTaskType', backref = 'producer_id2')

    def __repr__(self) -> str:
        return f'Producer>>>{self.name} - {self.area}'

class ProjectProducer(db.Model):
    project = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key = True)
    producer = db.Column(db.Integer, db.ForeignKey('producer.id'), primary_key = True)

    def __repr__(self) -> str:
        return f'{self.project} - {self.producer}'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    customer = db.Column(db.Integer, db.ForeignKey('Customer.id'))
    description = db.Column(db.String(250), nullable = False)
    full_value = db.Column(db.Numeric(20,2), nullable = False)
    task = db.relationship('Task', backref = 'project')
    project_producer = db.relationship('ProjectProducer', backref = 'project_id')
    income = db.relationship('Income', backref = 'project_id2')

    def __repr__(self) -> str:
        return f'{self.description}'

class TaskType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(250), nullable = False)
    task = db.relationship('Task', backref = 'task_type')
    producer_task_type = db.relationship('ProducerTaskType', backref = 'task_type_id')

    def __repr__(self) -> str:
        return f'{self.description}'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    type_id = db.Column(db.Integer, db.ForeignKey('task_type.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'))
    description = db.Column(db.String(250), nullable = False)
    deadline = db.Column(db.Date, nullable = False)
    started = db.Column(db.DateTime, default=datetime.now())
    finished = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f'{self.description}'

