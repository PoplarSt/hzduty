from datetime import *
from jose import jwt

from api.hzduty.settings.auth.setting import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# 这段代码通常用于Web应用程序的身份验证流程：
#
# create_token函数在用户登录成功后调用，生成一个包含用户信息和过期时间的JWT，然后发送给用户。
# extract_token函数在需要验证用户身份的请求中调用，从JWT中提取用户信息。
def extract_token(token:str):
 payload=jwt.decode(token,JWT_SECRET_KEY,JWT_ALGORITHM)
 return payload.get("username")
def create_token(data:dict):
 to_encode = data.copy()
 expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
 expire=datetime.now() + expires_delta
 to_encode.update({"exp":expire})
 encoded_jwt=jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
 return encoded_jwt
