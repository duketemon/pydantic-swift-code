## Overview
Micro-package that defines a SWIFT/BIC code type using the Pydantic package

## Installation
Install from PyPI
```commandline
pip install pydantic-swift-code
```
Install from GitHub
```commandline
pip install git@github.com:duketemon/pydantic-swift-code.git
```

## Usage
```python
from pydantic import BaseModel, field_validator
from pydantic_swift_code import SwiftCode

class BankAccount(BaseModel):
    ...
    swift_code: SwiftCode

    @field_validator("swift_code", mode="after")
    @classmethod
    def validate_swift_code_after_init(cls, swift_code: str) -> str:
        """Custom validation"""
        
        if swift_code[:4] not in {"REVO", "MONZ"}:
            raise ValueError("Only Revolut and Monzo swift codes are allowed")
        
        if swift_code[4:6] not in {"US", "GB"}:
            raise ValueError("Only GB and US swift codes are allowed")
        
        return swift_code
```
