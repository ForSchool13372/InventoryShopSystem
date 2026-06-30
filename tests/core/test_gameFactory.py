import pytest
from app.core.game.gameFactory import PlayerFactory, GameFactory


def test_player_factory_uses_defaults():
    player = PlayerFactory.fromData(1, {})

    assert player.playerId == 1
    assert player.core["gold"] == 0
    assert player.core["hp"] == 100
    assert player.progression["level"] == 1
    assert player.progression["xp"] == 0


def test_player_factory_hydrates_player():
    player = PlayerFactory.fromData(
        1,
        {
            "gold": 500,
            "hp": 75,
            "level": 10,
            "xp": 2500,
        }
    )

    assert player.playerId == 1
    assert player.core["gold"] == 500
    assert player.core["hp"] == 75
    assert player.progression["level"] == 10
    assert player.progression["xp"] == 2500


def test_game_factory_raises_when_player_not_found(monkeypatch):
    factory = GameFactory()

    # IMPORTANT FIX: bypass cache
    monkeypatch.setattr(
        "app.core.game.gameFactory.gameState.getPlayer",
        lambda playerId: None
    )

    monkeypatch.setattr(
        factory.repos.player,
        "load",
        lambda playerId: None,
    )

    with pytest.raises(ValueError, match="Player not found"):
        factory.create(1)