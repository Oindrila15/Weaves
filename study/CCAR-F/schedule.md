# CCA-F schedule (hands-on)

Exam: **Monday 21 December 2026** (moved from 24 Nov). Built from Anthropic's official exam guide only (`CCA-F-Exam-Guide.pdf` in this folder, kept local and not in git). See [syllabus-map.md](syllabus-map.md) for all 30 topics in plain language and [notes/](notes/) for revision sheets. Code lives in [day1/](day1/) and [day2/](day2/).

If a day slips, CCA-F comes first until 21 Dec (see [../README.md](../README.md)). Revised on Mon 23 Nov: no study on 23 and 24 Nov, and CCA-P teaching now runs alongside CCA-F (two blocks a day from Wed 25 Nov). Weekends are off. **Guide check (23 Nov):** the new CCAR-F guide v1.1 (November 2026) was compared with v1.0. Content is unchanged (same 5 domains and weights, same task statements); only registration, identification, support and exam-day rules changed. The plan below stands. Both PDFs are kept locally, not in git.

**Method:** each day, learn a domain's ideas, build a small thing that uses them (on saree data, so it is useful for Weaves later), then answer practice questions. Building teaches the *how*; the exam asks *which design is best*, so every day ends with scenario questions.

**What you need:** an Anthropic API key (small spend, a few dollars for the whole week), Python 3, and the `Weaves` repo.

| Day | Date | F block | Build (small, saved to git) | Status |
|---|---|---|---|---|
| 1 | Thu 29 Oct | Domain 1: agentic loop (1.1), hooks (1.5), enforcement (1.4) | Tool-using agent, loop on `stop_reason`, a blocking hook | Done (guide exercise not yet done) |
| 2 | Fri 30 Oct to Tue 3 Nov | Domain 2: tool descriptions, errors, tool counts, MCP | Overlapping tools fixed, structured errors, tiny MCP server | Done |
| 3 | Wed 11 to Fri 20 Nov | Domain 4: 4.1 to 4.4 taught | `day3/ch1` to `ch4` scripts | 4.1 and 4.2 checked 5/5. 4.3 and 4.4 taught, not yet checked |
| | Mon 23 and Tue 24 Nov | **Away, no study** | | |
| 4 | Wed 25 Nov | Domain 4: **Chapter 5 (batch), re-taught**, then Chapter 6 (independent review) | `ch5_batch.py` (built, run once), Chapter 6 script | Ch 5 on hold until here |
| 5 | Thu 26 Nov | Domain 4 practice set. Domain 1: 1.2 and 1.3 (coordinator, subagents) | A coordinator with two subagents | |
| 6 | Fri 27 Nov | Domain 1: 1.6 and 1.7 (task splitting, sessions) | Parallel subagents, cited summary, simulated timeout | |
| 7 | Mon 30 Nov | Domain 3: 3.1 to 3.3 (CLAUDE.md, commands and skills, path rules) | `.claude/rules/` with paths, a skill with `context: fork` | |
| 8 | Tue 1 Dec | Domain 3: 3.4 to 3.6 (plan mode, iterating, CI) | `.mcp.json`, `claude -p` | |
| 9 | Wed 2 Dec | Domain 5: 5.1 to 5.3 | Escalation rules with examples | |
| 10 | Thu 3 Dec | Domain 5: 5.4 to 5.6 | Confidence and review-routing check | |
| 11 | Fri 4 Dec | F practice set: mixed scenarios, all domains | | |
| | Mon 7 Dec | F weak spots. Compare the new CCAR-P guide | | |
| | Wed 9 Dec | F and P mixed practice | | |
| | Thu 10 and Fri 11 Dec | Weak spots and buffer | | |
| | Mon 14 to Thu 17 Dec | Buffer and weak spots | | |
| | Fri 18 Dec | Light review of F, early night | | |
| | Sat 19 and Sun 20 Dec | Rest | | |
| | **Mon 21 Dec** | **Exam** | | |

**Daily routine:** read the day's rows in the syllabus map, build with Claude Code guiding, then 5 to 10 scenario questions. Write weak spots at the bottom of that day's notes file.

**Exam day facts:** government photo ID matching your registration name, a clear desk, no phone or notes, proctored. Do not share exam questions afterwards.

**Away:** Sat 7 to Tue 10 Nov, Sat 14 Nov and Sun 15 Nov (birthday). Revised on Wed 11 Nov because Domain 4 teaching is more detailed (textbook style, theory first). Teaching for CCA-F ends Mon 16 Nov and for CCA-P Fri 20 Nov. Sat 21 is practice questions for both, Sun 22 is weak spots and light review, Mon 23 is rest. Videos: [../videos.md](../videos.md).
