import json
import pytest


def test_getLeaderboard_ws(ws_client, token):
    with ws_client("/api/ws/leaderboard") as ws:

        msg = ws.receive_json()

        # Expect the WS wrapper object
        assert msg["type"] == "LEADERBOARD_UPDATE"
        assert isinstance(msg["data"], list)

        data = msg["data"]

        if len(data) > 0:
            first = data[0]

            assert "playerId" in first
            assert "level" in first
            assert "xp" in first
            assert "gold" in first
