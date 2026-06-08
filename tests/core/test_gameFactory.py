import pytest

from app.core.gameFactory import PlayerFactory, GameFactory


def test_player_factory_uses_defaults():
    player = PlayerFactory.fromData({})

    assert player.gold == 0
    assert player.hp == 100
    assert player.level == 1
    assert player.xp == 0


def test_player_factory_hydrates_player():
    player = PlayerFactory.fromData(
        {
            "gold": 500,
            "hp": 75,
            "level": 10,
            "xp": 2500,
        }
    )

    assert player.gold == 500
    assert player.hp == 75
    assert player.level == 10
    assert player.xp == 2500


def test_game_factory_raises_when_player_not_found(monkeypatch):
    factory = GameFactory()

    monkeypatch.setattr(
        factory.repos.player,
        "load",
        lambda playerId: None,
    )

    with pytest.raises(ValueError, match="Player not found"):
        factory.create(1)