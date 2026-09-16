from pathlib import Path
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument(
    "--brand",
    default="SpotifyCares",
    help="Brand to process"
)

parser.add_argument(
    "--sample",
    action="store_true",
    help="Use sample dataset"
)

args = parser.parse_args()

print("=" * 60)
print("Spotify Support Agent Pipeline")
print("=" * 60)

# Step 1
print("\n[1/5] Preparing dataset...")

subprocess.run(
    [
        sys.executable,
        "scripts/make_demo_data.py"
    ],
    check=True
)

# Step 2
print("\n[2/5] Running evaluation...")

subprocess.run(
    [
        sys.executable,
        "-m",
        "src.evaluate",
        "--data",
        "data/golden_set.jsonl",
        "--out",
        "artifacts/results.json"
    ],
    check=True
)

print("\n[3/5] Running reviewer audit...")

subprocess.run(
    [
        sys.executable,
        "reviewer/run_reviewer.py",
    ],
    check=True,
)

print("\n[4/5] Running demo prediction...")

subprocess.run(
    [
        sys.executable,
        "-m",
        "src.demo",
        "@SpotifyCares I was charged twice for Premium"
    ],
    check=True
)

# Step 4
print("\n[5/5] Pipeline complete!")

print("\nOutputs written to:")
print("artifacts/results.json")
print("data/golden_set.jsonl")