from myproject.main import add


def test_add() -> None:
    assert add(3, 5) == 8
