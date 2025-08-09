
# Imports ----------------------------------------------------------------------
from typing import List, Type, TypeVar
from numbers import Number


# Initialization ---------------------------------------------------------------
T = TypeVar('T')         # Generic type variable (to type output of python functions)
_no_default = object()   # Default argument values for cases when default fallback is forbidden


# Type conversion --------------------------------------------------------------
def _convert_to_type(
        input_object,
        dtype: Type[T],
        default_value,
    ) -> T:
    """Return converted `input_object` to type `dtype` or `default_value` if conversion failed and `default_value` is allowed."""
    try:
        return dtype(input_object)
    except:
        if default_value is _no_default:
            obj_str = str(input_object)
            MAX_CHAR = 30
            if len(obj_str) > MAX_CHAR:
                obj_str = obj_str[0:MAX_CHAR] + "..."
            raise ValueError(f"\033[91mERROR\033[0m in littlecsv::_convert_to_type(): failed to convert object '{obj_str}' to type {dtype}.")
        else:
            return default_value


# Logs -------------------------------------------------------------------------
def _stringify(
        input_object,
        round_digit: int=4
    ) -> str:
    """Return stringified `input_object` (if input is a float, first it rounds the values)."""
    if isinstance(input_object, float):
        input_str = f"{input_object:.{round_digit}f}"
        if input_str[0] != "-":
            input_str = " " + input_str
        return input_str
    return str(input_object)
    
def _format_string(
        input_object,
        size: int=20,
        filler: str=" ",
        dots_str: str="...",
        round_digit: int=4
    ) -> str:
    """Format `input_object` to a standardized string form."""
    shift_to_right = isinstance(input_object, Number)
    input_str = _stringify(input_object, round_digit=round_digit)
    if len(input_str) > size:
        return input_str[:size-len(dots_str)] + dots_str
    else:
        if shift_to_right:
            return filler*(size - len(input_str)) + input_str
        return input_str + filler*(size - len(input_str))

def _format_line(
        line_list: list,
        sizes_list: List[int],
        sep: str,
        round_digit: int=4,
        do_highlight: bool=False,
    ) -> str:
    """Format the list of objects `line_list` (representing a line in a table) to a standardized string form."""

    # Construct line_list_str
    line_list_str = [
        _format_string(element, size=size, round_digit=round_digit)
        for element, size in zip(line_list, sizes_list)
    ]

    # Highlights
    if do_highlight:
        line_list_str = [f"\033[92m{el}\033[0m" if el != "..." else el for el in line_list_str]

    # Post-process and return
    line_str = sep[1:] + sep.join(line_list_str) + sep[:-1]
    return line_str