from pydantic import BaseModel


class InputData(BaseModel):
    prompt: str


class Output(BaseModel):
    result: str


class InputDataWPdf(BaseModel):
    prompt: str
    path: str
