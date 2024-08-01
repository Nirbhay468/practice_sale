import datetime
import typing

import pydantic


class BaseSchemaModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        orm_mode: bool = True
        validate_assignment: bool = True
        allow_population_by_field_name: bool = True
