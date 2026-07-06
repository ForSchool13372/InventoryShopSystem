import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.deps import (
    getCurrentPlayerId,
    getCurrentGame,
    getWebsocketPlayerId,
    getCurrentGameWs
)
from app.state.gameState import gameState


# =========================================================
# FAKE GAME FACTORY
# =========================================================

class FakeFactory:
    def create(self, playerId):
        return {
            "playerId": playerId
        }


# =========================================================
# AUTH TESTS
# =========================================================

def test_get_current_player_id(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: {"playerId": 1}
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="token"
    )

    assert getCurrentPlayerId(credentials) == 1


def test_get_current_player_id_invalid_token(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: None
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="bad-token"
    )

    with pytest.raises(HTTPException):
        getCurrentPlayerId(credentials)


def test_get_current_player_id_missing_player_id(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: {}
    )

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="token"
    )

    with pytest.raises(HTTPException):
        getCurrentPlayerId(credentials)


# =========================================================
# GAME TESTS
# =========================================================

def test_get_current_game_creates(monkeypatch):
    gameState.games.clear()

    monkeypatch.setattr(
        "app.core.deps.factory",
        FakeFactory()
    )

    game = getCurrentGame(1)

    assert game["playerId"] == 1
    assert gameState.games[1] == game


def test_get_current_game_reuses(monkeypatch):
    gameState.games.clear()

    existing = {"playerId": 1}
    gameState.games[1] = existing

    game = getCurrentGame(1)

    assert game is existing


# =========================================================
# WEBSOCKET TESTS
# =========================================================

def test_get_websocket_player_id(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: {"playerId": 5}
    )

    assert getWebsocketPlayerId("token") == 5


def test_get_websocket_player_id_invalid(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: None
    )

    assert getWebsocketPlayerId("bad") is None


def test_get_current_game_ws(monkeypatch):
    gameState.games.clear()

    monkeypatch.setattr(
        "app.core.deps.factory",
        FakeFactory()
    )

    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: {"playerId": 7}
    )

    game = getCurrentGameWs("token")

    assert game["playerId"] == 7
    assert gameState.games[7] == game


def test_get_current_game_ws_invalid(monkeypatch):
    monkeypatch.setattr(
        "app.core.deps.verifyToken",
        lambda token: None
    )

    assert getCurrentGameWs("bad") is None