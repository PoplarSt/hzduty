from pathlib import Path
from tempfile import TemporaryDirectory
from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator import DataModelType

json_schema: str = """{
    "title": "数据表列表",
    "type": "object",
    "properties": {
        "数据表": {
            "type": "array",
            "items": [{"$ref": "#/definitions/数据表枚举"}],
        },
    },
    "definitions": {
        "数据表枚举": {"enum": ["Street", "Avenue", "Boulevard"]},
    },
}"""

with TemporaryDirectory() as temporary_directory_name:
    temporary_directory = Path(temporary_directory_name)
    output = Path(temporary_directory / "model.py")
    generate(
        json_schema,
        input_file_type=InputFileType.JsonSchema,
        input_filename="example.json",
        output=output,
        # set up the output model types
        output_model_type=DataModelType.PydanticV2BaseModel,
    )
    model: str = output.read_text()
print(model)