# CCA-P syllabus map

Plain-language summary of Anthropic's official exam guide (Claude Certified Architect - Professional, CCAR-P, v1.0, July 2026). The guide is the authority; the PDF is not stored in this repo. The objective names below come from the guide. The "In plain words" column is our own explanation and must be checked against Anthropic's official documentation when we study each topic.

**Exam:** 63 questions, 120 minutes, multiple choice and multiple response (each question says how many answers to pick), proctored (online or Pearson VUE test centre), pass mark 720 on a 100 to 1,000 scale, fee $175. The credential is valid for 12 months, then renewed with a free assessment. The score report shows percent correct per domain, but pass or fail uses the total score only.

**Who it is for:** mid- to senior-level people who design and deliver production AI systems. The guide recommends 3+ years in systems architecture and 6+ months with Claude or similar systems in production. These are recommendations, not requirements.

**The pattern in the three sample questions:** each answer is a proportionate fix aimed at the real cause. Least privilege: remove unneeded tools, do not just log or confirm them. Repeated static prompt: put it first and use prompt caching. Confident but wrong answers after a document refresh: check retrieval and indexing first.

## How it relates to CCA-F

| P domain | Weight | Overlap with CCA-F |
|---|---|---|
| 1 Solution Design & Architecture | 17% | Partly: multi-agent and decomposition (F 1.2, 1.6). New: business framing, choosing a pattern |
| 2 Models, Prompting & Context | 13% | Partly: few-shot, context (F 4.2, 5.1). New: model choice, chain-of-thought, prompt caching |
| 3 Integration | 19% | Partly: tool count, MCP (F 2.3, 2.4). New: security, observability, **RAG** |
| 4 Evaluation, Testing & Optimization | 16% | Mostly new |
| 5 Governance, Safety & Risk | 14% | Partly: hooks, human review (F 1.5, 5.5). New: regulations, ethics |
| 6 Stakeholder Communication & Lifecycle | 14% | All new |
| 7 Developer Productivity | 7% | Mostly covered by F Domain 3 |

RAG, embeddings and prompt caching are **not** on CCA-F but **are** on CCA-P.

## Domain 1: Solution Design & Architecture (17%)

| # | Objective (from the guide) | In plain words |
|---|---|---|
| 1.1 | Translate business problems into Claude-based solutions | Turn a vague need into a clear problem, inputs, outputs and a way to measure success |
| 1.2 | Design end-to-end architectures (input, processing, output, feedback loops) | Draw the whole path, including how results flow back to improve the system |
| 1.3 | Select patterns: workflow, agentic, augmented LLM | Fixed steps, a model-driven loop, or one model call with added tools or data. Pick the simplest that works |
| 1.4 | Design multi-agent systems and orchestration | Coordinator and subagents (see F 1.2, 1.3) |
| 1.5 | Apply decomposition techniques | Split a big problem into parts (see F 1.6) |
| 1.6 | Align to business value (efficiency, transformation, productivity, cost, performance SLAs) | Say what the business gains and the promised speed or quality |

## Domain 2: Claude Models, Prompting & Context Engineering (13%)

| # | Objective | In plain words |
|---|---|---|
| 2.1 | Select Claude models based on trade-offs | Bigger models cost more and are slower; match the model to the task |
| 2.2 | Design system prompts, templates and guardrails | Standing instructions, reusable prompt shapes, and limits on behaviour |
| 2.3 | Apply zero-shot, few-shot and chain-of-thought | No examples, examples, and asking for step-by-step reasoning |
| 2.4 | Optimise context windows and token use | Send only what is needed, in a good order |
| 2.5 | Prompt reuse: caching, modular prompts, Skills | Reuse stable parts instead of resending and repaying for them |

## Domain 3: Integration (19%)

| # | Objective | In plain words |
|---|---|---|
| 3.1 | Evaluate tool and agent configuration for capability bloat | Too many tools or permissions make an agent worse and riskier |
| 3.2 | Analyse authentication and authorisation to find security gaps | Who is allowed to do what, and where that breaks |
| 3.3 | Evaluate accuracy-latency trade-offs | Faster or cheaper setups can be less accurate; justify the choice |
| 3.4 | Analyse observability at scale and choose monitoring | Logs and metrics so you can see what the system is doing |
| 3.5 | Design a RAG pipeline: chunking and indexing | Cut documents into pieces, index them, retrieve the relevant ones for Claude |
| 3.6 | Match retrieval strategy to data shape and query pattern | Different data and questions need different search methods |
| 3.7 | Choose a connection protocol: MCP, API/CLI, agent-to-agent | Pick how Claude connects to other systems |
| 3.8 | Progressive discovery vs one big context | Load detail on demand, or put everything in at once |

## Domain 4: Evaluation, Testing & Optimization (16%)

| # | Objective | In plain words |
|---|---|---|
| 4.1 | Define metrics: accuracy, latency, cost, safety, security | Decide what "good" means, in numbers |
| 4.2 | Design evaluation datasets and test frameworks, mixed methods | Test questions with known answers, run automatically and reviewed by people |
| 4.3 | Run A/B tests and iterate | Compare two versions on real or test traffic |
| 4.4 | Diagnose prompt failure, hallucination, model mismatch | Find the real cause before fixing |
| 4.5 | Optimise tokens, latency and cost | Reduce spend and wait time without losing quality |
| 4.6 | Monitor with logging and observability tools | Watch the live system |

## Domain 5: Governance, Safety & Risk Management (14%)

| # | Objective | In plain words |
|---|---|---|
| 5.1 | Implement guardrails and safety controls | Rules enforced around the model (see F 1.5) |
| 5.2 | Identify risks, limits and failure modes | What can go wrong and how it shows up |
| 5.3 | Apply human-in-the-loop validation | A person checks the risky or uncertain cases (see F 5.5) |
| 5.4 | Ensure compliance (for example GDPR, HIPAA, FedRAMP) | Meet legal and regulatory rules for data |
| 5.5 | Address ethics: bias, fairness, transparency | Treat people fairly and be open about how it works |

## Domain 6: Stakeholder Communication & Lifecycle Management (14%)

| # | Objective | In plain words |
|---|---|---|
| 6.1 | Structured discovery and requirement gathering | Ask the right questions up front |
| 6.2 | Communicate decisions and trade-offs | Explain why, and what was given up |
| 6.3 | Manage feedback loops and expectations, including SLAs | Keep people aligned on what will be delivered |
| 6.4 | Document architectures and give implementation guidance | Write it down so others can build it |
| 6.5 | Support lifecycle phases: discovery, design, handoff, monitoring, iteration | The whole life of the system, not just the build |

## Domain 7: Developer Productivity & Operational Enablement (7%)

| # | Objective | In plain words |
|---|---|---|
| 7.1 | Configure Claude tools and environments for teams (for example Claude Code) | See F Domain 3 |
| 7.2 | Improve developer workflows with AI tooling | Use the tools to make teams faster |
| 7.3 | Support debugging and operational issue resolution | Use Claude to find and fix problems |

## Exam policies in the guide
- Cancel or reschedule up to 24 hours before the appointment. Changes inside 24 hours forfeit the fee.
- Retakes: wait 14 days after the first fail, 30 after the second, 90 after the third. Up to four attempts in a rolling 12 months. The fee applies each time.
- Government photo ID, with the name matching your registration exactly. No phone, notes or watch. Do not share exam content.
