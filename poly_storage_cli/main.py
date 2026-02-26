from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

from poly_storage_sdk import PolyStorageAPIError, PolyStorageAuthError, PolyStorageClient


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="poly-storage")
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key (fallback: ENTITY_API_KEY environment variable)",
    )
    parser.add_argument(
        "--base-url",
        default="https://api.entityml.com",
        help="API base URL (default: https://api.entityml.com)",
    )

    commands = parser.add_subparsers(dest="command")

    commands.add_parser("health", help="Check API health")

    polymarket = commands.add_parser("polymarket", help="Polymarket endpoints")
    polymarket_commands = polymarket.add_subparsers(dest="subcommand")

    poly_market_data = polymarket_commands.add_parser(
        "market-data", help="Fetch raw polymarket market data"
    )
    poly_market_data.add_argument("--condition-id", required=True)
    poly_market_data.add_argument("--date", required=True)
    poly_market_data.add_argument("--offset", type=int, default=0)
    poly_market_data.add_argument("--limit", type=int, default=10000)

    poly_summary = polymarket_commands.add_parser(
        "orderbook-summary", help="Fetch polymarket orderbook summary"
    )
    poly_summary.add_argument("--condition-id", required=True)
    poly_summary.add_argument("--date", required=True)
    poly_summary.add_argument("--resolution", type=int, default=60)

    kalshi = commands.add_parser("kalshi", help="Kalshi endpoints")
    kalshi_commands = kalshi.add_subparsers(dest="subcommand")

    kalshi_market_data = kalshi_commands.add_parser(
        "market-data", help="Fetch raw kalshi market data"
    )
    kalshi_market_data.add_argument("--ticker", required=True)
    kalshi_market_data.add_argument("--date", required=True)
    kalshi_market_data.add_argument("--offset", type=int, default=0)
    kalshi_market_data.add_argument("--limit", type=int, default=10000)

    kalshi_summary = kalshi_commands.add_parser(
        "orderbook-summary", help="Fetch kalshi orderbook summary"
    )
    kalshi_summary.add_argument("--ticker", required=True)
    kalshi_summary.add_argument("--date", required=True)
    kalshi_summary.add_argument("--resolution", type=int, default=60)

    api_keys = commands.add_parser("api-keys", help="API key management")
    api_key_commands = api_keys.add_subparsers(dest="subcommand")

    api_keys_create = api_key_commands.add_parser("create", help="Create an API key")
    api_keys_create.add_argument("--name", required=True)
    api_keys_create.add_argument("--user-id", required=True)

    api_keys_list = api_key_commands.add_parser("list", help="List API keys")
    api_keys_list.add_argument("--user-id", required=True)

    api_keys_delete = api_key_commands.add_parser("delete", help="Delete an API key")
    api_keys_delete.add_argument("--key-id", required=True)
    api_keys_delete.add_argument("--user-id", required=True)

    return parser


def _emit_json(payload: Dict[str, Any], *, stream) -> None:
    stream.write(json.dumps(payload, indent=2, sort_keys=True))
    stream.write("\n")


def _build_client(args: argparse.Namespace) -> PolyStorageClient:
    api_key = args.api_key or os.getenv("ENTITY_API_KEY")
    return PolyStorageClient(api_key=api_key, base_url=args.base_url)


def _execute(client: PolyStorageClient, args: argparse.Namespace) -> Dict[str, Any]:
    if args.command == "health":
        return client.system.health()

    if args.command == "polymarket":
        if args.subcommand == "market-data":
            return client.polymarket.get_market_data(
                condition_id=args.condition_id,
                date=args.date,
                offset=args.offset,
                limit=args.limit,
            )
        if args.subcommand == "orderbook-summary":
            return client.polymarket.get_orderbook_summary(
                condition_id=args.condition_id,
                date=args.date,
                resolution=args.resolution,
            )

    if args.command == "kalshi":
        if args.subcommand == "market-data":
            return client.kalshi.get_market_data(
                ticker=args.ticker,
                date=args.date,
                offset=args.offset,
                limit=args.limit,
            )
        if args.subcommand == "orderbook-summary":
            return client.kalshi.get_orderbook_summary(
                ticker=args.ticker,
                date=args.date,
                resolution=args.resolution,
            )

    if args.command == "api-keys":
        if args.subcommand == "create":
            return client.api_keys.create(name=args.name, user_id=args.user_id)
        if args.subcommand == "list":
            return client.api_keys.list(user_id=args.user_id)
        if args.subcommand == "delete":
            return client.api_keys.delete(key_id=args.key_id, user_id=args.user_id)

    raise PolyStorageAPIError(
        "Unknown command",
        status_code=400,
        detail="Unknown command",
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help(sys.stderr)
        return 2

    try:
        client = _build_client(args)
        result = _execute(client, args)
        _emit_json(result, stream=sys.stdout)
        return 0
    except PolyStorageAuthError as exc:
        _emit_json(
            {
                "error": "auth_error",
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
            stream=sys.stderr,
        )
        return 2
    except PolyStorageAPIError as exc:
        _emit_json(
            {
                "error": "api_error",
                "status_code": exc.status_code,
                "detail": exc.detail,
            },
            stream=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
