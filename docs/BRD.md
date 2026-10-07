# Weaves: Business Requirements Document

**Version:** 0.5 (draft) · **Owner:** Oindrila · **Date:** 7 October 2026 · **Status:** For review

## 1. The problem

Handloom sarees are made by skilled weavers, but buying directly from them is hard.

- A buyer cannot see a weaver's full collection. Many weavers are not active online.
- A buyer usually has no way to contact the weaver.
- Reliable information is hard to find: the material, how the weave is made, a fair price, how rare the saree is.
- Some knowledge is shared by influencers in Instagram stories, but stories disappear after a day.

The sector is digitally unorganised. Weaves brings this information into one trusted place.

## 2. What Weaves is

A platform that connects saree lovers, buyers and curious readers to weavers. It is a **directory and knowledge base**, not a shop.

- **A map of India.** Click any region to see its weaves, photos and weavers.
- **Community photos.** Visitors can upload photos of themselves in sarees, or of sarees of a given weave. Each is reviewed and labelled as unverified.
- **A knowledge repository** covering handloom weaves across India, built from information available online (summarised, with links back, not copied) and grown through a "Know a weaver?" option anyone can use.
- **A chatbot** that answers questions by searching the knowledge repository (RAG, explained in the glossary) and using only Weaves' own verified information.
- **A website first**, built to work well on phones. An installable app can follow later.
- **Evals and guardrails** across the whole platform, so what it shows and says can be trusted.

Payments and delivery stay between buyer and weaver, outside Weaves.

## 3. Goals

**Product goals**
- Make weaves, weavers and their public profiles easy to find, starting from a map.
- Explain each weave: material, technique, region and exclusivity.
- Give fair price guidance.
- Show where every fact came from and how much to trust it.
- Let people contribute what they know.

**Learning goals** (kept separate on purpose)
- Learn agentic architecture by building Weaves in small steps.
- Prepare for the Claude Certified Architect - Foundations exam using Anthropic's official materials only.

**Success measures.** Weaves is free and does not need to onboard weavers. Success is how much good information it gives out. Starter targets are in [success-targets.md](../knowledge/policies/success-targets.md).

Website measures:
- Footfall (unique visitors) and returning visitors.
- Map clicks, searches and weave pages viewed.
- Chatbot conversations.
- "Know a weaver?" submissions.
- Clicks through to weavers' public profiles.

AI measures (from the eval set, section 8):
- Chatbot answers that are correct and backed by a source.
- Share of answers that stay within the sources (low invented content).
- Whether the right information is found for a question (retrieval hit rate).
- Share of out-of-scope questions correctly declined.
- Accuracy of fields extracted from pages and screenshots.
- Share of bad records the data quality checks catch, and how often they wrongly flag good ones.
- Share of records sent to human review, and how often the person disagrees with the AI.
- Time and cost per chatbot answer.

## 4. Who it is for

| Person | What they need |
|---|---|
| Buyer | Find a genuine saree and the weaver's public profile |
| Knowledge seeker | Learn about weaves, materials and regions |
| Contributor | Add a weaver they know, simply |
| Weaver | Be found without needing to be tech-savvy |
| Influencer or curator | Have their knowledge kept and credited |
| Platform owner (Oindrila) | Keep the information accurate and trusted |

## 5. Scope

**In scope**
- Map of India with all handloom weaves by region, and open-licensed photos.
- A knowledge repository built from online information, searched by the chatbot.
- Weave guide, weaver profiles and links to their public Instagram and Facebook profiles.
- "Know a weaver?" submissions, community photo uploads and an agent that finds candidate weavers from public web sources, with a person approving each one.
- Price and exclusivity guidance.
- Chatbot, data quality checks, evals and guardrails.

**Out of scope for now**
- Payments, shipping and returns.
- Scraping Instagram or Facebook. It breaks their rules and risks Oindrila's accounts.
- Contacting weavers one by one.
- Showing phone numbers without the weaver's consent.

## 6. What Weaves must do

| # | Requirement | Priority |
|---|---|---|
| BR-01 | An interactive map of India. Clicking a region shows its weaves, photos and weavers. | Must |
| BR-02 | Search by weave name, region, material and technique. | Must |
| BR-03 | Each weave page explains the material, the technique and how to tell it is genuine. | Must |
| BR-04 | Each weaver profile shows location, weaves made and links to their public Instagram and Facebook profiles. | Must |
| BR-05 | A phone number or personal contact is shown only after the weaver agrees. | Must |
| BR-06 | Every fact shows its source, the date it was last checked and a trust level. | Must |
| BR-07 | Weaves claiming official recognition (for example a GI tag) are checked against government sources. | Must |
| BR-08 | Photos come only from open licences or the public domain. Each photo shows its licence and credit. | Must |
| BR-09 | Anyone can submit a weaver through "Know a weaver?" with a link, screenshot or note. | Must |
| BR-10 | An agent finds candidate weavers from public web sources. A person approves each one before it is listed. | Should |
| BR-11 | Low-trust information and reports of errors go to a person for review before they are published. | Must |
| BR-12 | Prices appear as ranges, and each weave shows how exclusive it is (common, limited, rare) and why. | Should |
| BR-13 | A chatbot answers questions from Weaves' verified information, cites its sources, and says so when it does not know. | Should |
| BR-14 | A set of test questions and records (evals) is run before each release to measure data extraction, data quality checks and chatbot answers. | Must |
| BR-15 | Guardrails (section 8) apply across the platform. | Must |
| BR-16 | Pages work well on a phone. English only for now. | Should |
| BR-17 | Visitors can upload photos of sarees of a weave, or of themselves in sarees. Each photo is checked, approved by a person and labelled "Community photo, not verified". | Should |

