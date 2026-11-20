# CCA-F schedule (hands-on)

Exam: **Monday 21 December 2026** (moved from 24 Nov). Built from Anthropic's official exam guide only (`CCA-F-Exam-Guide.pdf` in this folder, kept local and not in git). See [syllabus-map.md](syllabus-map.md) for all 30 topics in plain language and [notes/](notes/) for revision sheets. Code lives in [day1/](day1/) and [day2/](day2/).

If a day slips, CCA-F comes first until 21 Dec (see [../README.md](../README.md)). Revised on Fri 20 Nov after the exams moved to 21 to 23 Dec. Weekends are off. **Note:** third-party sites say the 7 Dec exam changes affect CCAO-F, CCDV-F and CCAR-P but not CCAR-F (unconfirmed; Anthropic's page blocks my tool). If the CCAR-F guide on Anthropic's site shows a newer version than v1.0 July 2026, compare it with ours first.

**Method:** each day, learn a domain's ideas, build a small thing that uses them (on saree data, so it is useful for Weaves later), then answer practice questions. Building teaches the *how*; the exam asks *which design is best*, so every day ends with scenario questions.

**What you need:** an Anthropic API key (small spend, a few dollars for the whole week), Python 3, and the `Weaves` repo.

| Day | Date | Learn | Build (small, saved to git) | Status |
|---|---|---|---|---|
| 1 | Thu 29 Oct | Domain 1: agentic loop (1.1), hooks (1.5), enforcement (1.4) | Tool-using agent, loop on `stop_reason`, a blocking hook | Done (guide exercise not yet done) |
| 2 | Fri 30 Oct to Tue 3 Nov | Domain 2: tool descriptions, errors, tool counts, MCP | Overlapping tools fixed, structured errors, tiny MCP server | Done |
| 3 | Wed 11 to Fri 20 Nov | Domain 4: 4.1 criteria, 4.2 few-shot, 4.3 schemas, 4.4 retry, 4.5 batch, 4.6 review | `day3/ch1` to `ch5` scripts | Chapters 1 to 4 taught and 1 to 2 checked. Chapter 5 built, not yet taught. Chapter 6 to do |
| 4 | Fri 20 Nov (today) | Domain 4 finish: Chapter 5 (batch) and Chapter 6 (independent review) | Chapter 6 script | |
| 5 | Mon 23 Nov | Domain 4 practice set | | |
| 6 | Tue 24 and Wed 25 Nov | Domain 1.2, 1.3, 1.6, 1.7: coordinator, subagents, parallel, handoffs, sessions | A coordinator with two subagents, parallel, cited summary, simulated timeout | |
| 7 | Thu 26 and Fri 27 Nov | Domain 3: CLAUDE.md levels, rules, commands, skills, plan mode, iterating, CI | `.claude/rules/` with paths, a skill with `context: fork`, `.mcp.json`, `claude -p` | |
| 8 | Mon 30 Nov and Tue 1 Dec | Domain 5: context, escalation, errors, provenance, human review | Escalation rules with examples, a confidence and review-routing check | |
| 9 | Wed 2 Dec | F practice set 1: mixed scenarios, all domains | | |
| 10 | Thu 3 Dec | F weak spots from every notes file | | |
| | Fri 4 Dec | **Buffer** (catch up, or changes from the new guides) | | |
| | Mon 7 to Mon 14 Dec | CCA-P teaching (see [../CCAR-P/schedule.md](../CCAR-P/schedule.md)) | | |
| | Wed 16 Dec | F and P mixed practice, weak spots | | |
| | Thu 17 Dec | **Buffer** and weak spots | | |
| | Fri 18 Dec | Light review of F, early night | | |
| | Sat 19 and Sun 20 Dec | Rest | | |
| | **Mon 21 Dec** | **Exam** | | |

**Daily routine:** read the day's rows in the syllabus map, build with Claude Code guiding, then 5 to 10 scenario questions. Write weak spots at the bottom of that day's notes file.

**Exam day facts:** government photo ID matching your registration name, a clear desk, no phone or notes, proctored. Do not share exam questions afterwards.

**Away:** Sat 7 to Tue 10 Nov, Sat 14 Nov and Sun 15 Nov (birthday). Revised on Wed 11 Nov because Domain 4 teaching is more detailed (textbook style, theory first). Teaching for CCA-F ends Mon 16 Nov and for CCA-P Fri 20 Nov. Sat 21 is practice questions for both, Sun 22 is weak spots and light review, Mon 23 is rest. Videos: [../videos.md](../videos.md).
