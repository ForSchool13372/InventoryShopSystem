import json
import pytest


def test_getLeaderboard_ws(ws_client, token):
    with ws_client("/api/ws/leaderboard") as ws:

        msg = ws.receive_json()

        # Event type (your WSManager contract)
        assert msg["type"] == "LEADERBOARD_UPDATE"

        assert isinstance(msg["data"], list)

        data = msg["data"]

        if len(data) > 0:
            first = data[0]

            # Must match LeaderboardService output exactly
            assert "playerId" in first
            assert isinstance(first["playerId"], int)

            assert "level" in first
            assert "xp" in first
            assert "gold" in first

            # optional sanity check (new system consistency)
            assert first["level"] >= 1
            assert first["xp"] >= 0