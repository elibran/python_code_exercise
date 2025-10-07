from pydantic import BaseModel, ConfigDict # type: ignore

class TaskCreate(BaseModel):
    title: str

class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    # BEFORE
    # class Config:
    #     from_attributes = True

    # AFTER
    model_config = ConfigDict(from_attributes=True)
