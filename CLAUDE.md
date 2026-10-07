# Weaves

A learn-by-building project. The owner is learning agentic architecture with Claude and preparing for the Claude Certified Architect - Foundations (CCA-F) exam, and builds working projects alongside each topic.

## Goals

- Learn agentic architecture by building small, working examples, not only reading about it.
- Prepare for the CCA-F exam; map each thing built to an exam topic.
- Explain the why behind design choices, since understanding matters more than finishing quickly.

## Exam topics (unverified)

Third-party guides list five domains: agentic architecture, Claude Code configuration, prompt engineering, tool design and MCP, and context management. Sources disagree on weights, so confirm against Anthropic's official exam guide before relying on this list.

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
