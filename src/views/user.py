from fastapi import APIRouter, Security
from fastapi import Depends, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import src.database as database
from . import schemas
from .core import generate_response_schemas
from fastapi import Depends, FastAPI, HTTPException

from ..config import jwt_config
from ..database.exceptions.core import BaseDbException
from ..database.scripts import user as db_user
from ..database.scripts import user
from src.database.utils import get_session
from . import schemas
from src.config import jwt_config
from src.database.scripts import user as db_user

router = APIRouter(prefix='/users', tags=['User'])


@router.post("/create",
             responses=generate_response_schemas(db_user.create))
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_session)):
    try:
        db_user.create.execute(db=db,
                               password=user.password,
                               username=user.username)

    except BaseDbException as e:
        status_code, message = e.generate_http_exception()
        id = e.get_exception_id()
        return JSONResponse(status_code=status_code, content={'exception_id': id, 'message': message})
@router.get("/me",
            responses={
                401: {}
            },
            response_model=schemas.User)
def get_me(credentials: JwtAuthorizationCredentials = Security(jwt_config.access_security),
           db: Session = Depends(get_session)):
    return schemas.User.model_validate(db_user.get_by_id.execute(db, credentials.subject["id"]))
