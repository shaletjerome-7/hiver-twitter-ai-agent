import argparse, json
from pathlib import Path
from .agent import decide

parser = argparse.ArgumentParser()
parser.add_argument("message")
parser.add_argument("--examples", default="data/historical_pairs.jsonl")
args = parser.parse_args()
examples = [json.loads(x) for x in Path(args.examples).read_text(encoding="utf8").splitlines()]
print(json.dumps(decide(args.message, examples).__dict__, indent=2))
