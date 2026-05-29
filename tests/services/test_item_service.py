from app.services.itemService import ItemService

def test_getItem_returnsCorrectItem():
    service = ItemService()

    item = service.getItem("sword")

    assert item is not None