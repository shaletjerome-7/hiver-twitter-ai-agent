from __future__ import annotations

import json

from pathlib import Path

from reviewer_logic import review


def main():

    input_file = Path(
        "artifacts/primary_eval.json"
    )

    output_file = Path(
        "artifacts/final_audit_report.json"
    )

    rows = json.loads(
        input_file.read_text(
            encoding="utf8"
        )
    )

    audits = []

    passed = 0

    total_score = 0

    for row in rows:

        result = review(row)

        audits.append(
            result.__dict__
        )

        total_score += result.total_score

        if result.passed:

            passed += 1

    summary = {

        "total_examples": len(rows),

        "passed": passed,

        "failed": len(rows) - passed,

        "average_score": round(
            total_score / len(rows),
            2,
        ),

        "results": audits,
    }

    output_file.write_text(

        json.dumps(
            summary,
            indent=4,
        ),

        encoding="utf8",
    )

    print("=" * 60)

    print("Reviewer Audit Complete")

    print("=" * 60)

    print(

        f"Passed : {passed}/{len(rows)}"

    )

    print(

        f"Average Score : {summary['average_score']}"

    )

    print(

        f"Saved : {output_file}"

    )


if __name__ == "__main__":

    main()