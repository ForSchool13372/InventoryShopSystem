import pytest
from app.services.itemService import ItemService
from app.services.combatService import CombatService
from app.services.gameEventService import GameEventService
from app.services.shopService import ShopService
from tests.utils.test_ctx import ShopTestContext


# =========================================================
# ITEM SERVICE TESTS
# =========================================================

@pytest.mark.parametrize("itemName", ["sword", "potion"])
def test_getItem_returnsItem(itemName):
    service = ItemService()

    item = service.getItem(itemName)

    assert item is not None
    assert hasattr(item, "name")


def test_getItem_invalid_returnsNone():
    service = ItemService()

    item = service.getItem("fake_item")

    assert item is None


# =========================================================
# SHOP SERVICE TESTS
# =========================================================

def test_buy_success(create_player, create_item, fake_shop_repo):
    player = create_player(gold=200)
    item = create_item("sword", 50)

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=2,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    result = service.buy(ctx)

    assert result["success"] is True
    assert player.gold == 100
    assert fake_shop_repo.stock["sword"] == 8


def test_buy_fail_not_enough_gold(create_player, create_item, fake_shop_repo):
    player = create_player(gold=10)
    item = create_item("sword", 50)

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=1,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    result = service.buy(ctx)

    assert result["success"] is False
    assert result["message"] == "Not enough gold"


def test_buy_invalid_quantity(create_player, create_item, fake_shop_repo):
    player = create_player(gold=200)
    item = create_item("sword", 50)

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=0,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    with pytest.raises(ValueError):
        service.buy(ctx)


def test_buy_fail_not_enough_stock(create_player, create_item, fake_shop_repo):
    player = create_player(gold=1000)
    item = create_item("sword", 50)

    fake_shop_repo.stock["sword"] = 1

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=5,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    result = service.buy(ctx)

    assert result["success"] is False
    assert result["message"] == "Not enough stock"


def test_sell_success(create_player, create_item, fake_shop_repo):
    player = create_player(gold=0)
    item = create_item("sword", 50)

    fake_shop_repo.playerItems["sword"] = 3

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=2,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    result = service.sell(ctx)

    assert result["success"] is True
    assert player.gold == 100
    assert fake_shop_repo.stock["sword"] == 12


def test_sell_fail_not_enough_items(create_player, create_item, fake_shop_repo):
    player = create_player(gold=0)
    item = create_item("sword", 50)

    fake_shop_repo.playerItems["sword"] = 1

    service = ShopService(fake_shop_repo)

    ctx = ShopTestContext(
        player=player,
        item=item,
        quantity=5,
        playerId=1,
        shopRepo=fake_shop_repo
    )

    result = service.sell(ctx)

    assert result["success"] is False
    assert result["message"] == "Not enough items"


# =========================================================
# COMBAT TESTS
# =========================================================

def test_fight_returns_valid_structure(create_player, create_enemy):
    player = create_player()
    enemy = create_enemy()

    service = CombatService()

    result = service.handleFight(player, [enemy])

    assert isinstance(result, dict)
    assert "result" in result
    assert "xp" in result
    assert "enemy" in result
    assert "logs" in result
    assert result["result"] in ("win", "lose")
    assert isinstance(result["logs"], list)


# =========================================================
# GAME EVENT TESTS
# =========================================================

def test_fight_win_event(create_player, fake_quest_manager):
    player = create_player()

    service = GameEventService(player, fake_quest_manager)

    service.handleEvent({
        "type": "fightWin",
        "xp": 50,
        "enemy": "goblin"
    })

    assert player.xp == 50
    assert fake_quest_manager.updated_enemy == "goblin"


def test_fight_lose_event(create_player, fake_quest_manager):
    player = create_player()

    service = GameEventService(player, fake_quest_manager)

    service.handleEvent({
        "type": "fightLose"
    })

    assert player.hp == 0