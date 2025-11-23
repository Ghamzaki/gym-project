from pydantic import BaseModel
from typing import Optional

# Shared properties
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Properties to receive on creation
class ServiceCreate(ServiceBase):
    pass

# Properties to receive on update
class ServiceUpdate(ServiceBase):
    pass

# Properties stored in DB
class ServiceInDBBase(ServiceBase):
    id: int

    class Config:
        orm_mode = True

# Additional properties to return via API
class Service(ServiceInDBBase):
    pass