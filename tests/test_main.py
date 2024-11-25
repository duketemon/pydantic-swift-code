import pytest
from hypothesis import given, settings, strategies as st
from pydantic import ValidationError
from pydantic_swift_code import SwiftCode


# Helper function to generate valid SWIFT codes
def generate_valid_swift_code(length=8):
    import random
    random.seed(1234)  # Set seed for determinism
    import string
    bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
    country_code = ''.join(random.choices(string.ascii_uppercase, k=2))
    location_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
    branch_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3)) if length == 11 else ''
    return f"{bank_code}{country_code}{location_code}{branch_code}"


# Hypothesis strategy for valid SWIFT codes
valid_swift_codes = st.sampled_from([generate_valid_swift_code(8), generate_valid_swift_code(11)])


# Hypothesis strategy for invalid SWIFT codes
invalid_swift_codes = st.text(min_size=1, max_size=20).filter(
    lambda x: not (len(x) in {8, 11} and all(c.isalnum() for c in x))
)


# Test cases for valid SWIFT codes
@settings(max_examples=10)
@given(swift_code=valid_swift_codes)
def test_valid_swift_codes(swift_code):
    instance = SwiftCode(code=swift_code)
    assert instance.code == swift_code


# Test cases for invalid SWIFT codes
@settings(max_examples=10)
@given(swift_code=invalid_swift_codes)
def test_invalid_swift_codes(swift_code):
    with pytest.raises(ValidationError):
        SwiftCode(code=swift_code)


# Test case for case insensitivity
def test_case_insensitivity():
    swift_code = "abCDEF12"
    instance = SwiftCode(code=swift_code, case_sensitive=False)
    assert instance.code == "ABCDEF12"  # Should convert to uppercase


# Test case for whitespace stripping
def test_strip_whitespace():
    swift_code = "  ABCDEF12  "
    instance = SwiftCode(code=swift_code, strip_whitespace=True)
    assert instance.code == "ABCDEF12"


# Test case for default behavior (case-sensitive and no whitespace stripping)
def test_default_behavior():
    swift_code = "ABCDEF12"
    instance = SwiftCode(code=swift_code)
    assert instance.code == swift_code


# Test for length errors
@pytest.mark.parametrize("swift_code", ["ABC", "ABCDEFGH12", "ABCDEFGHIJKLMNOP"])
def test_length_errors(swift_code):
    with pytest.raises(ValidationError):
        SwiftCode(code=swift_code)


# Test for invalid characters
@pytest.mark.parametrize("swift_code", ["ABC123!!", "12345678", "A!@#$%^&*()"])
def test_invalid_characters(swift_code):
    with pytest.raises(ValidationError):
        SwiftCode(code=swift_code)


# Test for None value in SWIFT code
def test_none_value():
    with pytest.raises(ValidationError):
        SwiftCode(code=None)
