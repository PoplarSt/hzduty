from fastapi import FastAPI, HTTPException, status
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from api.hzduty.settings.auth.password import get_password_hash, verify_password
from api.hzduty.settings.auth.schemas import UserID, Response, Token, UserCreate
from api.hzduty.settings.auth.setting import AUTH_INIT_USER, AUTH_INIT_PASSWORD, AUTH_SCHEMA
from api.hzduty.settings.auth.token import create_token
from core.database import HZDUTY
from api.hzduty.settings.classes.model import 班次, 班次类型
from api.hzduty.settings.auth.crud import query_login, get_user, authenticate_user, create_user
from model import Login, 角色, 组织

router = APIRouter(tags=["登陆管理"])


@router.post("/login/read",
             summary="读取",
             )
async def read_login(id: UserID, db=Depends(HZDUTY.session)):
    user_id = id.用户ID
    shift_types = await query_login(user_id=user_id, db=db)
    response = Response(code="000000", data=shift_types, message="操作成功")
    return response


# dependencies=[Depends(AUTH_SCHEMA)]
@router.post('/login', summary="登录", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db=Depends(HZDUTY.session)):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码无效",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_token(data={"username": user.账号, "password": user.密码})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/add", summary="添加用户", dependencies=[Depends(AUTH_SCHEMA)])
async def create_user1(user: UserCreate, db=Depends(HZDUTY.session)):
    dbuser = await get_user(user.账号, db)
    if dbuser:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="用户已经存在",
        )
    return await create_user(user, db)

# @router.post(
#              "/teamstest123/",
#              summary="AI添加"
#
# )
