"""Command-line interface for censusgeocode"""

# This file is part of censusgeocode.
# https://github.com/fitnr/censusgeocode

# Licensed under the General Public License (version 3)
# http://opensource.org/licenses/LGPL-3.0
# Copyright (c) 2015-2026, Neil Freeman <contact@fakeisthenewreal.org>

import argparse
import csv
import io
import sys

from . import __version__
from .censusgeocode import DEFAULT_BENCHMARK, DEFAULT_VINTAGE, CensusGeocode, DEFAULT_TIMEOUT


def main() -> None:
    """Command-line interface for censusgeocode"""
    parser = argparse.ArgumentParser("censusgeocode", description="Command-line interface for the Census Geocoding API")

    parser.add_argument("-v", "--version", action="version", version="%(prog)s v" + __version__)
    parser.add_argument("address", type=str, nargs="?", default=None)
    parser.add_argument(
        "--csv",
        type=str,
        help=(
            "comma-delimited file of addresses. No header. Must have the following columns: id, street address, city, state, zip. "
            "The id must be a unique. Read from stdin with -"
        ),
    )
    parser.add_argument(
        "--rettype",
        choices=["locations", "geographies"],
        default="locations",
        help=(
            "Query type. Geographies will return state, county, tract, and block code in addition to TIGER/Line info and "
            "latitude and longitude. For use with --csv"
        ),
    )
    parser.add_argument(
        "--benchmark",
        default=DEFAULT_BENCHMARK,
        help="Version of the locator to query. See Census documentation for options.",
    )
    parser.add_argument(
        "--vintage",
        default=DEFAULT_VINTAGE,
        help="Geography version query. See Census documentation for options.",
    )
    parser.add_argument(
        "--timeout",
        metavar="SECONDS",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Request timeout [default: {DEFAULT_TIMEOUT}]",
    )

    args = parser.parse_args()
    cg = CensusGeocode(benchmark=args.benchmark, vintage=args.vintage)

    if args.address:
        search_result = cg.onelineaddress(args.address, returntype=args.rettype, timeout=args.timeout)

        try:
            print("{},{}".format(search_result[0]["coordinates"]["x"], search_result[0]["coordinates"]["y"]))

        except IndexError:
            print(f"Address not found: {args.address}", file=sys.stderr)
            sys.exit(1)

    elif args.csv:
        if args.csv == "-":
            # No streaming here - consume the entirety of stdin.
            infile = io.StringIO()
            csv.writer(infile).writerows(csv.reader(sys.stdin))
            infile.seek(0)

        else:
            infile = args.csv

        csv_result = cg.addressbatch(infile, returntype=args.rettype, timeout=args.timeout)

        fieldnames = cg.batchfields[args.rettype] + ["lat", "lon"]
        fieldnames.pop(fieldnames.index("coordinate"))
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_result)

    else:
        print("Address or csv file required", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
