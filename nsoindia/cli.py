"""
nsoindia CLI — command-line interface for the MoSPI data portal.

Usage:
    nsoindia list-datasets
    nsoindia get-indicators --dataset PLFS
    nsoindia get-metadata   --dataset PLFS --indicator-code 1
    nsoindia get-data       --dataset PLFS --filters '{"indicator_code":1,"year":"2022-23"}'

    # Or equivalently via python -m:
    python -m nsoindia list-datasets
"""

import argparse
import json
import sys

import nsoindia


def _dump(obj):
    """Pretty-print any object as JSON to stdout."""
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def _error(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_list_datasets(_args):
    result = nsoindia.list_datasets(format="dict")
    _dump(result)


def cmd_get_indicators(args):
    if not args.dataset:
        _error("--dataset is required for get-indicators")
    result = nsoindia.get_indicators(dataset=args.dataset, format="dict")
    _dump(result)


def cmd_get_metadata(args):
    if not args.dataset:
        _error("--dataset is required for get-metadata")

    # Parse optional integer flags
    def _opt_int(val):
        if val is None:
            return None
        try:
            return int(val)
        except ValueError:
            _error(f"Expected an integer, got: {val!r}")

    result = nsoindia.get_metadata(
        dataset=args.dataset,
        indicator_code=_opt_int(args.indicator_code),
        base_year=args.base_year,
        level=args.level,
        frequency=args.frequency,
        classification_year=args.classification_year,
        frequency_code=_opt_int(args.frequency_code),
        series=args.series,
        use_of_energy_balance_code=_opt_int(args.use_of_energy_balance_code),
        sub_indicator_code=_opt_int(args.sub_indicator_code),
        format="dict",
    )
    _dump(result)


def cmd_get_data(args):
    if not args.dataset:
        _error("--dataset is required for get-data")
    if not args.filters:
        _error("--filters is required for get-data (pass a JSON string)")

    try:
        filters = json.loads(args.filters)
    except json.JSONDecodeError as exc:
        _error(f"--filters must be valid JSON: {exc}")

    result = nsoindia.get_data(dataset=args.dataset, filters=filters, format="dict")
    _dump(result)


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nsoindia",
        description=(
            "CLI for India's National Statistical Office (MoSPI) data portal.\n\n"
            "4-step workflow:\n"
            "  1. nsoindia list-datasets\n"
            "  2. nsoindia get-indicators --dataset <NAME>\n"
            "  3. nsoindia get-metadata   --dataset <NAME> [filter options]\n"
            "  4. nsoindia get-data       --dataset <NAME> --filters '{...}'\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"nsoindia {nsoindia.__version__}"
    )

    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # ---- list-datasets ----
    sub.add_parser(
        "list-datasets",
        help="List all available MoSPI datasets (Step 1)",
        description="Returns an overview of all 19 MoSPI statistical datasets.",
    )

    # ---- get-indicators ----
    p_ind = sub.add_parser(
        "get-indicators",
        help="List indicators for a dataset (Step 2)",
        description="Returns available indicators for the given dataset.",
    )
    p_ind.add_argument("--dataset", required=True, metavar="NAME",
                       help="Dataset name, e.g. PLFS, CPI, IIP, NAS …")

    # ---- get-metadata ----
    p_meta = sub.add_parser(
        "get-metadata",
        help="Get valid filter values for a dataset/indicator (Step 3)",
        description="Returns valid filter values (states, years, quarters, etc.).",
    )
    p_meta.add_argument("--dataset", required=True, metavar="NAME")
    p_meta.add_argument("--indicator-code", dest="indicator_code", metavar="INT",
                        help="Indicator code (required for most datasets)")
    p_meta.add_argument("--base-year", dest="base_year", metavar="STR",
                        help="Base year — required for CPI, IIP, NAS")
    p_meta.add_argument("--level", metavar="STR",
                        help="CPI level: Group or Item")
    p_meta.add_argument("--frequency", metavar="STR",
                        help="IIP frequency: Annually or Monthly")
    p_meta.add_argument("--classification-year", dest="classification_year", metavar="STR",
                        help="ASI classification year")
    p_meta.add_argument("--frequency-code", dest="frequency_code", metavar="INT",
                        help="Frequency code (PLFS, ASUSE)")
    p_meta.add_argument("--series", metavar="STR",
                        help="Series: Current or Back (CPI, NAS)")
    p_meta.add_argument("--use-of-energy-balance-code", dest="use_of_energy_balance_code",
                        metavar="INT", help="ENERGY: 1=Supply, 2=Consumption")
    p_meta.add_argument("--sub-indicator-code", dest="sub_indicator_code", metavar="INT",
                        help="Sub-indicator code (RBI)")

    # ---- get-data ----
    p_data = sub.add_parser(
        "get-data",
        help="Fetch statistical data (Step 4)",
        description="Fetches statistical data. Use filter values from get-metadata.",
    )
    p_data.add_argument("--dataset", required=True, metavar="NAME")
    p_data.add_argument(
        "--filters", required=True, metavar="JSON",
        help='Filters as a JSON string, e.g. \'{"indicator_code":1,"year":"2022-23"}\'',
    )

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

COMMAND_MAP = {
    "list-datasets": cmd_list_datasets,
    "get-indicators": cmd_get_indicators,
    "get-metadata": cmd_get_metadata,
    "get-data": cmd_get_data,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    handler = COMMAND_MAP.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    try:
        handler(args)
    except Exception as exc:  # noqa: BLE001
        _error(str(exc))


if __name__ == "__main__":
    main()
