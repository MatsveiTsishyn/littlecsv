

# Imports ----------------------------------------------------------------------
import os.path
import csv
from typing import Union, Tuple, List, Dict, Callable, Any
import numpy as np
from littlecsv.header import Header
from littlecsv.utils import _convert_to_type, _stringify, _format_line, _no_default


# Main -------------------------------------------------------------------------
class CSV:
    """
    Class to read, write and manage CSV files ('.csv') as a DataFrame.
        * Entries are just dictionary {header_property => entry_value}
        * Provide only basic maipulation functions like 'add_col' / 'remove_col', ...
        * Never assumes a column or a cell type except when it is explicitely specified (all cells are ::str by default).
        * Strict on format: no redundant columns in header and each line must have the same number of elements
    """

    # Constants ----------------------------------------------------------------
    ALLOWED_EXTENTIONS = ["csv", "tsv"]
    _error_str_class = f"\033[91mERROR\033[0m in littlecsv::CSV"

    # Constructor --------------------------------------------------------------
    def __init__(
            self,
            header: List[str]=[],
            sep: str=",",
            name: str="DataFrame",
            ignore_warnings: bool=False,
        ):
        """Create a new empty DataFrame (no entries) with a defined header."""

        # Base properties
        self.name = name
        self.ignore_warnings = ignore_warnings

        # Content
        self._header = Header(header, sep)
        self.entries: List[dict] = []

    @classmethod
    def read(
            cls,
            input_path: str,
            sep: str=",",
            name: Union[None, str]=None,
            ignore_warnings: bool=False,
            col_types: Dict[str, type]={},
            col_default: Dict[str, Any]={},
        ) -> "CSV":
        """Read CSV object from a '.csv' file."""

        # Guardians
        assert any([input_path.endswith(f".{extention}")] for extention in cls.ALLOWED_EXTENTIONS), f"{cls._error_str_class}: extention sould be among {cls.ALLOWED_EXTENTIONS}."
        assert os.path.isfile(input_path), f"{cls._error_str_class}: input_path='{input_path}' file does not exists."

        # Set name
        file_name = os.path.basename(input_path)
        if name is None:
            name = file_name
            for extention in cls.ALLOWED_EXTENTIONS:
                if file_name.endswith(f".{extention}"):
                    name = name.removesuffix(f".{extention}")
                    break

        # Parse csv from file
        with open(input_path, newline='') as csvfile:
            csv_lines = list(csv.reader(csvfile, delimiter=sep))

        # Init CSV object
        header = csv_lines[0]
        output_csv = CSV(header, sep=sep, name=name, ignore_warnings=ignore_warnings)

        # WARNING: separator might be incorrect
        if len(header) <= 1 and len("".join(header)) > 10:
            MAX_CHAR_HEADER = 40
            header_str = ", ".join([f'"{prop}"' for prop in header])
            if len(header_str) > MAX_CHAR_HEADER:
                header_str = header_str[:MAX_CHAR_HEADER] + "..."
            output_csv.log_warning(f".read('{input_path}'): header contains only 1 colums: '{header_str}'!\n -> Separator sep='{sep}' parameter might be incorrect.")

        # Set CSV entries
        for i, line in enumerate(csv_lines[1:]):
            assert len(line) == len(header), f"{cls._error_str_class}.read('{input_path}'): number of elements ({len(line)}) in entry ({i+1}/{len(csv_lines)-1}) does not match the header length ({len(header)})."
            output_csv.entries.append({prop: value for prop, value in zip(header, line)})

        # Set column types if required
        for col_name, dtype in col_types.items():
            col_default_value = col_default.get(col_name, _no_default)
            output_csv.set_col_type(col_name, dtype, default_value=col_default_value)

        return output_csv

    # Basic properties ---------------------------------------------------------
    @property
    def sep(self) -> str:
        """Return CSV separator."""
        return self._header._sep

    def __len__(self) -> int:
        """Number of entries in CSV."""
        return len(self.entries)
    
    def __contains__(self, property_name: str) -> bool:
        """Return if CSV contain `property_name` in header."""
        return property_name in self._header
    
    def __getitem__(self, id: int) -> dict:
        """Get entry at index `id`."""
        return self.entries[id]
    
    def __iter__(self):
        """Loop on entries"""
        return iter(self.entries)
    
    @property
    def n_rows(self) -> int:
        return len(self.entries)
    
    @property
    def n_cols(self) -> int:
        return len(self._header)
    
    @property
    def df_shape(self) -> Tuple[int, int]:
        return (self.n_rows, self.n_cols)
    
    @property
    def df_size(self) -> int:
        """Returns n_rows * n_cols."""
        return self.n_rows * self.n_cols
    
    def header(self) -> List[str]:
        """Return list of Header properties."""
        return self._header.properies()

    def __str__(self) -> str:
        return f"\033[92mCSV\033[0m('{self.name}', n_rows={self.n_rows}, n_cols={self.n_cols})"
    
    @property
    def _error_str(self) -> str:
        return f"\033[91mERROR\033[0m in littlecsv::{self}"
    
    def log_warning(self, warning_str: str="") -> None:
        """Log a Warning."""
        if not self.ignore_warnings:
            print(f"\033[93mWARNING\033[0m in littlecsv::{self}{warning_str}")

    # Mutation Methods ---------------------------------------------------------
    def set_sep(self, sep: str) -> "CSV":
        """Set separator for CSV."""
        self._header.set_sep(sep)
        return self

    def add_entry(self, input_entry: dict) -> "CSV":
        """Copy (but not deepcopy) `input_entry` dictionary and add it as an entry to CSV."""
        entry = {prop: input_entry[prop] for prop in self._header}
        self.entries.append(entry)
        return self

    def add_entries(self, entries: List[dict]) -> "CSV":
        """Copy (but not deepcopy) each `input_entry` dictionary from `entries` and them as an entries to CSV."""
        for entry in entries:
            self.add_entry(entry)
        return self

    def add_col(self, property: str, values: list, allow_replacement: bool=False) -> "CSV":
        """Add column named `property` with values `values` to CSV."""
        if not allow_replacement:
            assert property not in self._header, f"{self._error_str}.add_col(): property='{property}' already exists and `allow_replacement` is set to False."
        if property not in self._header:
            self._header.add(property)
        assert len(values) == len(self), f"{self._error_str}.add_col(): values length ({len(values)}) != CSV length ({len(self)})."
        for entry, value in zip(self.entries, values):
            entry[property] = value
        return self
    
    def add_empty_col(self, property: str, default_value: str="XXX", allow_replacement: bool=False) -> "CSV":
        """Add column named `property` with values all as `default_value` to CSV."""
        values = [default_value for _ in self.entries]
        self.add_col(property, values, allow_replacement=allow_replacement)
        return self
    
    def remove_col(self, property: str) -> "CSV":
        """Remove an existing CSV column."""
        self._header.remove(property)
        for entry in self.entries:
            del entry[property]
        return self

    def rename_col(self, property_old: str, property_new: str) -> "CSV":
        """Rename an existing CSV colums"""
        self._header.rename(property_old, property_new)
        for entry in self.entries:
            entry[property_new] = entry[property_old]
            del entry[property_old]
        return self

    def order_header(self, header_order: List[str]) -> "CSV":
        """
        Order properties in columns as specified in `header_order`.
            - `header_order` must contain only values that are existing columns in CSV
            - column names that are in CSV but not in `header_order` will appear after all properties from `header_order`
        """
        self._header.order(header_order)
        return self
    
    def filter(self, keep_entry_function: Callable, do_print: bool=False, filter_name: str="") -> "CSV":
        """Filter entries in CSV with a keep_entry_function."""
        l1 = len(self)
        self.entries = [entry for entry in self.entries if keep_entry_function(entry)]
        l2 = len(self)
        if do_print:
            print(f"{self}: Filter('{filter_name}'): {l1} -> {l2}")
        return self
    
    def set_col_type(self, property_name: str, dtype: type, default_value=_no_default) -> "CSV":
        """Set all values of columns `property_name` to type `dtype`."""
        assert property_name in self._header, f"{self._error_str}.set_col_type(): property_name='{property_name}' does not exists."
        for entry in self.entries:
            entry[property_name] = _convert_to_type(entry[property_name], dtype, default_value)
        return self
    
    # Get Methods --------------------------------------------------------------
    def get_col(self, property: str, dtype: Union[None, type]=None, default_value=_no_default, as_numpy: bool=False):
        """Get a column of CSV as array."""
        assert property in self, f"{self._error_str}.get_array('{property}'): property does not exists."
        col_list = [entry[property] for entry in self.entries]
        if dtype is not None:
            col_list = [_convert_to_type(el, dtype, default_value=default_value) for el in col_list]
        if as_numpy:
            col_list = np.array(col_list)
        return col_list
    
    def get_row(self, id: int, dtype: Union[None, type]=None, default_value=_no_default, as_numpy: bool=False):
        """Get Raw of CSV as array"""
        entry = self[id]
        row_list = [entry[p] for p in self._header]
        if dtype is not None:
            row_list = [_convert_to_type(el, dtype, default_value=default_value) for el in row_list]
        if as_numpy:
            row_list = np.array(row_list)
        return row_list
    
    def get_X(self, features: List[str]) -> np.ndarray:
        """Get features matrix X (numpy) from the CSV."""
        for feature in features:
            assert feature in self, f"{self._error_str}.get_X(): feature='{feature}' does not exists."
        return np.array([
            [float(entry[feature]) for feature in features]
            for entry in self.entries
        ])
    
    def get_y(self, label: str) -> np.ndarray:
        """Get label array y (numpy) from the CSV."""
        assert label in self, f"{self._error_str}.get_y(): label='{label}' does not exists."
        return np.array([float(entry[label]) for entry in self.entries])
    
    def get_Xy(self, features: List[str], label: str) -> Tuple[np.ndarray, np.ndarray]:
        """Get (features, label) tuple (X, y) (numpy) from the CSV."""
        return self.get_X(features), self.get_y(label)
    
    @staticmethod
    def get_entry_hash(entry: dict, hash_properties: List[str], sep: str="_") -> str:
        """Hash an entry (to string) by values of its hash_properties."""
        return sep.join([entry[prop] for prop in hash_properties])

    def get_map(self, hash_properties: List[str], sep: str="_", map_function: Union[None, Callable]=None) -> Dict[str, Dict]:
        """
        Obtain a map {hash(entry) -> entry} from CSV (redundencies not allowed).
            * if map_function is set, values of the map are defined as map_function(entry)
        """
        for property in hash_properties:
            assert property in self, f"{self._error_str}.get_map(): property='{property}' not in header."
        entries_map: Dict[str, Dict] = {}
        for entry in self.entries:
            h = self.get_entry_hash(entry, hash_properties, sep=sep)
            assert h not in entries_map, f"{self._error_str}.to_map({hash_properties}) redundency found for '{h}'."
            entries_map[h] = entry
        if map_function is not None:
            for h, entry in entries_map.items():
                entries_map[h] = map_function(entry)
        return entries_map

    def get_groups(self, hash_properties: List[str], sep: str="_", map_function: Union[None, Callable]=None) -> Dict[str, List[Dict]]:
        """
        Obtain a map for groups {hash(entry) -> [entries_list]} from CSV.
            * if map_function is set, values of the map are defined as [map_function(entry), ...]
        """
        for property in hash_properties:
            assert property in self, f"{self._error_str}.to_map(): property='{property}' not in header."
        groups_map: Dict[str, List[Dict]] = {}
        for entry in self:
            h = self.get_entry_hash(entry, hash_properties, sep=sep)
            if h not in groups_map:
                groups_map[h] = []
            groups_map[h].append(entry)
        if map_function is not None:
            for h, group in groups_map.items():
                groups_map[h] = [map_function(e) for e in group]
        return groups_map
    
    def copy(self):
        """Copy CSV object."""
        new_csv = CSV()
        new_csv.name = self.name
        new_csv.ignore_warnings = self.ignore_warnings
        new_csv._header = self._header.copy()
        new_csv.entries = [
            {k: v for k, v in entry.items()}
            for entry in self.entries
        ]
        return new_csv
    
    def show(self, n_entries: int=10, max_col_length: int=20, max_line_length: int=200, round_digit: int=4, sep: str=" | ") -> None:

        # Init
        dots = "..."
        n_columns = len(self._header)
        len_sep = len(sep)
        len_dots = len(dots)

        # Overwrite extreme input parameters to avoid degenerated logs
        n_entries = max(n_entries, 3)
        min_col_length = 3
        max_col_length = max(max_col_length, 3)
        max_line_length = max(max_line_length, len_sep + max_col_length + len_sep + len_dots + len_sep)

        # Init show table
        table = []
        header_line = [_stringify(prop) for prop in self.header()]
        table.append(header_line)
        if n_entries >= len(self): # Case: all lines are displayed
            for id in range(len(self)):
                table.append([_stringify(val, round_digit=round_digit) for val in self.get_row(id)])
        else: # Case: some lines are not displayed (to log '...' line and last line at the end)
            for id in range(n_entries - 2):
                table.append([_stringify(val, round_digit=round_digit) for val in self.get_row(id)])
            table.append([dots for _ in range(n_columns)])
            table.append([_stringify(val, round_digit=round_digit) for val in self.get_row(-1)])

        # Compute columns sized
        len_current = len_sep - 1
        columns_length_arr: List[str] = []
        are_hidden_columns = False
        for n_col in range(n_columns):
            columns_values = [line[n_col] for line in table]
            column_length = max([len(val) for val in columns_values]) # maximal cell length in ths columns
            column_length = min(column_length, max_col_length) # set ceil to col length
            column_length = max(column_length, min_col_length) # set floor to col length
            len_current += column_length + len_sep
            if len_current + len_dots + (len_sep - 1) > max_line_length:
                are_hidden_columns = True
                columns_length_arr.append(len_dots)
                break
            columns_length_arr.append(column_length)
        
        # Crop table if all columns can not be displayed
        if are_hidden_columns:
            for line_i, line in enumerate(table):
                table[line_i] = line[0:len(columns_length_arr)-1] + [dots]

        # Show
        print(self)
        print(_format_line(table[0], columns_length_arr, sep, round_digit=round_digit, do_highlight=True))
        for line in table[1:]:
            print(_format_line(line, columns_length_arr, sep, round_digit=round_digit))
    
    # IO -----------------------------------------------------------------------
    def write(self, output_path: str) -> "CSV":
        """Save CSV to a file at `output_path`."""

        # Guardians
        assert any([output_path.endswith(f".{extention}")] for extention in self.ALLOWED_EXTENTIONS), f"{self._error_str}.write('{output_path}'): extention should be among {CSV.ALLOWED_EXTENTIONS})."
        assert os.path.isdir(os.path.dirname(output_path)), f"{self._error_str}.write('{output_path}'): destination folder does not exists."
        
        # Stringity and write
        with open(output_path, "w", newline="") as csvfile:

            # Init
            writer = csv.writer(csvfile, delimiter=self.sep)
            header_list = self.header()
            
            # Write Header
            writer.writerow(header_list)

            # Write entries
            for entry in self.entries:
                entry_list = [entry[prop] for prop in header_list]
                writer.writerow(entry_list)

        return self