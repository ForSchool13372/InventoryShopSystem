from pydantic import BaseModel, field_validator
from typing import List, Literal


# =========================================================
# REQUEST MODELS
# =========================================================

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


# =========================================================
# RESPONSE MODELS (THIS IS THE IMPORTANT UPGRADE)
# =========================================================

class LoginResponse(BaseModel):
    success: bool
    token: str
    id: int


class PlayerResponse(BaseModel):
    gold: int
    hp: int
    level: int
    xp: int


class InventoryResponse(BaseModel):
    items: list


class ShopItem(BaseModel):
    itemName: str
    stock: int
    price: int


class ShopResponse(BaseModel):
    data: List[ShopItem]


class ActionResponse(BaseModel):
    success: bool
    message: str | None = None