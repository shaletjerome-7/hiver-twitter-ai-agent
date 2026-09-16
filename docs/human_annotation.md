# Human Annotation Protocol

## Purpose

The golden dataset is manually labelled to evaluate the support agent.

Each example is labelled with:

- intent
- should_escalate

## Double Annotation

50 examples should be independently labelled by two annotators.

The remaining examples may be labelled by a single annotator.

## Conflict Resolution

When disagreement occurs:

1. Discuss the example.
2. Refer to the intent codebook.
3. Record the final agreed label.

## Agreement Metric

Inter-annotator agreement is measured using Cohen's κ.

Only the independently labelled subset is used for κ.