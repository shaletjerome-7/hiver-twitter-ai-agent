"""
Extract Spotify support conversations from the Kaggle
Customer Support on Twitter dataset.

Outputs
-------
data/spotify_pairs.jsonl
    Retrieval corpus for the agent.

data/sample_data.csv
    Small reproducible sample (default: 700 conversations)
    used for evaluation and manual labelling.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Path to twcs.csv"
    )

    parser.add_argument(
        "--brand",
        default="SpotifyCares"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=700,
        help="Maximum conversations to extract"
    )

    args = parser.parse_args()

    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    ##############################################
    # Pass 1
    # Store every Spotify reply by parent tweet id
    ##############################################

    spotify_replies = {}

    with open(args.input, encoding="utf8", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if (
                row["author_id"].lower() == args.brand.lower()
                and row.get("in_response_to_tweet_id")
            ):

                spotify_replies[
                    row["in_response_to_tweet_id"]
                ] = row

    ##############################################
    # Pass 2
    ##############################################

    retrieval_examples = []

    sample_rows = []

    with open(args.input, encoding="utf8", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if len(sample_rows) >= args.limit:
                break

            if row.get("inbound", "").lower() != "true":
                continue

            tweet_id = row["tweet_id"]

            if tweet_id not in spotify_replies:
                continue

            reply = spotify_replies[tweet_id]

            retrieval_examples.append(
                {
                    "message": row["text"],
                    "reply": reply["text"],
                }
            )

            sample_rows.append(
                {
                    "tweet_id": tweet_id,
                    "conversation_id": row.get(
                        "conversation_id",
                        ""
                    ),
                    "customer_message": row["text"],
                    "spotify_reply": reply["text"],
                }
            )

    ##############################################
    # Save Retrieval Corpus
    ##############################################

    retrieval_path = output_dir / "spotify_pairs.jsonl"

    retrieval_path.write_text(
        "\n".join(
            json.dumps(x, ensure_ascii=False)
            for x in retrieval_examples
        ),
        encoding="utf8",
    )

    ##############################################
    # Save Sample CSV
    ##############################################

    csv_path = output_dir / "sample_data.csv"

    with open(csv_path, "w", newline="", encoding="utf8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "tweet_id",
                "conversation_id",
                "customer_message",
                "spotify_reply",
            ],
        )

        writer.writeheader()

        writer.writerows(sample_rows)

    print("=" * 60)
    print("Extraction Complete")
    print("=" * 60)
    print(f"Retrieval pairs : {len(retrieval_examples)}")
    print(f"Sample dataset  : {len(sample_rows)}")
    print(f"Saved to        : {csv_path}")


if __name__ == "__main__":
    main()