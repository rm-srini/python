# test_math_operations.py
import pytest
from unit_testing.program import add, subtract

@pytest.mark.mandatory
def test_unit_testing_program_add(setup1):
    print("test")
    assert add(2, 3) == 5
    assert add(2, 2) == 4


@pytest.mark.parametrize("a, b, output", [
(3, 2, 1), (5, 3, 2)
])
def test_unit_testing_program_subtract(a, b, output):
    assert subtract(a, b) == output
    assert subtract(a, b) == output

