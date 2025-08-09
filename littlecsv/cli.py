
# Imports ----------------------------------------------------------------------
import argparse
from littlecsv import CSV


# CLI: show function -----------------------------------------------------------
def show():

    # Define Argument Parser ---------------------------------------------------

    # Init parser
    parser = argparse.ArgumentParser(
        description="Show a summary table of the CSV file at <csv_path>.",
        usage=f"littlecsv_show <csv_path> [options]\nhelp:  littlecsv_show -h",
    )

    parser.add_argument(
        "csv_path", type=str,
        help="path to CSV '.csv' file",
    )

    parser.add_argument(
        "-s", "--sep", type=str, default=",", metavar="",
        help="CSV separator",
    )

    parser.add_argument(
        "-n", "--n_entries", type=int, default=10, metavar="",
        help="number of entries (rows) to show",
    )

    parser.add_argument(
        "-l", "--max_col_length", type=int, default=20, metavar="",
        help="maximum number of character a single column can take",
    )

    parser.add_argument(
        "-L", "--max_line_length", type=int, default=200, metavar="",
        help="maximum number of character a line can take",
    )

    args = parser.parse_args()

    # Execution ----------------------------------------------------------------

    # Read and Show CSV
    data = CSV.read(args.csv_path, sep=args.sep)
    data.show(n_entries=args.n_entries, max_col_length=args.max_col_length, max_line_length=args.max_line_length)
