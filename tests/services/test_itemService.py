from app.services.itemService import ItemService


# =========================================================
# TESTS
# =========================================================

def test_item_service_creates_items():
    service = ItemService()

    assert service.items is not None
    assert isinstance(service.items, dict)


def test_item_service_get_item_exists():
    service = ItemService()

    item = service.getItem("sword")

    assert item is not None


def test_item_service_get_item_missing():
    service = ItemService()

    item = service.getItem("does_not_exist")

    assert item is None