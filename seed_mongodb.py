"""
Seed MongoDB Atlas with disease_info data migrated from sql/create_tables.sql.

Usage:
    python scripts/seed_mongodb.py
    python scripts/seed_mongodb.py --reset   # drop collection before seeding
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from db_config import DB_NAME, DISEASE_COLLECTION, get_client, get_disease_collection  # noqa: E402


def load_seed_data() -> list[dict]:
    data_path = ROOT / "sql" / "disease_data.json"
    with data_path.open(encoding="utf-8") as f:
        return json.load(f)


def seed(reset: bool = False) -> None:
    client = get_client()
    client.admin.command("ping")
    print(f"Connected to MongoDB Atlas (database: {DB_NAME})")

    collection = get_disease_collection()
    if reset:
        collection.drop()
        print(f"Dropped collection '{DISEASE_COLLECTION}'")

    records = load_seed_data()
    collection.create_index("disease_name", unique=True)

    inserted = 0
    updated = 0
    for record in records:
        result = collection.update_one(
            {"disease_name": record["disease_name"]},
            {"$set": record},
            upsert=True,
        )
        if result.upserted_id:
            inserted += 1
        elif result.modified_count:
            updated += 1

    total = collection.count_documents({})
    print(f"Seed complete: {inserted} inserted, {updated} updated, {total} total documents")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed MongoDB with plant disease data")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop the disease_info collection before seeding",
    )
    args = parser.parse_args()

    try:
        seed(reset=args.reset)
    except Exception as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
