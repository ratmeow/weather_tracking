from typing import Any


def safe_int(value: Any):
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None
