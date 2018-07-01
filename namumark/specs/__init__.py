from ..elements import Block

_spec_by_element = {}
_block_specs = []


def spec_for(element_cls):
    def decorator(spec_cls):
        if element_cls in _spec_by_element:
            raise ValueError('An element can only have one specification')

        if issubclass(element_cls, Block):
            _block_specs.append(spec_cls)

        _spec_by_element[element_cls] = spec_cls

        return spec_cls

    return decorator


def spec_of(element):
    return _spec_by_element.get(type(element), None)


# Specs should be imported after spec_for
from .specs import *  # noqa: E402

block_specs = tuple(_block_specs)
