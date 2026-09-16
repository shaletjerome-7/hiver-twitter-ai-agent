from __future__ import annotations

import re

TOKEN = re.compile(r"[a-z']+")

KEYWORDS = {
    "billing": {
        "charged",
        "charge",
        "billing",
        "payment",
        "premium",
        "invoice",
        "price",
        "double",
        "twice",
    },
    "login": {
        "login",
        "log in",
        "password",
        "sign in",
        "reset",
        "locked",
        "access",
    },
    "playback": {
        "play",
        "playing",
        "music",
        "song",
        "stream",
        "offline",
        "download",
        "buffer",
        "ads",
    },
    "account": {
        "account",
        "hack",
        "hacked",
        "email",
        "suspicious",
        "someone",
    },
    "refund": {
        "refund",
        "money back",
        "cancel",
        "cancelled",
        "trial",
    },
}


def tokenize(text: str):

    return set(TOKEN.findall(text.lower()))


def classify(text: str):

    lower = text.lower()

    words = tokenize(text)

    scores = {}

    for intent, phrases in KEYWORDS.items():

        score = 0

        for phrase in phrases:

            if " " in phrase:

                if phrase in lower:
                    score += 1

            else:

                if phrase in words:
                    score += 1

        scores[intent] = score

    if scores["refund"]:

        return "refund", 0.95

    if scores["account"]:

        return "account", 0.95

    intent = max(
        scores,
        key=scores.get,
    )

    confidence = min(
        0.95,
        0.45 + 0.15 * scores[intent],
    )

    if scores[intent] == 0:

        return "other", 0.40

    return intent, confidence