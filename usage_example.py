
# Import
from littlecsv import CSV

# Read from file
dataset = CSV.read(
    "./data_sample.csv",
    sep=",", # default is sep=","
    col_types={"DDG": float, "RSA*LOR": float}, # optional type conversions, by default all is string
    col_default={"DDG": 0.0}, # optional in case type conversions fails
)

# Show a summary table of data
dataset.show()

# Or create a new DataFrame
friends = CSV(["name", "age"], sep=";", name="friends")
friends.add_entry({"name": "Alice", "age": 30})
friends.add_entry({"name": "Bob", "age": 28})
friends.show()

# Access colums
ddg_array = dataset.get_col("DDG", dtype=float, as_numpy=True)

# But if any conversion fails, this will lead to an error
dataset.entries[3]["DG"] = "unknown_value"
#dg_array = dataset.get_col("DG", dtype=float) # -> ERROR
dg_array = dataset.get_col("DG") # so you can just avoid conversion
dg_array = dataset.get_col("DG", dtype=float, default_value=0.0) # or provide a default fallback value

# Access numpy matrices in the dataset
X = dataset.get_X(["RSA", "LOR", "RSA*LOR"])
y = dataset.get_y("DDG")
print(X.shape, y.shape)

# Filter entries
dataset.filter(lambda e: e["DDG"] < -1.0, do_print=True, filter_name="Only stabilizing DDG")

# Loop on entries (which are just dictionaries {header_property => entry_value})
for entry in dataset:
    mutation = entry["mutation_fasta"]
    DDG = entry["DDG"]
    print(f" * stabilizing mutation '{mutation}': DDG = {DDG:.3f}")

# Manimulate data by direct access
for entry in dataset:
    entry["sec_str"] = entry["sec_str"].replace("X", "Loop").replace("A", "Alpha").replace("B", "Beta")

# Manipulate data with methods
dataset.set_sep("\t")
dataset.remove_col("mutation_pdb")
dataset.remove_col("mutation_msa")
dataset.rename_col("mutation_fasta", "mutation")
dataset.add_col("DDG_squared", dataset.get_col("DDG", float, as_numpy=True)**2)
dataset.order_header(["mutation", "DDG", "RSA*LOR"])

# Group by some properties
groups_by_sec_str = dataset.get_groups(["sec_str"])
for sec_str, entries in groups_by_sec_str.items():
    print(f" * {sec_str}: {len(entries)} mutations")

# Let us see all the changed
dataset.show()

# Write
dataset.write("./data_sample_modified.csv")
