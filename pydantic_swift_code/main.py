from re import fullmatch
from typing import Set

from pydantic import BaseModel, model_validator


class SwiftCode(BaseModel):
    code: str
    case_sensitive: bool = True
    strip_whitespace: bool = False
    valid_lengths: Set[int] = {8, 11}

    @model_validator(mode="after")
    def model_validation(self):
        # Strip whitespace
        if self.strip_whitespace:
            self.code = self.code.strip()

        # Enforce case sensitivity
        if not self.case_sensitive:
            self.code = self.code.upper()

        # Check length
        if len(self.code) not in self.valid_lengths:
            raise ValueError(f"SWIFT code '{self.code}' should be 8 or 11 characters long")

        # Validate format
        if not fullmatch(r"[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?", self.code):
            raise ValueError(f"Invalid SWIFT code format: '{self.code}'")

        return self
