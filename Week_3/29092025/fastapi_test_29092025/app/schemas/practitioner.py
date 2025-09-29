from pydantic import BaseModel, Field, ConfigDict # type: ignore

class PractitionerBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    specialty: str = Field(min_length=1, max_length=100)

class PractitionerCreate(PractitionerBase):
    pass

class PractitionerUpdate(PractitionerBase):
    pass

class PractitionerRead(PractitionerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
