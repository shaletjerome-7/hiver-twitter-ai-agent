from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuditResult:

    id: int

    intent_correct: bool

    escalation_correct: bool

    grounded: bool

    reply_quality: int

    total_score: int

    passed: bool

    comments: list[str]


def review(record):

    comments = []

    score = 0

    ###########################################
    # Intent
    ###########################################

    intent_ok = (
        record["expected_intent"]
        == record["predicted_intent"]
    )

    if intent_ok:

        score += 2

    else:

        comments.append(
            "Incorrect intent."
        )

    ###########################################
    # Escalation
    ###########################################

    expected = (
        "escalate"
        if record["expected_escalation"]
        else "auto_handle"
    )

    escalation_ok = (
        expected
        == record["action"]
    )

    if escalation_ok:

        score += 2

    else:

        comments.append(
            "Wrong escalation."
        )

    ###########################################
    # Grounding
    ###########################################

    grounded = (
        record["similarity"] >= 0.10
        and len(record["evidence"]) > 0
    )

    if grounded:

        score += 2

    else:

        comments.append(
            "Weak retrieval grounding."
        )

    ###########################################
    # Reply Quality
    ###########################################

    reply = record["reply"].lower()

    reply_score = 0

    if len(reply) > 25:
        reply_score += 1

    if (
        "please" in reply
        or "thanks" in reply
        or "sorry" in reply
    ):
        reply_score += 1

    score += reply_score

    if reply_score < 2:

        comments.append(
            "Reply could be more helpful."
        )

    ###########################################

    return AuditResult(

        id=record["id"],

        intent_correct=intent_ok,

        escalation_correct=escalation_ok,

        grounded=grounded,

        reply_quality=reply_score,

        total_score=score,

        passed=score >= 6,

        comments=comments,
    )