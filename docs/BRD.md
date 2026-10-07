# Weaves: Business Requirements Document

**Version:** 0.1 (draft) · **Owner:** Oindrila · **Date:** 7 October 2026 · **Status:** For review

## 1. The problem

Handloom sarees are made by skilled weavers, but buying directly from them is hard.

- A buyer cannot see a weaver's full collection. Many weavers are not active online.
- A buyer usually has no way to contact the weaver.
- Reliable information is hard to find: what the material is, how the weave is made, what a fair price is, and how rare the saree is.
- Some knowledge is shared by influencers in Instagram stories, but stories disappear after a day. Miss one and the information is gone.

The sector is digitally unorganised. Weaves brings this information into one trusted place.

## 2. What Weaves is

A platform that connects saree lovers, buyers and curious readers to weavers. It is a **directory and knowledge base**, not a shop. People find a weave, learn about it, see who makes it, and get in touch with the weaver. Payments and delivery happen between buyer and weaver, outside Weaves.

## 3. Goals

**Product goals**
- Make a weaver's collection, weave type and contact easy to find.
- Explain each weave: material, technique, region and exclusivity.
- Give fair price guidance.
- Show where every fact came from and how much to trust it.

**Learning goals** (kept separate on purpose)
- Learn agentic architecture by building Weaves in small steps.
- Prepare for the Claude Certified Architect - Foundations exam using Anthropic's official materials only.

**How we will measure success.** Targets are still to be agreed with Oindrila. Suggested measures:
- Number of weavers listed with consent.
- Share of records that show a source and a trust level.
- Number of buyer enquiries sent to weavers.
- Share of records that pass the data quality checks.

## 4. Who it is for

| Person | What they need |
|---|---|
| Buyer | Find a genuine saree, see the price range, contact the weaver |
| Knowledge seeker | Learn about weaves, materials and regions |
| Weaver | Be found by buyers without needing to be tech-savvy |
| Influencer or curator | Have their knowledge kept and credited, not lost after 24 hours |
| Platform owner (Oindrila) | Keep the information accurate and trusted |

## 5. Scope

**In scope for the first release**
- Weave guide (material, technique, region, official recognition such as GI tags).
- Weaver profiles with collection, price range and contact.
- Price and exclusivity guidance.
- Data quality checks on everything shown.
- Contact details shown only with the weaver's consent.

**Out of scope for now**
- Payments, shipping and returns.
- Automatic scraping of Instagram. It breaks Instagram's rules, stories need a login, and it puts Oindrila's account at risk.

## 6. What Weaves must do

| # | Requirement | Priority |
|---|---|---|
| BR-01 | Visitors can browse and search weaves by name, region, material and technique. | Must |
| BR-02 | Each weave page explains the material, the technique and how to tell it is genuine. | Must |
| BR-03 | Each weaver has a profile showing location, weaves made and collection. | Must |
| BR-04 | A weaver's contact is shown only after the weaver has agreed. | Must |
| BR-05 | Buyers can send an enquiry to a weaver. | Must |
| BR-06 | Every fact shows its source, the date it was last checked and a trust level. | Must |
| BR-07 | Weaves claiming official recognition (for example a GI tag) are checked against government sources. | Must |
| BR-08 | Prices are shown as ranges with a short note on what affects them. | Should |
| BR-09 | Each weave shows how exclusive it is (common, limited or rare) and why. | Should |
| BR-10 | Information with low trust is held for a person to review before it is published. | Must |
| BR-11 | Buyers can report wrong or outdated information. | Should |
| BR-12 | Pages work well on a phone and offer English plus at least one regional language. | Should |

**Example of success for BR-06:** a weaver's price range displays "Source: weaver, checked 3 Oct 2026, trust: high".

## 7. Where the information comes from

- **Official government pages** (such as GI registry and handloom brand listings). This is the reliable base. The exact pages and formats still need to be checked.
- **Weavers directly**, for example by sending photos and a voice note on WhatsApp. Claude turns them into a record and a person confirms it.
- **Influencers, with their permission**, or screenshots and links that users submit from public posts, which Claude reads and a person confirms.
- **Buyers**, who report corrections.

**Data quality** means checking that records are complete, plausible (for example prices within a sensible range), consistent with official sources, not duplicated and not stale.

## 8. Quality, privacy and trust

- **Accuracy:** nothing is shown as fact without a source.
- **Freshness:** old prices lose trust over time and are flagged.
- **Privacy:** a weaver's phone number is personal data. India's Digital Personal Data Protection Act, 2023 applies. Check the exact obligations with a lawyer before launch.
- **Credit:** influencer content is credited and used only with permission.

## 9. Assumptions, risks and constraints

| Risk or assumption | How we handle it |
|---|---|
| Weavers may not want to be listed or may not trust a new platform | Start with a few willing weavers, always ask consent, make joining simple |
| Fake "handloom" sarees damage trust | Check against official sources and show trust levels |
| Government data may be incomplete or hard to read | Verify early, and fall back to manual entry |
| Legal or privacy problems | Consent first, no scraping, legal review before launch |
| The project grows into a full marketplace | Keep the first release as a directory |
| Learning and product goals compete for time | Build in small steps; each step teaches one exam topic |

Constraint: Oindrila is a beginner, so every build step needs a plain explanation.

## 10. Phases

- **Phase 1 (MVP):** weave guide and weaver profiles for a small starting set of weaves and weavers, with source and trust shown.
- **Phase 2:** price and exclusivity guidance, buyer enquiries, human review queue.
- **Phase 3:** influencer partnerships, more regions and languages, possible revenue ideas such as featured listings.

The technical design (agents, tools, hosting, app or website) comes after this document is agreed.

## 11. Open questions

See [open-questions.md](open-questions.md).

## 12. Glossary

- **Agent:** a program where Claude decides which steps to take and which tools to use to finish a task.
- **GI tag:** an official label linking a product, such as Kancheepuram silk, to its place of origin.
- **BRD:** this document; it says what the business needs, not how to build it.
- **Trust level:** how confident we are in a fact, based on its source and age.
