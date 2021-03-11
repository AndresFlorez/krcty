from typing import Optional

from fastapi import Body, FastAPI, Form, Depends, HTTPException
from passlib.context import CryptContext

from auth import get_current_active_user, get_password_hash
from database import db
from models import Employee, Rol, UserInDB, User

app = FastAPI(debug=True)


@app.get('/employees')
async def list_employees():
    employees = []
    for employee in db.employees.find():
        employees.append(Employee(**employee))
    return {'employees': employees}

@app.get('/roles')
async def list_roles():
    roles = []
    print(db.roles)
    for rol in db.rols.find():
        roles.append(Rol(**rol))
    return {'roles': roles}

@app.post('/employees')
async def create_employee(employee: Employee):
    ret = db.employees.insert_one(employee.dict(by_alias=True))
    employee.id = ret.inserted_id
    return {'employee': employee}

@app.post('/roles')
async def create_rol(rol: Rol):
    ret = db.roles.insert_one(rol.dict(by_alias=True))
    rol.id = ret.inserted_id
    return {'rol': rol}

@app.post('/users/signup')
async def create_user(user: UserInDB):
    if db.users.find({'username': user.username}).count() > 0:
        raise HTTPException(status_code=409, detail="User exists")
    pwd = get_password_hash(user.hashed_password)
    user.hashed_password = pwd
    ret = db.users.insert_one(user.dict(by_alias=True))
    user.id = ret.inserted_id
    return {'user': user}

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
