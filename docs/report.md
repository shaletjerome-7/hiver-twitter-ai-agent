# Report: SpotifyCares support agent

## Problem framing

The useful version of this agent is a **triage-and-draft assistant**, not an autonomous
account agent. A good result identifies the customer's primary need, gives a short reply
consistent with prior support language, and avoids public handling of account, refund,
or sensitive-data cases. I chose six intents: billing, login, playback, account, refund,
and other. I did not build identity verification, payment actions, multilingual support,
or an LLM that invents policy.

## Data and gold labels

For the executable demo, `make_demo_data.py` creates 24 safe support-pair fixtures and
200 deterministic held-out message/action cases. They are not a manually labelled golden
set, and are deliberately not presented as original Twitter rows. For the required real
run, I would take the first direct
SpotifyCares reply for a stratified random sample of inbound tweets, remove duplicates,
sample 30-40 messages per provisional intent plus ambiguous cases, and label the 200
messages before running any model. Each label records the single dominant intent and
whether public auto-handling is safe. The Kaggle source uses reply links, so direct pairs
can be reconstructed by joining an agent row's `in_response_to_tweet_id` to an inbound
tweet ID.

## Method

The classifier is transparent keyword scoring. The reply is retrieved using Jaccard word
overlap from historical pairs. A policy layer escalates refunds, account changes, low
confidence/low-similarity messages, and sensitive terms. This is intentionally simple:
the interesting claim is whether the gate is safe, not that a tiny fixture can train a
general language model.

## Results

## Experimental Results

| System | Intent Accuracy | Macro F1 | Escalation F1 | Reply Quality (/8) |
|---------|----------------:|---------:|--------------:|-------------------:|
| Proposed System | 0.780 | 0.763 | 0.786 | 5.20 |
| Keyword Baseline | 0.780 | 0.763 | N/A | N/A |
| Trivial Baseline | 0.135 | 0.040 | N/A | N/A |

The proposed system achieves the same intent accuracy as the keyword baseline because it intentionally uses the same deterministic intent classifier. Its additional value comes from retrieval-grounded responses, conservative escalation rules, evidence tracking, and reviewer auditing rather than improved classification accuracy.

### Reply-quality judge and human agreement plan

The offline judge scores four 0-2 dimensions: correct intent, safe action, evidence exists,
and useful polite tone. The harness will calculate agreement when a reviewer adds a
`human_rubric` (0-8) field to audited rows. This demo contains no fabricated human scores.
For the real implementation, I would blind two human reviewers and compare a fixed
prompt/model judge with Pearson correlation and weighted agreement.

## Failure analysis

## Top 5 Failure Modes

### 1. Billing vs Refund

Messages containing payment and refund terminology occasionally overlap.

### 2. Playback vs Other

Very short tweets contain too little information.

### 3. Login vs Account

Security-related login issues sometimes resemble account compromise.

### 4. Retrieval Failure

If no similar historical conversation exists, the generated reply becomes generic.

### 5. Multiple Intents

Tweets mentioning multiple issues receive only one predicted intent.


## What is Misleading About the Headline Number?

The headline accuracy of 78% only measures intent classification.

It does not capture:

- Whether the retrieved historical example was relevant.
- Whether the drafted reply was grounded.
- Whether unsafe cases were escalated correctly.
- Whether supporting evidence was produced.

Consequently, intent accuracy alone understates the practical behaviour of the complete support pipeline.

## What I Would Do With One More Week

- Replace keyword classification with a supervised classifier.
- Replace lexical retrieval with TF-IDF or embedding retrieval.
- Add multilingual support.
- Add confidence calibration.
- Introduce active learning from reviewer feedback.
## Reviewer Audit

The reviewer independently evaluates every prediction produced by the primary agent.

Summary:

- Examples Reviewed: 200
- Passed: 141
- Average Reviewer Score: 6.12 / 8

The reviewer focuses on:

- intent correctness
- escalation correctness
- retrieval grounding
- reply quality

The proposed intent accuracy was 0.780 (95% CI: 0.723–0.837).

## Human Agreement

This repository includes support for measuring inter-annotator agreement.

The metric will be calculated after the manually labelled golden dataset has been completed.

Fields:

- Annotator A
- Annotator B
- Final Label

Metric:

- Cohen's κ

Target:

κ ≥ 0.60