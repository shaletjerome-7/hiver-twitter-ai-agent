# Decision log

1. Chose SpotifyCares because playback, login, and Premium billing form coherent public-support themes.
2. Treated this as assistive triage, not an account-action bot, to keep claims proportional to evidence.
3. Used six broad intents so a 200-case gold set can cover each reasonably.
4. Made `other` a valid route rather than forcing every message into a business category.
5. Escalate account and refund requests even when intent is obvious; correctness is not authorisation.
6. Escalate messages with sensitive-data words because public replies are unsafe for them.
7. Used lexical retrieval so every draft has inspectable local evidence.
8. Used Jaccard overlap rather than an embedding dependency to keep a first run offline and under 15 minutes.
9. Kept reply writing extractive; it cannot hallucinate a new policy from an LLM.
10. Included a deterministic fixture rather than redistributing a large public dataset in the repository.
11. Kept the Kaggle extraction script separate so a reviewer can run a real-data experiment with their own download.
12. Added a hook for a human audit of the rubric; rubric validity should be measured, not assumed.
13. Reported limitations prominently because fixture scores do not generalise to production.
14. Chose action accuracy alongside intent accuracy because safe routing is the product decision.
