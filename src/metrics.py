from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)


def classification_metrics(true_labels, predicted_labels):

    accuracy = accuracy_score(
        true_labels,
        predicted_labels,
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            true_labels,
            predicted_labels,
            average="macro",
            zero_division=0,
        )
    )

    matrix = confusion_matrix(
        true_labels,
        predicted_labels,
    ).tolist()

    return {
        "accuracy": round(float(accuracy), 3),
        "precision": round(float(precision), 3),
        "recall": round(float(recall), 3),
        "macro_f1": round(float(f1), 3),
        "confusion_matrix": matrix,
    }


def escalation_metrics(
    expected,
    predicted,
):

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            expected,
            predicted,
            average="binary",
            zero_division=0,
        )
    )

    return {
        "precision": round(float(precision), 3),
        "recall": round(float(recall), 3),
        "f1": round(float(f1), 3),
    }