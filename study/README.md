# CCA-F study plan (hands-on, one week)

Built from Anthropic's official exam guide only. See [syllabus-map.md](syllabus-map.md) for all 30 topics in plain language.

**Method:** each day, learn a domain's ideas, build a small thing that uses them (on saree data, so it is useful for Weaves later), then answer practice questions. Building teaches the *how*; the exam asks *which design is best*, so every day ends with scenario questions.

**What you need:** an Anthropic API key (small spend, a few dollars for the whole week), Python 3, and the `Weaves` repo.

| Day | Learn | Build (small, saved to git) | Guide exercise |
|---|---|---|---|
| 1 | Domain 1: agentic loop (1.1), hooks (1.5), enforcement (1.4) | A tool-using agent with 3 or 4 saree tools and a loop that follows `stop_reason`. A hook that blocks a rule-breaking call | Exercise 1 |
| 2 | Domain 2: tool descriptions, errors, tool counts, MCP | Rewrite two overlapping tools so Claude picks correctly. Add structured errors (category, retryable). A tiny MCP server | Exercise 1, 2 |
| 3 | Domain 4: criteria, few-shot, schemas, retry, batch | Extract a weave record from a web page: nullable fields, validate and retry, a small batch run | Exercise 3 |
| 4 | Domain 1.2 to 1.3, 1.6 to 1.7 and Domain 5.3, 5.6 | A coordinator with two subagents, run in parallel, passing sources through to a cited summary. Simulate a timeout | Exercise 4 |
| 5 | Domain 3: CLAUDE.md levels, rules, skills, plan mode, CI | Configure the Weaves repo: `.claude/rules/` with paths, one skill with `context: fork`, a `.mcp.json`. Run `claude -p` | Exercise 2 |
| 6 | Domain 5.1, 5.2, 5.4, 5.5 | Escalation rules with examples. A confidence and review-routing check. Then practice questions for all six scenarios | Sample questions |
| 7 | Gaps | Redo the topics you got wrong. Light review only. Sleep | Sample questions |

**Daily routine (about 3 to 4 hours):** read the day's rows in the syllabus map, build with Claude Code guiding, then 5 to 10 scenario questions. Write your weak spots at the bottom of this file.

**Exam day facts:** government photo ID matching your registration name, a clear desk, no phone or notes, proctored. Do not share exam questions afterwards.

## Weak spots
(add as we go)
