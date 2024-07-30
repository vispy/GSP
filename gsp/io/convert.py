# Package: Graphic Server Protocol / Matplotlib
# Authors: Nicolas P .Rougier <nicolas.rougier@inria.fr>
# License: BSD 3 clause
import numpy as np

# Registered converters with keys equal to (src_type, dst_type)
converters = {}


class Converter:
    """This class is used to postpone the conversion of a parameter of
    a command.

    This allows to writes function with types compatible with the
    required type while the actual conversion to the required type
    will be done just in time (depending on the convert flag). This is
    necessary to avoid passing large data from one function to the
    other. For example, numpy arrays ca be kept as such and converted
    to bytes only when it is needed by the protocol (dump functions).

    """

    def __init__(self, converter, value):
        self.converter = converter
        self.value = value

    def __call__(self):
        return self.converter(self.value)


def unregister(src_types, dst_type):
    """
    Unregister converters from `src_type`  to `dst_type`

    Parameters
    ----------
    src_types: string or tuple of strings
        Source type ("*" means any type)

    dst_type: string
        Destination type

    Usage example
    -------------

    unregister("*", "int")
    """

    if isinstance(src_types,(list,tuple)):
        for src_type in src_types:
            if (src_type,dst_type) in converters.keys():
                del converters[(src_type, dst_type)]
    else:
        src_type = src_types
        if (src_type,dst_type) in converters.keys():
            del converters[(src_type, dst_type)]


def register(src_types, dst_type):
    """
    Function decorator that registers a converter from `src_type`
    to `dst_type`

    Parameters
    ----------
    src_types: string or tuple of strings
        Source type ("*" means any type)

    dst_type: string
        Destination type

    Usage example
    -------------

    @register("*", "int")
    def any_to_int(value):
        return int(value)
    convert(4.5, "int)
    """

    def inner(func):
        if isinstance(src_types,(list,tuple)):
            for src_type in src_types:
                if (src_type,dst_type) not in converters.keys():
                    converters[(src_type, dst_type)] = func
                else:
                    raise TypeError(
                        f"A converter for '{src_type}' to '{dst_type}' has already been registered.")
        else:
            src_type = src_types
            if (src_type,dst_type) not in converters.keys():
                converters[(src_type, dst_type)] = func
            else:
                raise TypeError(
                    f"A converter for '{src_type}' to '{dst_type}' has already been registered.")

        return func
    return inner


def is_registered(src_type, dst_type):
    """
    Check if a converter from `src_type` to `dst_type` has been
    registered.
    """

    return (converters.get((src_type, dst_type), None)
            or converters.get(("*", dst_type), None))


def get_converter(value, dst_type):
    """
    Get a converter to convert value to dst_type.

    Parameters
    ----------

    value: type, str or any object
         Source value or type

     dst_type: str
         Destination type

    Return
    ------

    A convert function or None
    """

    # Get source type
    src_type = None
    if isinstance(value, type):
        src_type = value.__name__
    else:
        if isinstance(value, str) and is_registered(value, dst_type):
            src_type = value
        else:
            src_type = type(value).__name__

    # Get dst type
    if isinstance(dst_type, type):
        dst_type = dst_type.__name__
    elif not isinstance(dst_type, str):
        raise ValueError("dst_type must be a type or a string")

    # Get direct converter
    converter = is_registered(src_type, dst_type)
    if converter:
        return converter

    # Get converter from bases
    for base in value.__class__.__bases__:
        src_type = base.__name__
        converter = is_registered(src_type, dst_type)
        if converter:
            return converter

    return None


def convert(value, dst_type):
    """
    Convert value to dst_type is there exists a converter

    Parameters
    ----------

    value: any type
         Source value

     dst_type: str
         Destination type
    """

    try:
        return get_converter(value, dst_type)(value)
    except:
        src_type = value.__class__.__name__
        raise ValueError(f"No converter found for converting '{value}' ({src_type}) to '{dst_type}'.")


@register("dtype", "str")
def numpy_dtype_to_str(dt):
    if dt.names:
        elements = []
        for name in dt.names:
            size = int(np.prod(dt[name].shape))
            type = dt[name].base.str
            elements.append (f"{type}:{name}:{size}")
        return ",".join(elements)
    else:
        size = int(np.prod(dt.shape))
        type = dt.base.str
        return f"{type}::{size}"

@register("str", "dtype")
def numpy_str_to_dtype(desc):
    dt = []
    elements = desc.split(",")
    for element in elements:
        type,name,size = element.split(":")
        if name :
            if size and int(size) > 1:
                dt.append((name, type, int(size)))
            else:
                dt.append((name, type))
        else:
            if size and int(size) > 1:
                dt.append((type, int(size)))
            else:
                dt.append(type)
    if len(dt) == 1 and not len(name):
        dt = dt[0]
    return np.dtype(dt)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    from numpy import dtype

    Z = np.zeros(3)
    # convert(4.5, str)

    dtype_str = convert(Z.dtype, "str")
    print(Z.dtype)
    print(convert(Z.dtype, "str"))
    print(convert(convert(Z.dtype, "str"), dtype))

    print("Known converters")
    for converter in converters:
        print(" -", converter)
