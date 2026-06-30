import pytest

def test_login(controller):
    res = controller.login()

    assert res["success"] is True
    assert "token" in res


def test_get_stats(controller):
    stats = controller.getPlayerStats()
    assert "core" in stats


def test_revive(controller):
    res = controller.revive()
    assert res["success"] is True


@pytest.mark.asyncio
async def test_fight(controller):
    res = await controller.fight()
    assert res["result"] == "win"


@pytest.mark.asyncio
async def test_buy(controller):
    res = await controller.buy("sword", 1)
    assert res["cost"] == 10