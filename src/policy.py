from __future__ import annotations

import re

HIGH_RISK = {

    "refund",

    "account",

}

SENSITIVE = re.compile(

    r"\b(card|password|bank|cvv|address|phone|email)\b",

    re.I,

)


def decide_action(

    text,

    intent,

    confidence,

    similarity,

):

    if SENSITIVE.search(text):

        return (

            "escalate",

            "Sensitive information detected.",

        )

    if intent in HIGH_RISK:

        return (

            "escalate",

            f"{intent} requires human review.",

        )

    if confidence < 0.60:

        return (

            "escalate",

            "Low intent confidence.",

        )

    if similarity < 0.10:

        return (

            "escalate",

            "No similar historical example.",

        )

    return (

        "auto_handle",

        "Safe to auto-handle.",

    )