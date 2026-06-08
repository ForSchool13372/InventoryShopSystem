import pytest
from fastapi import HTTPException

from app.core.utils.apiUtils import ok, normalize, safeExecute


def test_ok_returns_success_response():
    result = ok({"gold": 100})

    assert result == {
        "success": True,
        "data": {"gold": 100},
    }


def test_normalize_strips_and_lowercases():
    assert normalize("  Sword Of Power  ") == "sword of power"


def test_safe_execute_returns_function_result():
    result = safeExecute(lambda: 42)

    assert result == 42


def test_safe_execute_converts_value_error_to_400():
    def raise_value_error():
        raise ValueError("Invalid item")

    with pytest.raises(HTTPException) as exc:
        safeExecute(raise_value_error)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid item"


def test_safe_execute_converts_unhandled_error_to_500():
    def raise_runtime_error():
        raise RuntimeError("Boom")

    with pytest.raises(HTTPException) as exc:
        safeExecute(raise_runtime_error)

    assert exc.value.status_code == 500
    assert exc.value.detail == "Internal server error"