from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from lib.db_init import *
from model.model_utils import *
# from model.models import  EntityType, Entity, EntityPerson, EntityContact  # Import other models as needed
from model import models




app = FastAPI()

def get_table(model_name, table_dict):
    table_dict["__tablename__"] = f'{model_name.lower()}'
    return type(model_name, (DeclarativeBase,), table_dict)

def authenticate_user(kwargs):
    username = kwargs.get('username')
    password = kwargs.get('password')
    this = DBSession.query(User).\
         filter(User.username == username).\
         filter(User.hashed_password == password).first()
    if this:
        return this.entity_id
    else:
        return False

def get_all(class_name):
    ModelClass = getattr(models, class_name)
    dbase_query = DBSession.query(ModelClass).\
        filter(ModelClass.bln_active == True).all()
    outputlist = []
    for i in dbase_query:
        outputdict = i.__dict__
        outputdict.pop('_sa_instance_state', None)
        outputlist.append(outputdict)

    outputdict = {
        'success' : True,
        'data' : outputlist,
        'message' : 'Success!'
    }
    return outputdict

def update_or_create(class_name, **kwargs):
    ModelClass = getattr(models, class_name)
    instance = DBSession.query(ModelClass).filter_by(**kwargs).first()
    if instance:
        for key, value in kwargs.items():
            setattr(instance, key, value)
    else:
        instance = ModelClass(**kwargs)
        DBSession.add(instance)
    DBSession.commit()
    DBSession.flush()

    return instance

def create(class_name, **kwargs):
    ModelClass = getattr(models, class_name)
    instance = ModelClass(**kwargs)
    DBSession.add(instance)
    DBSession.commit()
    DBSession.flush()
    return instance.id

def get_name_by_id(class_name,id):
     ModelClass = getattr(models, class_name)
     this = DBSession.query(ModelClass).\
         filter(ModelClass.by_id == id).first()
     if this:
         return this.name
     else:
         return None

def get_id_by_name(class_name,name):
     ModelClass = getattr(models, class_name)
     this = DBSession.query(ModelClass).\
         filter(ModelClass.name == name).first()
     if this:
         return this.id
     else:
         return None

def delete_record_by_id(class_name,key_id):
     ModelClass = getattr(models, class_name)
     this = DBSession.query(ModelClass).\
         filter(ModelClass.id == key_id).first()
     if this:
          this.bln_active = False
          DBSession.commit()
          DBSession.flush()
          return True
     else:
         return False

def get_record_by_id(class_name,key_id):
     ModelClass = getattr(models, class_name)
     this = DBSession.query(ModelClass).\
         filter(ModelClass.id == key_id).first()
     if this:
        outputdict = this.__dict__
        outputdict.pop('_sa_instance_state', None)
        return outputdict
     else:
         return False

def get_all_records_by_attr_id(class_name, kwargs):
    ModelClass = getattr(models, class_name)
    attr_name = kwargs.pop('attr_name', None)  # Extract attribute name from kwargs and remove it
    attr_value = kwargs.pop('attr_value', None)  # Extract attribute value from kwargs and remove it

    if attr_name is None or attr_value is None:
        return {
            'success': False,
            'data': [],
            'message': 'Attribute name or value is missing!'
        }

    dbase_query = DBSession.query(ModelClass).filter(
        getattr(ModelClass, attr_name) == attr_value,
        ModelClass.bln_active == True
    ).all()

    outputlist = []
    for record in dbase_query:
        outputdict = record.__dict__.copy()
        outputdict.pop('_sa_instance_state', None)
        outputlist.append(outputdict)

    return {
        'success': True,
        'data': outputlist,
        'message': 'Success!'
    }


def update_record_by_id(class_name, kwargs):
    ModelClass = getattr(models, class_name)
    attr_name = kwargs.pop('attr_name', None)  # Extract attribute name from kwargs and remove it
    instance_id = kwargs.pop(attr_name, None)
    if instance_id is None:
        return None
    instance = DBSession.query(ModelClass).get(instance_id)
    if instance is None:
        return None

    for key, value in kwargs.items():
        setattr(instance, key, value)
    DBSession.commit()
    DBSession.flush()
    return instance.id

def update_by_attr_first(class_name, kwargs):
    ModelClass = getattr(models, class_name)
    attr = kwargs.pop('attr', None)
    instance_id = kwargs.pop('attr_id', None)

    if attr is None or instance_id is None:
        return None

    filter_condition = getattr(ModelClass, attr) == instance_id
    instance = DBSession.query(ModelClass).filter(filter_condition).first()

    if instance is None:
        return None
    for key, value in kwargs.items():
        setattr(instance, key, value)

    DBSession.commit()
    DBSession.flush()
    return instance.id

def check_if_it_exist(class_name, kwargs):
    ModelClass = getattr(models, class_name)
    attr_name = kwargs.pop('attr_name', None)  # Extract attribute name from kwargs
    attr_value = kwargs.pop(attr_name, None)   # Extract attribute value from kwargs
    if attr_value is None:
        return False
    # Construct a filter to check if a record with the specified attribute value exists
    filter_criteria = {attr_name: attr_value}
    instance = DBSession.query(ModelClass).filter_by(**filter_criteria).first()
    if instance:
        return True
    else:
        return False
