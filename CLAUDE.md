# Weaves

Project in planning. Goals, stack and conventions will be added here as the plan firms up.

## Git workflow

- Repo: https://github.com/Oindrila15/Weaves (public, branch `main`, remote `origin`).
- After each logical chunk of work, commit and push so there is always a saved version to revert to.
- Stage specific files, not `git add -A`, so nothing sensitive is picked up.
- Commit messages: short imperative subject (about 50 characters), blank line, then a body explaining why when it helps.
- After each push, tell the user the commit hash so they can undo it with `git revert <hash>`.
- Never force-push or rewrite history without explicit approval.
- The repo is public: never commit secrets, API keys or `.env` files.
