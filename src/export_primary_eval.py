from __future__ import annotations

import json
from pathlib import Path

from .agent import decide


def export_primary_eval(
    golden_rows,
    history,
    output_path="artifacts/primary_eval.json",
):
    """
    Runs the support agent on every golden example and
    exports detailed predictions for reviewer auditing.
    """

    records = []

    for row in golden_rows:

        prediction = decide(
            row["message"],
            history,
        )

        records.append(
            {
                "id": row.get("id", len(records) + 1),
                "message": row["message"],

                # Ground Truth
                "expected_intent": row["intent"],

                "expected_escalation": (
                    row["should_escalate"]
                    if "should_escalate" in row
                    else row["expected_action"] == "escalate"
                ),

                # Agent Output
                "predicted_intent": prediction.intent,
                "reply": prediction.reply,
                "action": prediction.action,
                "reason": prediction.reason,
                "evidence": prediction.evidence or "",
                "similarity": prediction.score,
            }
        )

    Path("artifacts").mkdir(exist_ok=True)

    Path(output_path).write_text(
        json.dumps(records, indent=4, ensure_ascii=False),
        encoding="utf8",
    )

    print(f"Primary evaluation exported to {output_path}")