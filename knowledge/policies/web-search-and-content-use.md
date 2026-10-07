# Web search and content use

**Last checked:** 7 October 2026 · **Review when:** the search tool's price or terms change, or before launch (legal check).

## Search tool

The discovery agent and knowledge builder use the Claude API's web search tool, which costs $10 per 1,000 searches plus normal token costs. The web fetch tool adds no fee beyond tokens. [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) · [Web search tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/web-search-tool)

- Search budget: at most 1,000 searches per month (see [budget.md](budget.md)).
- Fetch only pages that came up in search or that we picked by hand. Respect each site's robots.txt and never get around paywalls or logins.
- Never fetch Instagram or Facebook pages (see [meta-platforms.md](meta-platforms.md)).

## Using other websites' content

- **Summarise in our own words.** Do not copy articles, tables or photos wholesale.
- Quote at most one short sentence, always with credit and a link.
- Every fact keeps: title, publisher, link, date accessed.
- Store extracted facts and short notes, not full copies of pages.
- Government data: check each dataset's licence before reuse and record it.
- Remove content within 48 hours of a valid request.
- Indian copyright law allows only limited "fair dealing", so we rely on summaries and links. **Legal check before launch.**

## AI-written content

Weave pages written by Claude are labelled as AI-assisted and reviewed by a person when trust is low. The chatbot says it is an AI.
