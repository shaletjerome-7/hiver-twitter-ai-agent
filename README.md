# Hiver take-home: Spotify Twitter support agent

This repository is a small, reproducible support-agent prototype for **SpotifyCares**.
It routes a customer tweet, retrieves similar historical resolutions, drafts a conservative
reply, and decides whether it is safe to auto-handle.

## Quick start (Windows PowerShell)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Tharun123q/hiver-twitter-ai-agent.git

cd hiver-twitter-ai-agent
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Entire Pipeline

```bash
python run_pipeline.py
```

### 6. Evaluate

```bash
python -m src.evaluate --data data/golden_set.jsonl --out artifacts/results.json
```

## Using the Kaggle data

Download `twcs.csv` from [Customer Support on Twitter](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
and put it in `data/raw/`. Then run:

```powershell
python -m src.prepare_twcs --input data/raw/twcs.csv --brand SpotifyCares --limit 5000
```

This creates `data/spotify_pairs.jsonl`. The demo stays offline: it does not call an
LLM API and therefore cannot leak customer text. For a production deployment I would
replace the rule-based intent layer with a supervised classifier and use an approved,
redacted LLM for rewrite-only generation.

## What is in the repo

- `src/agent.py` - intent, nearest-neighbour retrieval, response and escalation logic
- `src/evaluate.py` - deterministic metrics and a rubric-style offline judge
- `data/golden_set.jsonl` - 200 deterministic demo test cases after setup; replace these
  with manually labelled real examples before making a performance claim
- `docs/report.md` - concise report, baselines, failure analysis and limitations
- `docs/decision_log.md` - non-obvious decisions

## Reproduction notes

The included fixture is intentionally small and synthetic-looking enough to be safely
shared. It tests the *pipeline* rather than claiming to be a faithful statistical sample
of Twitter or a completed human-labelled golden set. The sampling/label protocol for a
real Kaggle run is documented in `docs/report.md`. Do not reuse public tweets for training
without checking the dataset licence and your organisation's privacy review.

## Sources

- [Customer Support on Twitter dataset](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
  (tweet/reply identifiers and `in_response_to_tweet_id` relationship).
- Hardalov et al., [Towards Automated Customer Support](https://arxiv.org/abs/1809.00303),
  used only as background for the dataset's conversational-support setting.

## Project Architecture

Customer Tweet
        │
        ▼
Intent Classifier
        │
        ▼
Historical Retrieval
        │
        ▼
Policy Engine
        │
        ▼
Draft Reply
        │
        ▼
Evaluation Harness
        │
        ▼
Reviewer Audit

## Current Limitations

This project intentionally avoids using an external LLM API to remain
fully reproducible.

Limitations include:

- keyword intent classifier
- lexical retrieval
- no multilingual support
- limited taxonomy
- no continuous learning

## API Keys

The default implementation is completely offline and does not require any API keys.

If an optional LLM reviewer is implemented in the future, API keys should be supplied using environment variables rather than hard-coded credentials.