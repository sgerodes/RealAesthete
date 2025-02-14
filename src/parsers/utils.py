from typing import TypeVar, Any
import scrapy

COPY_TO = TypeVar('COPY_TO')


def copy_all_properties(_from: Any, _to: COPY_TO, ignore_nulls=True) -> COPY_TO:
    if isinstance(_from, dict):
        iterable = _from.items()
    else:
        iterable = vars(_from).items()
    for k, v in iterable:
        if ignore_nulls and v is None:
            continue
        if hasattr(_to, k):
            setattr(_to, k, v)
    return _to


def copy_all_properties_from_scrapy_item(_from: scrapy.Item, _to: COPY_TO, ignore_nulls=True) -> COPY_TO:
    return copy_all_properties(_from._values, _to, ignore_nulls)
