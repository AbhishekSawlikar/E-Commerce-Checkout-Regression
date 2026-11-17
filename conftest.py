from pathlib import Path


def pytest_sessionstart(session):
    Path("reports").mkdir(exist_ok=True)
