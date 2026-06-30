from app.models.item import Item


def test_item_defaults():
    item = Item(name="Sword", price=10)

    assert item.name == "sword" 
    assert item.price == 10
    assert item.itemType == "misc"
    assert item.description == ""
    assert item.rarity == "common"


def test_item_custom_values():
    item = Item(
        name="Potion",
        price=5,
        itemType="consumable",
        description="heals hp",
        rarity="rare"
    )

    assert item.name == "potion"
    assert item.price == 5
    assert item.itemType == "consumable"
    assert item.description == "heals hp"
    assert item.rarity == "rare"


def test_item_name_always_lowercase():
    item = Item(name="GoLdEn SwOrD", price=100)

    assert item.name == "golden sword"