

# Imports ----------------------------------------------------------------------
from typing import List, Set


# Header -----------------------------------------------------------------------
class Header:
    """
    Container Class for the Header of a CSV object.
        * ordered list with no repetitions allowed and a separator of length = 1.
    """

    # Constructor --------------------------------------------------------------
    def __init__(self, properties: List[str], sep: str):

        # Init
        self._sep = ""
        self._properties: List[str] = []
        self._properties_set: Set[str] = set()

        # Set header values
        self.set_sep(sep)
        for property in properties:
            self.add(property)

    # Basic properties ---------------------------------------------------------
    def __getitem__(self, id: int) -> str:
        return self._properties[id]

    def __iter__(self):
        return iter(self._properties)
    
    def __contains__(self, property_name: str) -> bool:
        return property_name in self._properties_set

    def __len__(self) -> int:
        return len(self._properties)
    
    def __str__(self) -> str:
        return f"Header(l={len(self)})"
    
    @property
    def _error_str(self) -> str:
        return f"\033[91mERROR\033[0m in littlecsv::{self}"

    def properies(self) -> List[str]:
        """Return list of Header's properties (as a copy)."""
        return [prop for prop in self._properties]
    
    # Methods ------------------------------------------------------------------
    def set_sep(self, sep: str) -> "Header":
        """Set separator (like sep=',' or sep=';'). O[1]"""
        assert isinstance(sep, str) and len(sep) == 1, f"{self._error_str}.set_sep(): sep='{sep}' should be a string of length 1."
        self._sep = sep
        return self

    def add(self, property_name: str) -> "Header":
        """Add a new property to Header. O[1]"""
        assert property_name not in self._properties_set, f"{self._error_str}.add('{property_name}'): property already exists."
        self._properties.append(property_name)
        self._properties_set.add(property_name)
        return self

    def remove(self, property_name: str) -> "Header":
        """Remove an existing property to Header. O[n]"""
        assert property_name in self._properties_set, f"{self._error_str}.remove('{property_name}'): property does not exists."
        self._properties.remove(property_name)
        self._properties_set.remove(property_name)
        return self

    def rename(self, property_old: str, property_new: str) -> "Header":
        """Rename an existing property to Header. O[n]"""
        assert property_old != property_new, f"{self._error_str}.rename(): old property and new property have the same value '{property_old}'."
        assert property_old in self._properties_set, f"{self._error_str}.rename(): old property '{property_old}' is not in header."
        assert property_new not in self._properties_set, f"{self._error_str}.rename(): new property '{property_new}' already in header."
        id = self._properties.index(property_old)
        self._properties[id] = property_new
        self._properties_set.add(property_new)
        self._properties_set.remove(property_old)
        return self

    def order(self, header_order: List[str]) -> "Header":
        """Order first appearing properties in Header. O[n]"""
        for property in header_order:
            assert property in self, f"{self._error_str}.order(): property '{property}' not in header."
        ordered_properties_set = set(header_order)
        assert len(header_order) == len(ordered_properties_set), f"{self._error_str}.order(): header_order contain some redundancies."
        unordered_properties = [property for property in self if property not in ordered_properties_set]
        self._properties = header_order + unordered_properties
        return self
    
    def copy(self) -> "Header":
        """Copy Header object. O[n]"""
        return Header([p for p in self], self._sep)
