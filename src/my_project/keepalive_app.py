"""Resolve GitHub App credentials for keepalive automation."""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping


@dataclass(frozen=True)
class AppCredentials:
    """Structured GitHub App credentials."""

    app_id: str
    private_key: str
    source: str


_APP_PREFIXES = ("KEEPALIVE_APP", "GH_APP", "WORKFLOWS_APP")


def resolve_app_credentials(
    env: Mapping[str, str] | None = None,
) -> AppCredentials | None:
    """Return the highest-priority GitHub App credentials found in env."""
    env = env or os.environ
    for prefix in _APP_PREFIXES:
        app_id = env.get(f"{prefix}_ID")
        private_key = env.get(f"{prefix}_PRIVATE_KEY")
        if not app_id and not private_key:
            continue
        if not app_id or not private_key:
            missing = "ID" if not app_id else "PRIVATE_KEY"
            raise ValueError(f"{prefix}_{missing} is required when {prefix} is set")
        return AppCredentials(app_id=app_id, private_key=private_key, source=prefix)
    return None
