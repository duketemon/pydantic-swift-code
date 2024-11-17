import pytest
from pydantic_swift_code import SwiftCode
from pydantic import BaseModel, ValidationError


class BankAccount(BaseModel):
    swift_code: SwiftCode


@pytest.mark.parametrize(
    ids=(
        "full format (11 chars)",
        "short format (8 chars)",
        "leading spaces",
        "trailing spaces",
        "spaces around",
    ),
    argvalues=(
        "BARCGB5GXXX",
        "REVOPTP2",
        "       CITITHBXIBF",
        "BOFAUS3N          ",
        "   BOPIPHMMXXX    ",
    ),
    argnames="code",
)
def test_success(code):
    # When
    account = BankAccount(swift_code=code)

    # Then
    assert account.swift_code == code.strip()


@pytest.mark.parametrize(
    ids=(
        "too long",
        "uncompleted",
        "lower case",
        "mix case",
        "starts with number",
    ),
    argvalues=(
        ("BARCGB5GXXXXXXXXXXX", "String should have at most 11 characters"),
        ("REVOIT", "String should have at least 8 characters"),
        ("bagage22bog", "String should match pattern"),
        ("ISBKTRISxxx", "String should match pattern"),
        ("8CMRMXMMXXX", "String should match pattern"),
    ),
    argnames="code, error_msg",
)
def test_validation_error(code, error_msg):
    with pytest.raises(ValidationError) as error:
        # When
        BankAccount(swift_code=code)
    # Then
    assert error_msg in str(error)

