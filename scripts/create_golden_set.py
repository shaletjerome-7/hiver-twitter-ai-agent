"""
Create a template for manually labeling a golden dataset.

This script randomly samples conversations from sample_data.csv
and creates golden_200.json with empty labels that should be
filled in manually.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        default="data/sample_data.csv"
    )

    parser.add_argument(
        "--output",
        default="data/golden_200.json"
    )

    parser.add_argument(
        "--size",
        type=int,
        default=200
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42
    )

    args = parser.parse_args()

    random.seed(args.seed)

    with open(args.input, encoding="utf8") as file:
        rows = list(csv.DictReader(file))

    if len(rows) < args.size:
        raise ValueError(
            f"Only {len(rows)} rows available."
        )

    sampled = random.sample(rows, args.size)

    golden = []

    for i, row in enumerate(sampled, start=1):

        golden.append(
            {
                "id": i,
                "tweet_id": row["tweet_id"],
                "conversation_id": row["conversation_id"],
                "message": row["customer_message"],

                # Fill these manually
                "intent": "",
                "should_escalate": None,
                "reply_keywords": [],

                "historical_reply": row["spotify_reply"]
            }
        )

    Path(args.output).write_text(
        json.dumps(golden, indent=2, ensure_ascii=False),
        encoding="utf8"
    )

    print(f"Created {args.output}")
    print(f"Examples: {len(golden)}")


if __name__ == "__main__":
    main()