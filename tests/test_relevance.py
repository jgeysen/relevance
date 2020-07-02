from relevance.relevance import MyClass


def test_myclass() -> None:
    classy = MyClass("classy")
    assert classy.name == "classy"
