from pydantic import BaseModel, field_validator

class ItemRequest(BaseModel):
    itemName: str
    quantity: int

    @field_validator("itemName")
    @classmethod
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Item name cannot be empty")
        return v

    @field_validator("quantity")
    @classmethod
    def validate_qty(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be > 0")
        return v


class LoginRequest(BaseModel):
    playerId: int