# Runbook

## myapp-prod-cpu-high
CPU has been above 80% for 10+ minutes.
Check first: CloudWatch Logs for myapp-prod, look for repeated errors or retry loops.
Check the Actions tab for a recent deploy that might have introduced a regression.
Typical fix: if traffic-driven, this app has no autoscaling configured, so the
short-term fix is manual — redeploy with a larger task size (edit the task
definition's CPU value) if this becomes recurring. If it's a code issue, roll
back by redeploying the previous task definition revision from the ECS console.

## myapp-prod-memory-high
Same triage as CPU: check logs first, check recent deploys second.
Distinct risk if unaddressed: the task gets OOMKilled, which shows up as an
unexpected task stop, not a graceful shutdown, and looks like a crash in the logs.

## myapp-prod-tasks-down
RunningTaskCount dropped below 1. The prod site is fully down.
Check first: ECS console, myapp-prod service, Tasks tab, most recent stopped
task's "Stopped reason" field. This is the exact same field that showed the
platform-mismatch error during initial setup.
Typical fix: if it's an image or config problem, fix and redeploy. If the
task is simply gone with no clear reason, try Update service, Force new
deployment, before escalating further.

## myapp-bedrock-tokens-25pct-daily
The /ask feature used 25% of its daily token budget (7.5M of 30M, ~$0.47) in 24h.
Normal traffic is a few hundred questions a day, so this usually means a bot.
Check first: CloudWatch Logs for /ecs/myapp-task, filter `event = "ask"`, and
look at outcomes and questions. The app hard-stops at 30M tokens/day on its own,
so no action is required to cap spend; if abuse continues, lower
DAILY_TOKEN_BUDGET or ASK_LIMIT_PER_WINDOW in app.py and redeploy.
