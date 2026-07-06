import pytest


# =========================================================
# LOGIN
# =========================================================

def test_login(controller):
    res = controller.login()

    assert res["success"] is True
    assert res["id"] == 1
    assert "token" in res


# =========================================================
# PLAYER STATS
# =========================================================

def test_get_stats_existing_player(controller):
    stats = controller.getPlayerStats()

    assert "core" in stats
    assert "combat" in stats
    assert "progression" in stats


# =========================================================
# REVIVE
# =========================================================

def test_revive_success(controller):
    res = controller.revive()

    assert res["success"] is True


def test_revive_no_player(monkeypatch, controller):
    monkeypatch.setattr(controller, "_getPlayer", lambda: None)

    res = controller.revive()

    assert res["success"] is False


# =========================================================
# FIGHT
# =========================================================

@pytest.mark.asyncio
async def test_fight_win(controller):
    res = await controller.fight()

    assert res["result"] == "win"

    # side effects should exist
    assert "enemy" in res


@pytest.mark.asyncio
async def test_fight_lose_or_generic(controller, monkeypatch):
    # force combat loss path
    controller.combat.handleFight = lambda p, e: {"result": "lose", "enemy": e}

    res = await controller.fight()

    assert res["result"] == "lose"


# =========================================================
# BUY
# =========================================================

@pytest.mark.asyncio
async def test_buy_success(controller):
    res = await controller.buy("sword", 1)

    assert "cost" in res


@pytest.mark.asyncio
async def test_buy_item_not_found(controller):
    res = await controller.buy("fake_item", 1)

    assert res["success"] is False
    assert res["message"] == "Item not found"


# =========================================================
# SELL
# =========================================================

@pytest.mark.asyncio
async def test_sell_success(controller):
    res = await controller.sell("sword", 1)

    assert "gain" in res


@pytest.mark.asyncio
async def test_sell_item_not_found(controller):
    res = await controller.sell("fake_item", 1)

    assert res["success"] is False
    assert res["message"] == "Item not found"


# =========================================================
# QUEST CLAIM
# =========================================================

@pytest.mark.asyncio
async def test_claim_quest_success(controller):
    qm = controller.questManager

    # fake quest
    class Q:
        def __init__(self):
            self.name = "goblin"
            self.completed = True
            self.claimed = True

    qm.quests = [Q()]

    res = await controller.claimQuest("goblin")

    assert res["success"] is True
    assert "rewards" in res


@pytest.mark.asyncio
async def test_claim_quest_not_found(controller):
    res = await controller.claimQuest("missing")

    assert "error" in res


# =========================================================
# SHOP / INVENTORY READS
# =========================================================

def test_get_shop(controller):
    shop = controller.getShop()
    assert shop is not None


def test_get_inventory(controller):
    inv = controller.getInventory()
    assert inv is not None