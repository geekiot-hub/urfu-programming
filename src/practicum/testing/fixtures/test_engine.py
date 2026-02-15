from engine_class import Engine


# @pytest.mark.usefixtures("run_engine")
def test_engine_is_running(engine):
    print("test_engine_is_running")
    assert engine.is_running


def test_check_engine_class(engine):
    print("test_check_engine_class")
    assert isinstance(engine, Engine)
