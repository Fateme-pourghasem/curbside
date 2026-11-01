"""Shared fixtures. Tests never depend on a real Google Cloud project."""

import pytest


@pytest.fixture(autouse=True)
def _test_project(monkeypatch):
    monkeypatch.setenv("CURBSIDE_PROJECT_ID", "curbside-test-project")
