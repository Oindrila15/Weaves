# CCA-F schedule (hands-on)

Exam: **Tuesday 24 November 2026** (moved from 10 Nov). Built from Anthropic's official exam guide only (`CCA-F-Exam-Guide.pdf` in this folder, kept local and not in git). See [syllabus-map.md](syllabus-map.md) for all 30 topics in plain language and [notes/](notes/) for revision sheets. Code lives in [day1/](day1/) and [day2/](day2/).

If a day slips, CCA-F comes first until 24 Nov (see [../README.md](../README.md)). Revised on Wed 4 Nov: exams moved to 24 Nov, and Oindrila is away 7 to 10 Nov and on 15 Nov.

**Method:** each day, learn a domain's ideas, build a small thing that uses them (on saree data, so it is useful for Weaves later), then answer practice questions. Building teaches the *how*; the exam asks *which design is best*, so every day ends with scenario questions.

**What you need:** an Anthropic API key (small spend, a few dollars for the whole week), Python 3, and the `Weaves` repo.

| Day | Date | Learn | Build (small, saved to git) | Guide exercise | Status |
|---|---|---|---|---|---|
| 1 | Thu 29 Oct | Domain 1: agentic loop (1.1), hooks (1.5), enforcement (1.4) | A tool-using agent with 3 or 4 saree tools and a loop that follows `stop_reason`. A hook that blocks a rule-breaking call | Exercise 1 | Done (guide exercise not yet done) |
| 2 | Fri 30 Oct to Tue 3 Nov | Domain 2: tool descriptions (2.1), errors (2.2), tool counts and `tool_choice` (2.3), MCP (2.4) | Rewrite two overlapping tools so Claude picks correctly. Add structured errors (category, retryable). A tiny MCP server | Exercise 1, 2 | Done. MCP answers marked |
| 3 | Wed 11 to Thu 12 Nov | Domain 4: criteria, few-shot, schemas, retry, batch | Extract a weave record from a web page: nullable fields, validate and retry, a small batch run | Exercise 3 | |
| 4 | Thu 12 Nov | Domain 1.2 to 1.3, 1.6 to 1.7 and Domain 5.3, 5.6 | A coordinator with two subagents, run in parallel, passing sources through to a cited summary. Simulate a timeout | Exercise 4 | |
| 5 | Fri 13 Nov | Domain 3: CLAUDE.md levels, rules, skills, plan mode, CI | Configure the Weaves repo: `.claude/rules/` with paths, one skill with `context: fork`, a `.mcp.json`. Run `claude -p` | Exercise 2 | |
| 6 | Mon 16 Nov | Domain 5.1, 5.2, 5.4, 5.5 | Escalation rules with examples. A confidence and review-routing check | Sample questions | |
| 7 | Sat 21 Nov | Practice questions for all six scenarios | Redo weak spots from every notes file | Sample questions | |
| 8 | Sun 22 Nov | Light review and weak spots. No new topics | Sleep early. Mon 23 Nov is a rest day | | |
| | **Tue 24 Nov** | **Exam** | | | |

**Daily routine:** read the day's rows in the syllabus map, build with Claude Code guiding, then 5 to 10 scenario questions. Write weak spots at the bottom of that day's notes file.

**Exam day facts:** government photo ID matching your registration name, a clear desk, no phone or notes, proctored. Do not share exam questions afterwards.

**Away:** Sat 7 to Tue 10 Nov, Sat 14 Nov and Sun 15 Nov (birthday). Revised on Wed 11 Nov because Domain 4 teaching is more detailed (textbook style, theory first). Teaching for CCA-F ends Mon 16 Nov and for CCA-P Fri 20 Nov. Sat 21 is practice questions for both, Sun 22 is weak spots and light review, Mon 23 is rest. Videos: [../videos.md](../videos.md).
