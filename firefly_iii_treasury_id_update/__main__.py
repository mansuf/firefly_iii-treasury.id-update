import argparse
import os
import asyncio
import logging
from dotenv import load_dotenv

from . import __description__
from .main import run_main

description = __description__ + (
    ". It is highly recommended to use environments instead of CLI arguments, "
    "to ensure best security practices "
    "(because this app require sensitive information such as: API key to connect to firefly-iii)"
)


def setup_logging(name_module, verbose=False):
    log = logging.getLogger(name_module)
    handler = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(fmt)
    log.addHandler(handler)
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log


def execute_cli_main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--transaction-id", help="firefly-iii transaction id")
    parser.add_argument(
        "--api-key",
        help=(
            "firefly-iii personal access token, "
            "you can check this tutorial https://docs.firefly-iii.org/how-to/firefly-iii/features/api/#personal-access-tokens"
            "how to get personal access token"
        ),
    )
    parser.add_argument("--url", help="firefly-iii base url")
    parser.add_argument(
        "--grams-gold",
        help=(
            "Tell the app how much gold you have (in grams). "
            "Value can be a URL (local or remote file) or a harcoded numbers"
        ),
    )
    parser.add_argument("--verbose", help="Enable verbose logging", action="store_true")
    parser.add_argument(
        "--load-dotenv",
        help="Load required values from environment file (for example: .env)",
    )

    args = parser.parse_args()

    if args.transaction_id:
        os.environ.setdefault("FIREFLY_III_TRANSACTION_ID", args.transaction_id)

    if args.api_key:
        os.environ.setdefault("FIREFLY_III_API_KEY", args.api_key)

    if args.url:
        os.environ.setdefault("FIREFLY_III_URL", args.url)

    if args.grams_gold:
        os.environ.setdefault("GRAMS_GOLD", args.grams_gold)

    if args.load_dotenv:
        load_dotenv(args.load_dotenv)

    setup_logging("firefly_iii_treasury_id_update", verbose=args.verbose)
    asyncio.run(run_main())


if __name__ == "__main__":
    execute_cli_main()
