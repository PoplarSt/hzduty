import json
from typing import Literal
from fastapi import APIRouter

from pathlib import Path
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType

router = APIRouter(tags=["模型配置"])

data = {
    "title": "Person",
    "type": "object",
    "properties": {
        "first_name": {"type": "string", "description": "The person's first name."},
        "last_name": {
            "type": "string",
            "description": "The person's last name.",
        },
        "age": {
            "description": "Age in years.",
            "type": "integer",
            "minimum": 0,
            "maximum": 200,
        },
        "pets": {
            "type": "array",
            "maxLength": 5,
            "items": [{"$ref": "#/definitions/Pet"}],
        },
        "comment": {"type": "null"},
    },
    "required": ["first_name", "last_name"],
    "definitions": {
        "Pet": {"properties": {"name": {"type": "string"}, "age": {"type": "integer"}}},
        "Dog": {
            "allOf": [
                {"$ref": "#/definitions/Pet"},
                {
                    "title": "Dog",
                    "type": "object",
                    "properties": {"color": {"type": "string"}},
                },
            ]
        },
    },
}


@router.post(
    "/create",
    summary="生成数据模型",
)
async def create_schema_models(
    table: str,
    file_name: str = "generate",
    generator: Literal[
        "pydantic_v2.BaseModel",
        "pydantic.BaseModel",
        "dataclasses.dataclass",
        "typing.TypedDict",
        "msgspec.Struct",
    ] = "pydantic_v2.BaseModel",
):
    """
    查询全部数据表
    """


    temporary_directory = Path.cwd().joinpath("models").joinpath("auto_code").joinpath(file_name)
    output = Path(temporary_directory / "schema.py")
    generate(
        json.dumps(data),
        input_file_type=InputFileType.JsonSchema,
        input_filename="example.json",
        output=output,
        # set up the output model types
        output_model_type=DataModelType.PydanticV2BaseModel,
    )
    model: str = output.read_text()
    
    return model
