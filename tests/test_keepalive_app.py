from __future__ import annotations

import pytest

from my_project.keepalive_app import AppCredentials, resolve_app_credentials


def test_prefers_keepalive_app() -> None:
    env = {
        "KEEPALIVE_APP_ID": "1",
        "KEEPALIVE_APP_PRIVATE_KEY": "keepalive-key",
        "GH_APP_ID": "2",
        "GH_APP_PRIVATE_KEY": "gh-key",
        "WORKFLOWS_APP_ID": "3",
        "WORKFLOWS_APP_PRIVATE_KEY": "workflows-key",
    }

    creds = resolve_app_credentials(env)

    assert creds == AppCredentials(
        app_id="1",
        private_key="keepalive-key",
        source="KEEPALIVE_APP",
    )


def test_falls_back_to_gh_app() -> None:
    env = {
        "GH_APP_ID": "2",
        "GH_APP_PRIVATE_KEY": "gh-key",
    }

    creds = resolve_app_credentials(env)

    assert creds == AppCredentials(
        app_id="2",
        private_key="gh-key",
        source="GH_APP",
    )


def test_falls_back_to_workflows_app() -> None:
    env = {
        "WORKFLOWS_APP_ID": "3",
        "WORKFLOWS_APP_PRIVATE_KEY": "workflows-key",
    }

    creds = resolve_app_credentials(env)

    assert creds == AppCredentials(
        app_id="3",
        private_key="workflows-key",
        source="WORKFLOWS_APP",
    )


def test_requires_both_id_and_key() -> None:
    env = {
        "KEEPALIVE_APP_ID": "1",
    }

    with pytest.raises(ValueError, match="KEEPALIVE_APP_PRIVATE_KEY"):
        resolve_app_credentials(env)


def test_returns_none_when_unset() -> None:
    assert resolve_app_credentials({}) is None
