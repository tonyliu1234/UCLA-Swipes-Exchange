from typing import Any, TypeVar, Callable, Optional

T = TypeVar('T')
U = TypeVar('U')


def some(option: Optional[Any]) -> bool:
    return option is not None


def none(option: Optional[Any]) -> bool:
    return option is None


def map_or(option: Optional[T], f: Callable[[T], U], default: U) -> U:
    return f(option) if option is not None else default


def and_then(option: Optional[T], f: Callable[[T], Optional[U]]) -> Optional[U]:
    return f(option) if option is not None else None


def unwrap(option: Optional[T]) -> T:
    if option is not None:
        return option
    raise TypeError(f"{option} is None")


def unwrap_or(option: Optional[T], default: T) -> T:
    return option if option is not None else default
