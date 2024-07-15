from pydantic import ValidationInfo, field_validator

from models.test_route.schema import UserSchema


class TestParams(UserSchema):

    @field_validator("password", mode="after")
    @classmethod
    def validate_user_passwords(cls, password: str, info: ValidationInfo) -> str:
        """Check that user password is not in forbidden list."""
        if not any(char.isdigit() for char in password):
            raise ValueError("密码至少包含一个数字")
        if not any(char.isalpha() for char in password):
            raise ValueError("密码至少包含一个字母")
        return password
