from pydantic import BaseModel

class BlogCreate(BaseModel):
    name:str
    
class BlogResponse(BaseModel):
    id:int
    name:str
    
    class config:
        form_attributes=True