from __future__ import annotations

import argparse
import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)

from .agent import decide, classify
from .export_primary_eval import export_primary_eval
import math

def confidence_interval(p, n):
    if n == 0:
        return [0, 0]

    margin = 1.96 * math.sqrt((p * (1 - p)) / n)

    return [
        round(max(0, p - margin), 3),
        round(min(1, p + margin), 3),
    ]

####################################################
# Reply Rubric
####################################################

def rubric(prediction, row):
    """
    0–8 score

    2 = Correct intent

    2 = Correct escalation

    2 = Grounded reply

    2 = Helpful / polite
    """

    score = 0

    if prediction.intent == row["intent"]:
        score += 2

    if "should_escalate" in row:

        expected = (
            "escalate"
            if row["should_escalate"]
            else "auto_handle"
        )

    else:

        expected = row["expected_action"]

    if prediction.action == expected:
        score += 2

    if prediction.evidence:
        score += 2

    if any(
        word in prediction.reply.lower()
        for word in (
            "please",
            "sorry",
            "thanks",
        )
    ):
        score += 2

    return score


####################################################
# Baselines
####################################################

def trivial_baseline(rows):

    intents = ["other"] * len(rows)

    actions = ["escalate"] * len(rows)

    return intents, actions


def keyword_baseline(message: str):
    text = message.lower()

    if "refund" in text:
        return "refund"

    elif "payment" in text or "charged" in text:
        return "billing"

    elif "login" in text or "password" in text:
        return "login"

    elif "hack" in text:
        return "account"

    elif "play" in text or "song" in text:
        return "playback"

    return "other"

####################################################
# Metrics
####################################################

def metrics(true, pred):

    accuracy = accuracy_score(
        true,
        pred,
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            true,
            pred,
            average="macro",
            zero_division=0,
        )
    )

    matrix = confusion_matrix(
        true,
        pred,
    ).tolist()

    return {
        "accuracy": round(float(accuracy), 3),
        "precision": round(float(precision), 3),
        "recall": round(float(recall), 3),
        "macro_f1": round(float(f1), 3),
        "confusion_matrix": matrix,
    }


####################################################
# Main
####################################################

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data",
        required=True,
    )

    parser.add_argument(
        "--history",
        default="data/spotify_pairs.jsonl",
    )

    parser.add_argument(
        "--out",
        default="artifacts/results.json",
    )

    args = parser.parse_args()

    text = Path(args.data).read_text(
    encoding="utf8"
    ).strip()

    # Support both:
    # 1. JSON array (.json)
    # 2. JSON Lines (.jsonl)

    if text.startswith("["):
        rows = json.loads(text)
    else:
        rows = [
            json.loads(line)
            for line in text.splitlines()
            if line.strip()
        ]

    history = [
        json.loads(x)
        for x in Path(args.history)
        .read_text(
            encoding="utf8"
        )
        .splitlines()
        if x
    ]

    predictions = [
        decide(
            row["message"],
            history,
        )
        for row in rows
    ]

    ####################################################
    # Proposed System
    ####################################################

    true_intents = [
        row["intent"]
        for row in rows
    ]

    pred_intents = [
        p.intent
        for p in predictions
    ]

    proposed = metrics(
        true_intents,
        pred_intents,
    )
    

    ####################################################
    # Escalation
    ####################################################

    true_escalation = []

    for row in rows:

        if "should_escalate" in row:

            expected = (
                "escalate"
                if row["should_escalate"]
                else "auto_handle"
            )

        else:

            expected = row["expected_action"]

        true_escalation.append(expected)

    pred_escalation = [
        p.action
        for p in predictions
    ]

    esc_precision, esc_recall, esc_f1, _ = (
        precision_recall_fscore_support(
            true_escalation,
            pred_escalation,
            average="binary",
            pos_label="escalate",
            zero_division=0,
        )
    )

    ####################################################
    # Reply Quality
    ####################################################

    rubric_scores = [
        rubric(
            p,
            row,
        )
        for p, row in zip(
            predictions,
            rows,
        )
    ]

    ####################################################
    # Baselines
    ####################################################

    trivial_i, trivial_a = (
        trivial_baseline(rows)
    )

    keyword_i = [
        keyword_baseline(row["message"])
        for row in rows
    ]

    keyword_a = [
        "escalate"
        if intent in {"account", "refund"}
        else "auto_handle"
        for intent in keyword_i
    ]
    ####################################################
    # Output
    ####################################################

    result = {

        "n": len(rows),

        "proposed": {
            **proposed,
            "accuracy_95_ci": confidence_interval(
                proposed["accuracy"],
                len(rows),
            ),
            "escalation_precision": round(float(esc_precision), 3),
            "escalation_recall": round(float(esc_recall), 3),
            "escalation_f1": round(float(esc_f1), 3),

            "mean_reply_rubric": round(
                sum(rubric_scores) / len(rubric_scores),
                2,
            ),

            "advantages": [
                "Uses historical retrieval",
                "Grounded responses",
                "Safety policy before auto-handling",
                "Produces supporting evidence",
            ]
        },

        "baselines": {

            "trivial":{
                **metrics(true_intents, trivial_i),
                "supports_retrieval": False,
                "supports_grounding": False,
                "reply_generation": False,
            },

            "keyword":{
                **metrics(true_intents, keyword_i),
                "supports_retrieval": False,
                "supports_grounding": False,
                "reply_generation": False,
            },
        },
    }

    result["comparison"] = {
        "Proposed": {
            "Intent": True,
            "Retrieval": True,
            "Grounding": True,
            "Policy": True,
            "Evidence": True,
        },
        "Keyword Baseline": {
            "Intent": True,
            "Retrieval": False,
            "Grounding": False,
            "Policy": False,
            "Evidence": False,
        },
        "Trivial Baseline": {
            "Intent": False,
            "Retrieval": False,
            "Grounding": False,
            "Policy": False,
            "Evidence": False,
        },
    }
    Path("artifacts").mkdir(
        exist_ok=True
    )

    Path(args.out).write_text(
        json.dumps(
            result,
            indent=4,
        ),
        encoding="utf8",
    )
    export_primary_eval(
        rows,
        history,
    )

    print(
        json.dumps(
            result,
            indent=4,
        )
    )
if __name__ == "__main__":
    main()