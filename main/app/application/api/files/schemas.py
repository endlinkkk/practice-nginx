from pydantic import BaseModel



class SFile(BaseModel):
    title: str
    size: int
