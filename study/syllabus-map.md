# CCA-F syllabus map

Plain-language summary of Anthropic's official exam guide (CCAR-F, v1.0, July 2026). The guide itself is the authority: https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification

**Exam:** 60 questions, 120 minutes, multiple choice and multiple response, pass mark 720 of 1,000. Four scenarios are picked at random from six: customer support agent, Claude Code for development, multi-agent research system, developer productivity tools, Claude Code in CI/CD, structured data extraction.

**The pattern in the sample questions:** the right answer is usually the *proportionate, root-cause fix*. Programmatic enforcement beats prompt instructions when rules must always hold. Better tool descriptions beat extra infrastructure. Over-engineered answers (classifiers, routing layers, bigger models) are usually wrong.

## Domain 1: Agentic Architecture & Orchestration (27%)

| # | Topic | Remember |
|---|---|---|
| 1.1 | Agentic loop | Keep looping while `stop_reason` is `tool_use`: run the tool, append the result, call again. Stop on `end_turn`. Never decide completion by reading the text or by an iteration cap alone |
| 1.2 | Coordinator and subagents | Hub-and-spoke: the coordinator splits the task, delegates, merges results, and all communication goes through it. Subagents do not inherit its context. Too-narrow splitting causes coverage gaps |
| 1.3 | Spawning subagents | The Task tool, and `allowedTools` must include `"Task"`. Pass needed context in the prompt. Parallel subagents come from several Task calls in one response. Give goals, not step-by-step scripts |
| 1.4 | Enforcement and handoffs | When an order of steps must always hold, block with code (a prerequisite), not a prompt. Escalations carry a structured summary because the human cannot see the chat |
| 1.5 | Hooks | PostToolUse hooks clean up tool results before the model sees them. Pre-call hooks block rule-breaking calls (for example a refund over $500) and redirect. Hooks give guarantees; prompts give probabilities |
| 1.6 | Task decomposition | Prompt chaining (fixed steps) for predictable work; adaptive plans for open-ended work. Big reviews: one pass per file, then a cross-file pass |
| 1.7 | Sessions | `--resume <name>` to continue; `fork_session` to branch. If old tool results are stale, start fresh with a summary |

## Domain 2: Tool Design & MCP Integration (18%)

| # | Topic | Remember |
|---|---|---|
| 2.1 | Tool descriptions | The description is how Claude chooses a tool. Include inputs, examples, edge cases and when *not* to use it. Rename or split overlapping tools. Watch system-prompt keywords that bias choice |
| 2.2 | Error responses | Use the MCP `isError` flag with a category (transient, validation, business, permission) and `isRetryable`. A failure is not the same as a valid empty result. Recover locally first, then pass up with partial results |
| 2.3 | Tools per agent | 4 to 5 focused tools beat 18. Give each agent only its role's tools. `tool_choice`: `auto`, `any` (must call a tool), or forced (a named tool) |
| 2.4 | MCP in Claude Code | Project `.mcp.json` (shared, with `${ENV_VAR}` for secrets); personal `~/.claude.json`. All servers' tools are available at once. Resources expose catalogs. Prefer existing community servers for standard systems |
| 2.5 | Built-in tools | Grep searches contents; Glob matches file names; Read/Write whole files; Edit needs unique text (fall back to Read + Write) |

## Domain 3: Claude Code Configuration & Workflows (20%)

| # | Topic | Remember |
|---|---|---|
| 3.1 | CLAUDE.md | User (`~/.claude/CLAUDE.md`, not shared), project, directory levels. `@import` for modularity, `.claude/rules/` for topics, `/memory` to see what loaded |
| 3.2 | Commands and skills | `.claude/commands/` is shared via git; `~/.claude/commands/` is personal. Skills (`SKILL.md`) support `context: fork`, `allowed-tools`, `argument-hint`. Skills are on demand; CLAUDE.md is always loaded |
| 3.3 | Path rules | `.claude/rules/*.md` with `paths:` globs load only for matching files. Best for conventions spread across folders (for example all test files) |
| 3.4 | Plan mode | Plan for big, architectural, multi-file work. Direct execution for small, clear changes. Explore subagent keeps noisy discovery out of the main context |
| 3.5 | Iterating | 2 to 3 input/output examples beat prose. Tests first. Interview pattern. Send interacting problems together; independent ones one by one |
| 3.6 | CI/CD | `-p` for non-interactive; `--output-format json` with `--json-schema`; CLAUDE.md supplies context. A fresh instance reviews better than the one that wrote the code. Pass earlier findings to avoid duplicates |

## Domain 4: Prompt Engineering & Structured Output (20%)

| # | Topic | Remember |
|---|---|---|
| 4.1 | Explicit criteria | Name what to report and what to skip. "Be conservative" does not work. Give severity levels with examples. Turn off noisy categories to keep trust |
| 4.2 | Few-shot | 2 to 4 examples for ambiguous cases, with the reasoning. They fix format and cut hallucination in extraction |
| 4.3 | Structured output | `tool_use` with a JSON schema. It removes syntax errors, not meaning errors. Make fields nullable when the source may not have them. Use enums with `"unclear"` and `"other"` + detail |
| 4.4 | Validate and retry | Retry with the document, the failed output and the specific error. Retrying cannot create information the source lacks. Check meaning (calculated vs stated total) |
| 4.5 | Batch API | 50% cheaper, up to 24 hours, no latency promise, `custom_id` to match results, no multi-turn tool calls. Only for non-blocking work. Resubmit only failures |
| 4.6 | Multi-pass review | A model is poor at reviewing its own work in the same session. Use an independent instance. Per-file passes plus an integration pass |

## Domain 5: Context Management & Reliability (15%)

| # | Topic | Remember |
|---|---|---|
| 5.1 | Context | Keep a "case facts" block (amounts, dates, IDs) outside summaries. Summaries lose numbers. Models miss the middle of long inputs, so put key points first. Trim tool output to relevant fields |
| 5.2 | Escalation | Explicit criteria plus examples. Honour a request for a human immediately. Escalate policy gaps. Several matches means ask for an identifier. Sentiment and self-reported confidence are unreliable |
| 5.3 | Error propagation | Send structured context (type, query, partial results, alternatives). Do not hide errors as empty successes and do not kill the whole workflow. Note coverage gaps |
| 5.4 | Large codebases | Long sessions degrade. Use scratchpad files, subagents for noisy exploration, manifests for crash recovery, and `/compact` |
| 5.5 | Human review | Overall accuracy can hide weak segments. Sample high-confidence items at random. Calibrate field-level confidence with labelled data. Send low confidence to people |
| 5.6 | Provenance | Keep claim-to-source mappings through summaries. Show conflicting values with sources instead of picking one. Require dates |

## Not on the exam

Fine-tuning, API keys and billing, hosting MCP servers, Claude's internals and safety training, **embedding models and vector databases**, computer use, **image/vision analysis**, streaming, rate limits and **pricing**, OAuth, cloud setup, benchmarks, prompt caching details, tokenisation.

**What this means for Weaves:** the RAG search, screenshot reading, hosting and cost planning are valuable for the product but will not be tested. For the exam, focus on the agent loop, tool design, structured extraction, multi-agent orchestration, hooks, escalation, provenance and Claude Code configuration.
