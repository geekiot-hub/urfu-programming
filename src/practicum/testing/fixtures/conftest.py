import pytest
from engine_class import Engine


@pytest.fixture(scope="session")
def engine():
    print("Вызов произошел!")
    return Engine()


@pytest.fixture(autouse=True)
def run_engine(engine):
    engine.is_running = True
    print(f"Test not running, {engine.is_running=}")
    yield
    engine.is_running = False
    print(f"Test completed, {engine.is_running=}")
