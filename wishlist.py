#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

DATA_FILE = Path(__file__).with_name("wishlist.json")


def load_products() -> list[dict[str, str]]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_products(products: list[dict[str, str]]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(products, file, indent=2)
        file.write("\n")


def add_product(name: str, kind: str) -> None:
    products = load_products()
    if any(product["name"].lower() == name.lower() for product in products):
        print(f"'{name}' is already saved.")
        return

    products.append(
        {
            "name": name,
            "kind": kind,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    save_products(products)
    print(f"Saved '{name}' for future reference.")


def list_products() -> None:
    products = load_products()
    if not products:
        print("No saved products yet.")
        return

    print("Saved products:")
    for index, product in enumerate(products, start=1):
        print(f"{index}. {product['name']} [{product['kind']}]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save products you like or want to buy for future reference."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Save a product")
    add_parser.add_argument("name", help="Product name")
    add_parser.add_argument(
        "--kind",
        choices=("like", "want_to_buy"),
        default="want_to_buy",
        help="Why you saved this product",
    )

    subparsers.add_parser("list", help="Show saved products")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "add":
        add_product(args.name, args.kind)
    elif args.command == "list":
        list_products()


if __name__ == "__main__":
    main()
