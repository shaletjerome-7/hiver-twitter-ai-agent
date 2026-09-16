from __future__ import annotations

import re

TOKEN = re.compile(r"[a-z']+")


def tokenize(text):

    return set(
        TOKEN.findall(
            text.lower()
        )
    )


def retrieve(message, history):

    query = tokenize(message)

    best = None

    best_score = 0

    for row in history:

        words = tokenize(
            row["message"]
        )

        union = query | words

        if not union:
            continue

        score = len(query & words) / len(union)

        if score > best_score:

            best_score = score

            best = row

    return best, best_score