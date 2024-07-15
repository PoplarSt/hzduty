from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm.exc import NoResultFound
from .handler import authorization_error_handler, http_error_handler, not_found_error, params_error_handler
from .errors import ServerError, ForbiddenError, NotFoundError, AuthorizationError


def register_error_handler(app: FastAPI):
    """
    统一注册错误处理
    """

    app.add_exception_handler(AuthorizationError, authorization_error_handler)
    # app.add_exception_handler(Error, database_error)
    # app.add_exception_handler(OperationalError, database_offline)
    # app.add_exception_handler(MachineError, machine_error)
    # app.add_exception_handler(IntegrityError, integrity_error)
    app.add_exception_handler(NoResultFound, not_found_error)
    app.add_exception_handler(NotFoundError, not_found_error)
    # app.add_exception_handler(TransitionsError, transitions_error)
    app.add_exception_handler(ValidationError, params_error_handler)
    app.add_exception_handler(RequestValidationError, params_error_handler)

    # app.add_exception_handler(ServerError, server_error)
    # app.add_exception_handler(ExpiredSignatureError, auth_error)
    # app.add_exception_handler(JWTError, auth_error)
    # # app.add_exception_handler(Exception, http_error_handler)
    app.add_exception_handler(Exception, http_error_handler)

    return app


__all__ = ["ServerError", "ForbiddenError", "NotFoundError", "AuthorizationError"]