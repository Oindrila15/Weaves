# CCA-F schedule (hands-on, one week)

Exam: **Friday 6 November 2026**. Built from Anthropic's official exam guide only (`CCA-F-Exam-Guide.pdf` in this folder, kept local and not in git). See [syllabus-map.md](syllabus-map.md) for all 30 topics in plain language and [notes/](notes/) for revision sheets. Code lives in [day1/](day1/).

If a day slips, CCA-F comes first until 6 Nov (see [../README.md](../README.md)).

**Method:** each day, learn a domain's ideas, build a small thing that uses them (on saree data, so it is useful for Weaves later), then answer practice questions. Building teaches the *how*; the exam asks *which design is best*, so every day ends with scenario questions.

**What you need:** an Anthropic API key (small spend, a few dollars for the whole week), Python 3, and the `Weaves` repo.

| Day | Date | Learn | Build (small, saved to git) | Guide exercise | Status |
|---|---|---|---|---|---|
| 1 | Thu 29 Oct | Domain 1: agentic loop (1.1), hooks (1.5), enforcement (1.4) | A tool-using agent with 3 or 4 saree tools and a loop that follows `stop_reason`. A hook that blocks a rule-breaking call | Exercise 1 | Done (guide exercise not yet done) |
| 2 | Fri 30 Oct | Domain 2: tool descriptions, errors, tool counts, MCP | Rewrite two overlapping tools so Claude picks correctly. Add structured errors (category, retryable). A tiny MCP server | Exercise 1, 2 | |
| 3 | Sat 31 Oct | Domain 4: criteria, few-shot, schemas, retry, batch | Extract a weave record from a web page: nullable fields, validate and retry, a small batch run | Exercise 3 | |
| 4 | Sun 1 Nov | Domain 1.2 to 1.3, 1.6 to 1.7 and Domain 5.3, 5.6 | A coordinator with two subagents, run in parallel, passing sources through to a cited summary. Simulate a timeout | Exercise 4 | |
| 5 | Mon 2 Nov | Domain 3: CLAUDE.md levels, rules, skills, plan mode, CI | Configure the Weaves repo: `.claude/rules/` with paths, one skill with `context: fork`, a `.mcp.json`. Run `claude -p` | Exercise 2 | |
| 6 | Tue 3 Nov | Domain 5.1, 5.2, 5.4, 5.5 | Escalation rules with examples. A confidence and review-routing check. Then practice questions for all six scenarios | Sample questions | |
| 7 | Wed 4 Nov | Gaps | Short pass on the topics you got wrong | Sample questions | |
| | Thu 5 Nov | Practice questions and weak spots. No new topics | Sleep early | | |
| | **Fri 6 Nov** | **Exam** | | | |

**Daily routine:** read the day's rows in the syllabus map, build with Claude Code guiding, then 5 to 10 scenario questions. Write weak spots at the bottom of that day's notes file.

**Exam day facts:** government photo ID matching your registration name, a clear desk, no phone or notes, proctored. Do not share exam questions afterwards.
