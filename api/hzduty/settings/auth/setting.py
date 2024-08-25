from fastapi.security import OAuth2PasswordBearer
JWT_SECRET_KEY = '442ad62dffc991fb3b7f547e00da976702d92f9fca86d3557c73b1f39999fa08'
JWT_ALGORITHM ='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
AUTH_SCHEMA = OAuth2PasswordBearer(tokenUrl="/api/v2.0/duty/settings/auth/login")
AUTH_INIT_USER='admin'
AUTH_INIT_PASSWORD='111111'

