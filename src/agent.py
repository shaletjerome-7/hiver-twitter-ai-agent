from __future__ import annotations

from dataclasses import dataclass

from .classifier import classify
from .retrieval import retrieve
from .policy import decide_action


@dataclass
class Decision:

    intent: str

    reply: str

    action: str

    reason: str

    evidence: str

    score: float


def decide(

    message,

    history,

):

    intent, confidence = classify(message)

    match, similarity = retrieve(

        message,

        history,

    )

    action, reason = decide_action(

        message,

        intent,

        confidence,

        similarity,

    )

    if match:

        reply = match["reply"]

        evidence = match["reply"]

    else:

        reply = (

            "Thanks for contacting Spotify. "

            "We'll review this."

        )

        evidence = "No retrieval"

    return Decision(

        intent=intent,

        reply=reply,

        action=action,

        reason=reason,

        evidence=evidence,

        score=similarity,

    )