from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from core.database import HZDUTY
from model import 组织
from .model import Login, 角色
from .password import get_password_hash, verify_password
from .schemas import UserBase, User, Org, UserCreate
from .setting import AUTH_INIT_USER, AUTH_INIT_PASSWORD


async def query_login(user_id: int, db=Depends(HZDUTY.session)):
    query = select(Login).filter(Login.用户ID == user_id).options(joinedload(Login.角色), joinedload(Login.组织))
    db_login = await db.scalars(query)
    unique_db_login = [dl for dl in db_login.unique()]
    # user_base=[]
    for ddl in unique_db_login:
        user = {
            "用户ID": ddl.用户ID,
            "用户编号": ddl.用户编号,
            "账号": ddl.账号,
            "姓名": ddl.姓名,
            "用户类别ID": ddl.用户类别ID,
            "联系电话": ddl.联系电话,
            "邮箱地址": ddl.邮箱地址,
            "角色": [User(角色ID=s.角色ID, 角色名称=s.角色名称, 角色描述=s.角色描述, 角色标识=s.角色标识) for s in
                     ddl.角色],
            "组织": [Org(组织ID=z.组织ID, 组织名称=z.组织名称, 行政区划ID=z.行政区划ID) for z in ddl.组织]

        }
    return user




    # for dl in unique_db_login:
    #
    #     user_base.append(UserBase(
    #             用户ID=dl.用户ID,
    #             用户编号=dl.用户编号,
    #             账号=dl.账号,
    #             姓名=dl.姓名,
    #             用户类别ID=dl.用户类别ID,
    #             联系电话=dl.联系电话,
    #             邮箱地址=dl.邮箱地址,
    #             角色=[User(角色ID=s.角色ID, 角色名称=s.角色名称, 角色描述=s.角色描述, 角色标识=s.角色标识) for s in dl.角色],
    #             组织=[Org(组织ID=z.组织ID, 组织名称=z.组织名称,行政区划ID=z.行政区划ID) for z in dl.组织]
    #
    #         ))
    #
    # return user_base


async def init_admin_user(db=Depends(HZDUTY.session)):
    query = select(func.count()).where(Login.账号)
    cnt = await db.scalar(query)
    if cnt == 0:
        user = Login(
            账号=AUTH_INIT_USER,
            密码=get_password_hash(AUTH_INIT_PASSWORD)
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)


async def get_user(username: str, db=Depends(HZDUTY.session)):
    user = await db.scalars(select(Login).filter(Login.账号 == username))
    return user.first()
    # return db.query(Login).filter(Login.账号 == username).first()


async def authenticate_user(username: str, password: str, db=Depends(HZDUTY.session)):
    user = await get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.密码):
        return False
    return user


async def create_user(user: UserCreate, db=Depends(HZDUTY.session)):
    # 创建 Login 实例
    new_login = Login(

        用户编号=user.用户编号,
        账号=user.账号,
        密码=get_password_hash(user.密码),  # 假设有一个hash_password函数来哈希密码
        姓名=user.姓名,
        用户类别ID=user.用户类别ID,
        # 联系电话=user.联系电话,
        # 邮箱地址=user.邮箱地址
    )
    db.add(new_login)
    await db.commit()
    db.refresh(new_login)

    # 创建角色列表
    for role_data in user.角色:
        role = 角色(
            角色ID=role_data.角色ID,
            角色名称=role_data.角色名称,
            角色描述=role_data.角色描述,
            角色标识=role_data.角色标识,
            用户ID=role_data.用户ID
        )
        db.add(role)

    # 创建组织列表
    for org_data in user.组织:
        org = 组织(
            组织ID=org_data.组织ID,
            组织名称=org_data.组织名称,
            行政区划ID=org_data.行政区划ID,
            用户ID=org_data.用户ID
        )
        db.add(org)

    await db.commit()
    return new_login
