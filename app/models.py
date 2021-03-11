from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo import MongoClient

from database import db


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Rol(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias='_id')
    name: str
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class Employee(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias='_id')
    first_name: str
    last_name: str
    identification: str
    identification_type: str
    rol: Rol
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias='_id')
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class UserInDB(User):
    hashed_password: str
