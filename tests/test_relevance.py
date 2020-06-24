from relevance.relevance import MyClass, fib, fib_ratio


def test_fib() -> None:
    assert fib(0) == 0
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(4) == 3
    assert fib(5) == 5
    assert fib(10) == 55


def test_fib_ratio() -> None:
    assert fib_ratio(0) == 0
    assert fib_ratio(1) == 1
    assert fib_ratio(2) == 1.0


def test_myclass() -> None:
    classy = MyClass("classy")
    assert classy.name == "classy"
