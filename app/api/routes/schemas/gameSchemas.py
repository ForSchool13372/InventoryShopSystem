from pydantic import BaseModel, field_validator, Field, ConfigDict
from typing import List


# =========================================================
# BASE (GLOBAL RULE: snake_case DB -> camelCase API)
# =========================================================

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )


# =========================================================
# REQUEST MODELS
# =========================================================

class ItemRequest(BaseSchema):
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


class LoginRequest(BaseSchema):
    playerId: int


# =========================================================
# RESPONSE MODELS
# =========================================================

class LoginResponse(BaseSchema):
    success: bool
    token: str
    id: int


# =========================================================
# PLAYER
# =========================================================

class PlayerCore(BaseSchema):
    gold: int
    hp: int
    maxHp: int


class PlayerProgression(BaseSchema):
    level: int
    xp: int


class PlayerCombat(BaseSchema):
    attack: int
    defense: int
    critChance: float
    critMultiplier: float


class PlayerResponse(BaseSchema):
    core: PlayerCore
    progression: PlayerProgression
    combat: PlayerCombat


# =========================================================
# INVENTORY
# =========================================================

class InventoryItem(BaseSchema):
    itemName: str = Field(alias="itemname")
    quantity: int
    itemType: str | None = Field(default=None, alias="itemtype")
    description: str | None = None
    rarity: str | None = None
    price: int | None = None


class InventoryResponse(BaseSchema):
    items: List[InventoryItem]


# =========================================================
# SHOP
# =========================================================

class ShopItem(BaseSchema):
    itemName: str = Field(alias="itemname")
    stock: int
    price: int
    itemType: str | None = Field(default=None, alias="itemtype")
    description: str | None = None
    rarity: str | None = None


class ShopResponse(BaseSchema):
    data: List[ShopItem]


# =========================================================
# GENERIC ACTION RESPONSE
# =========================================================

class ActionResponse(BaseSchema):
    success: bool
    message: str | None = None