# Golden Set Sampling Protocol

## Dataset

Customer Support on Twitter (TWCS)

Brand: SpotifyCares

## Sampling Method

A sample of 200 customer conversations was selected from the extracted
SpotifyCares interactions.

Sampling was random after filtering for:

- inbound customer tweets
- valid Spotify reply
- one reply per conversation

Random seed used:

42

## Time Range

The sample was drawn from the available TWCS Spotify conversations.

## Label Distribution Goal

Each intent should contain at least 15 examples.

Intents:

- billing
- playback
- login
- account
- refund
- other

## Manual Annotation

Every sample will be manually labelled with:

- intent
- should_escalate

Two reviewers should independently annotate at least 50 samples.

Disagreements are resolved by discussion.

## Notes

The provided demo labels are placeholders.

Performance claims in the final report will be based only on the manually
verified golden dataset.