import os
from pathlib import Path
from typing import Any
import yaml
from typing import Any, Type, TypeVar
from dataclasses import is_dataclass

T = TypeVar("T")

def read_yml(path_or_stream: str) -> Any:
    if not is_path_valid(path_or_stream):
        yml = yaml.safe_load(path_or_stream)
        return yml
    
    if os.path.exists(path_or_stream):
        with open(path_or_stream, "r") as stream:
            yml = yaml.safe_load(stream)
        return yml
    else:
        raise FileNotFoundError(f"Given path: {path_or_stream} does not exist!")

def parse_yml(cls: Type[T], to_parse: list[dict[Any, Any]]) -> list[T]:
    if not is_dataclass(cls):
        raise TypeError(f"{cls} must be a dataclass")
    print(type(to_parse))
    return [cls(**item) for item in to_parse]

def is_path_valid(path: str) -> bool:
    try:
        p = Path(path)
        p.resolve(strict=True)
        return True
    except Exception:
        return False
    