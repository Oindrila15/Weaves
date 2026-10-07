# Weaves

A learn-by-building project. The owner, Oindrila, is learning agentic architecture with Claude and preparing for the Claude Certified Architect - Foundations (CCA-F) exam, and builds working projects alongside each topic. Oindrila is a beginner: explain each step plainly.

## Product

Weaves is a directory and knowledge base that connects saree lovers and buyers to handloom weavers: weave, material, weaver, price range, exclusivity, with a source and trust level on every fact. Not a marketplace for now. See `docs/BRD.md` and `docs/open-questions.md`. Currently in the requirements stage; no code yet.

## Rules

- Use Anthropic's official study materials only for exam prep. Never cite third-party exam guides as fact.
- Do not scrape Instagram or any login-gated content. It breaks their terms and risks the owner's account.
- Show a weaver's contact details only with consent.
- Keep documents short and human-readable.

## Goals

- Learn agentic architecture by building small, working examples, not only reading about it.
- Prepare for the CCA-F exam; map each thing built to an exam topic.
- Explain the why behind design choices, since understanding matters more than finishing quickly.

## Exam topics (unverified)

Pending. Anthropic says the exam covers Claude Code, the Claude Agent SDK, the Claude API and MCP. The official exam guide (PDF, via the Anthropic Partner Academy) lists the exact domains; Oindrila will share it. Do not rely on any domain list until then.

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
