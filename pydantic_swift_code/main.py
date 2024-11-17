from typing import Annotated

from pydantic.types import StringConstraints

SwiftCode = Annotated[
    str,
    StringConstraints(
        min_length=8,
        max_length=11,
        strip_whitespace=True,
        # 4x Bank code, 2x Country code, 2x Location code, 3x Branch code
        pattern=r"^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$",
    ),
]
