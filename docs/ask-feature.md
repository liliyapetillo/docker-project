# "Ask about my experience" with Bedrock

A question box on the page: visitors ask about my background and get a short
answer from Amazon Bedrock (Nova Lite), grounded only in
`prompts/resume_facts.md`. No new compute and no new role, just one more
permission on `myapp-task-role`, scoped to that one model.

Unlike everything else here, each request costs real money, and the endpoint
is public and unauthenticated. So the guardrails went in with the feature:

- **Per-IP rate limit** (5 questions/minute), an atomic counter in the
  existing DynamoDB table, checked before Bedrock is called.
- **Hard daily token cap** (30M tokens, about $1.90/day). Each request
  reserves its worst-case tokens in one conditional DynamoDB write before
  calling Bedrock, so concurrent requests can't overshoot it. A CloudWatch
  alarm emails at 25% of the budget.
- **Fail closed**: if the limits can't be checked, Bedrock isn't called.
- **Small, bounded requests**: questions capped at 300 characters, answers
  at 200 tokens, and the unchanging system prompt is prompt-cached.
- **Off-topic guard**: the model replies with a sentinel for anything not
  about me, and the app swaps in a fixed reply.
- **Question logging** to CloudWatch (outcome, question, tokens; no IPs),
  with 30-day retention.

What testing caught: the first off-topic guard blocked real questions like
"Has she worked with Docker?", and Nova Micro missed facts that were in the
file. Running a fixed set of on- and off-topic questions against the real
model is what settled the prompt wording and the move from Micro to Lite.