## 7. Where the information comes from

Any publicly available source may be used. Each one is placed in a trust tier (1 official to 5 community), and the tier decides the trust level shown. See [source-tiers-and-trust.md](../knowledge/policies/source-tiers-and-trust.md).

- **Official government pages** (GI registry, handloom brand listings). The reliable base. Exact pages and formats still need to be checked.
- **"Know a weaver?" submissions** from visitors and influencers, credited.
- **Public web search** by the discovery agent. It reads search results and public pages that mention weavers, not Instagram itself. We will check the search tool's terms before building.
- **Open-licensed photo sources**, such as Wikimedia Commons, with licence and credit recorded.
- **Buyers' corrections**.

**Data quality** means checking that records are complete, plausible (for example prices in a sensible range), consistent with official sources, not duplicated and not stale.

## 8. Evals and guardrails

**Evals** are tests we can rerun. Each has real examples with known right answers. They cover three things: whether information is extracted correctly from a screenshot or page, whether the data quality checks catch bad records, and whether the chatbot is correct and sticks to its sources. Results are tracked from release to release so quality does not slip unnoticed.

**Guardrails** are rules the platform must not break:
- The chatbot answers only from verified Weaves information and cites it. No invented prices, weavers or contacts.
- It never gives out a contact that has no consent. It does not certify a particular saree as genuine.
- Content from the web and from users is treated as untrusted. Instructions hidden inside it are ignored.
- Nothing is published from a source that is not credited.
- Personal data is kept to what the platform needs, and a weaver can ask for removal.
- Questions outside saree and handloom topics get a polite redirect.

## 9. Assumptions, risks and constraints

| Risk or assumption | How we handle it |
|---|---|
| Weavers may object to being listed | Link to their public profile only, no contact details, quick removal on request |
| Photos may carry licence conditions | Record the licence for each photo; use only open-licensed or public domain images |
| Maps of India must show official borders correctly | Use an approved boundary source and check Indian map rules before launch |
| The chatbot gives wrong or invented answers | Answer from verified data only, cite sources, test with evals |
| Web content tries to trick the chatbot | Treat all outside content as untrusted |
| Uploaded photos show people without consent, are not the uploader's, or are unsuitable | Uploader declarations, automated check plus human approval, no strangers or children, removal within 48 hours, legal check |
| The discovery agent finds the wrong people | A person approves every candidate |
| Information from the web is copied or wrong | Store short summaries with links back, not whole articles; check sources and show trust levels |
| "All of India" is a large job | Build outward from officially recognised weaves; show gaps honestly |
| Legal and privacy problems | Consent first, no scraping, legal review before launch |
| The project grows into a marketplace | Keep the first release as a directory |

Constraint: Oindrila is a beginner, so every build step needs a plain explanation.

## 10. Phases

- **Phase 1:** map, weave guide starting with officially recognised weaves (GI tags) and widening to all Indian handlooms, weaver profiles with public links, open photos, "Know a weaver?", human review, first evals and guardrails.
- **Phase 2:** discovery agent, chatbot, community photo uploads, price and exclusivity guidance, expanded evals.
- **Phase 3:** weavers connect their own Instagram, influencer partnerships, buyer enquiries, installable app, more languages if wanted.

The technical design (agents, tools, hosting) comes after this document is agreed.

## 11. Open questions

See [open-questions.md](open-questions.md).

Community photo rules are in [community-photos.md](../knowledge/policies/community-photos.md). Rules and policies live in the knowledge repository, in [knowledge/policies](../knowledge/README.md). They are updated whenever a rule or a source's terms change.

## 12. Glossary

- **Agent:** a program where Claude decides which steps to take and which tools to use.
- **Chatbot:** an agent you talk to, here limited to answering from Weaves' verified information.
- **Evals:** repeatable tests that measure how well the system works.
- **RAG:** the chatbot first searches the knowledge repository for the most relevant passages, then writes its answer from them.
- **Guardrails:** rules the system must not break.
- **GI tag:** an official label linking a product, such as Kancheepuram silk, to its place of origin.
- **Trust level:** how confident we are in a fact, based on its source and age.
