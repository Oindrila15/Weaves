# Weaves

A learn-by-building project. The owner, Oindrila, is learning agentic architecture with Claude and preparing for the Claude Certified Architect - Foundations (CCA-F) exam, and builds working projects alongside each topic. Oindrila is a beginner: explain each step plainly.

## Product

Weaves is a directory and knowledge base that connects saree lovers and buyers to handloom weavers: weave, material, weaver, price range, exclusivity, with a source and trust level on every fact. Not a marketplace for now. See `docs/BRD.md` and `docs/open-questions.md`. Website first (works on phones), installable app later. English only. Free to use. Budget cap: $50 per month in total. Currently in the requirements stage; no code yet.

## Rules

- Use Anthropic's official study materials only for exam prep. Never cite third-party exam guides as fact.
- Do not scrape Instagram or any login-gated content. It breaks their terms and risks the owner's account.
- Show a weaver's contact details only with consent.
- Keep documents short and human-readable.
- Policies and rules live in `knowledge/policies/`. When a rule or a source's terms change, update the policy file (including its Last checked date) and add a line to `knowledge/CHANGELOG.md`. Follow them when building.

## Goals

- Learn agentic architecture by building small, working examples, not only reading about it.
- Prepare for the CCA-F exam; map each thing built to an exam topic.
- Explain the why behind design choices, since understanding matters more than finishing quickly.

## Exam topics (from Anthropic's official exam guide, v1.0, July 2026, code CCAR-F)

60 questions, 120 minutes, proctored, pass mark 720 of 1,000, fee $125. Four scenarios are drawn from a bank of six.

| Domain | Weight |
|---|---|
| 1. Agentic Architecture & Orchestration | 27% |
| 2. Tool Design & MCP Integration | 18% |
| 3. Claude Code Configuration & Workflows | 20% |
| 4. Prompt Engineering & Structured Output | 20% |
| 5. Context Management & Reliability | 15% |

The six scenarios: customer support agent, code generation with Claude Code, multi-agent research system, developer productivity tools, Claude Code in CI/CD, structured data extraction. Weaves maps best to the multi-agent research, structured extraction and customer support (chatbot) scenarios. The guide is public on the Anthropic Partner Academy; the PDF is not stored in this repo.

## Stack and conventions

To be decided as the plan firms up.

## Git workflow

- Repo: https://github.com/Oindrila15/Weaves (public, branch `main`, remote `origin`).
- After each logical chunk of work, commit and push so there is always a saved version to revert to.
- Stage specific files, not `git add -A`, so nothing sensitive is picked up.
- Commit messages: short imperative subject (about 50 characters), blank line, then a body explaining why when it helps.
- After each push, tell the user the commit hash so they can undo it with `git revert <hash>`.
- Never force-push or rewrite history without explicit approval.
- The repo is public: never commit secrets, API keys or `.env` files.
