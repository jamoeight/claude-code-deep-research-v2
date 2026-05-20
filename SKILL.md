---
name: Deep Research
description: >
  Multi-agent research system (v2). Orchestrator-worker spine from Anthropic's
  Nov-2025 baseline, scaled with post-Nov-2025 SOTA: AggAgent synthesis
  (replaces flat synthesis, +10.3 pp on deep-research tasks), DRA Failure
  Rubric verification, heterogeneous-judge debate panels, BrowseConf confidence
  retry, BATS budget tracker, Skills + ToolSearch + Code-Execution-with-MCP
  (context-cost stack: -85% to -98%). Three modes selectable at Phase 0 —
  STANDARD (synthesis, the default), DISCOVERY (Co-Scientist 6-agent Elo
  tournament for novel hypothesis generation, Aletheia G/V/R fallback with
  explicit reject branch), GENERATOR-EVALUATOR (AlphaEvolve / OpenEvolve
  template for sub-questions with programmable evaluators).
  Triggers on research requests, competitive analysis, market trends,
  fact-checking, novel hypothesis generation, algorithm / prompt / code
  optimization, and any query needing multi-source investigation.
version: 2.0
upstream-skill: deep-research v1 (preserved at ~/.claude/skills/deep-research-old/)
globs:
  - "files/research_notes/**"
  - "files/research_session_*/**"
  - "files/reports/**"
  - "files/charts/**"
  - "files/data/**"
---

# Deep Research System v2

**Default for research / synthesis / discovery / evaluator-driven search.**
The v1 baseline (Nov 2025 orchestrator-worker) is preserved at
`~/.claude/skills/deep-research-old/` for A/B comparison; the user invokes
`deep-research-old` explicitly when they want the legacy behavior.

**Derived from:** 9 researcher notes + data summary in `files/research_notes/`
and `files/data/` produced 2026-05-20 from a Nov 2025 → May 2026 sweep of
Anthropic, OpenAI, DeepMind, open-source frameworks, and the multi-agent /
context-engineering / TTC / benchmarks literature.
**Why this exists:** The harness is now the product. Same model can vary 6× in
performance by harness alone. The cluster of post-Nov-2025 advances —
AggAgent, DRA Failure Rubric, Skills + ToolSearch, Code Execution with MCP,
Aletheia G/V/R, Co-Scientist 6-agent Elo tournament, asymmetric verification,
trajectory compression, adaptive per-step effort, durable memory, prompt-cache
discipline — stacks on the v1 spine for measurable lift in research richness
*and* unlocks novel-discovery capability v1 could not reach.

---

## Changelog vs v1 (read this first)

| # | Edit | Source finding (note-id) | Expected effect |
|---|------|--------------------------|-----------------|
| C1 | **Mode selection**: Standard / Discovery / Generator-Evaluator chosen in Phase 0 | R3 (DeepMind discovery stack), R4-F25, R8-OpenEvolve | Skill can now reach novel-discovery problem classes (math, code, hypothesis) instead of only synthesis |
| C2 | **Aggregator role** added (replaces flat synthesis at end of Phase 2 fan-in) | R4-F34 AggAgent | +5-10 pp on deep-research tasks; eliminates context-blowup and majority-vote dilution |
| C3 | **Verifier-Agent role** added (DRA Failure Rubric scoring) | R4-F8, R6-F51 DeepVerifier | +8-11 pp on GAIA hard; catches the 13 known agent failure modes before final synthesis |
| C4 | **Heterogeneous judge panel** for contested claims (3 judges, distinct model families) | R4-F5 PROClaim, R4-F6 A-HMAD | +10 pp on Check-COVID-style fact-check; anti-collusion through model-family diversity |
| C5 | **Generator-Evaluator sub-loop** (OpenEvolve template) for verifiable sub-questions | R3 AlphaEvolve, R4-F25, R8-OpenEvolve | Sub-questions with programmable evaluators now solved by search, not single-shot guess |
| C6 | **Discovery Mode** = Co-Scientist 6-agent stack (Generation / Proximity / Reflection / Ranking / Evolution / Meta-review + Supervisor) with Elo tournament | R3 Co-Scientist, R3 Aletheia | Unlocks novel-hypothesis generation; produces a *ranked* set of falsifiable hypotheses |
| C7 | **Aletheia G/V/R triplet** with explicit "I cannot resolve" reject branch for ambiguous synthesis | R3 Aletheia | Prevents fabricated synthesis on questions the evidence base cannot support |
| C8 | **BrowseConf confidence elicitation + retry** for low-confidence researcher findings | R6-F50 BrowseConf | Self-paced retries with Summary / Neg variants until confidence > τ* |
| C9 | **BATS budget tracker** injected after every researcher tool call | R6-F25 BATS | -40% tool calls, -31% cost at matched accuracy; explicit CONTINUE / PIVOT decision point |
| C10 | **Ares-style per-step adaptive effort** (low/med/high/xhigh) per researcher | R6-F24 Ares | -41 to -53% reasoning cost at matched accuracy |
| C11 | **TrACE adaptive sampling** at every uncertain agent step (sample N, commit on agreement) | R6-F39 TrACE | -33% to -65% LLM calls, free win (no training, no verifier) |
| C12 | **Trajectory compression** for late-wave / discovery rollouts | R6-F49 (Apr 2026) | +6.7 pp SWE-Bench, +12.2 pp Terminal-Bench; enables tournament voting across rollouts |
| C13 | **Skills + ToolSearch** with `defer_loading: true` on every researcher | R1-SDK1, R1-SDK2, R5-F19, R5-F20 | -85% tokens on multi-MCP setups; preserves prompt cache |
| C14 | **Code Execution with MCP** wrapper for high-token MCP servers | R1-SDK3, R5-F23 | -98.7% tokens (150K → 2K) on the Drive-to-Salesforce-class case |
| C15 | **clear_tool_uses_20250919** on researcher subagents at `trigger=30_000`, `keep=4` | R5-F8 | Drops WebFetch bodies once findings extracted; 335K → 173K peak |
| C16 | **compact_20260112** on orchestrator at 40% of window | R5-F7, R5-F11 | Compact before rot, not at limit |
| C17 | **Shared `/memories/research_session_<id>/`** for orchestrator + all researchers | R1-CTX3, R5-F6 | Cross-researcher knowledge fabric; pointer-based handoff |
| C18 | **File-only orchestrator ↔ researcher comms** after kickoff (`task.md` → `result.md`) | R5-F13, R5-F25 | Orchestrator context never receives raw researcher trace |
| C19 | **Byte-identical researcher system prompts** for prompt-cache hit | R5-F16 "Don't Break the Cache" | -41 to -80% cost on the cached prefix |
| C20 | **WebFetch wrapper** archives to disk, returns 10-line preview | R5-F28 (LangChain Deep Agents) | Researcher context lean; full pages reachable via grep |
| C21 | **Three-tier model routing**: Opus 4.7 lead, Opus 4.7 / Sonnet 4.6 workers, Haiku 4.5 narrow / verifier, Sonnet 4.6 writer | R1-M5, R8 routing | -51% cost vs uniform Opus per the industry numbers |
| C22 | **Tree-GRPO-style branching** when sampling N rollouts of the same researcher | R6-F9 | Shared prefixes amplify rollouts within budget; +69% rel on agent tasks |
| C23 | **Heterogeneous-model fallback** for ensemble queries when budget permits (Claude + GPT + Gemini in panel) | R4-F6 A-HMAD, R6-F19 ModelSwitch | Wisdom-of-crowd; anti-collusion |
| C24 | **Anti-collusion safety pass**: Petri-style audit before final delivery (multi-agent collusion sanity check) | R1-AL1, R1-AL2 "AI Orgs more effective but less aligned" | Mitigates the multi-agent alignment-regression caveat |
| C25 | **Inverse-entropy weighted voting** in any self-consistency aggregation | R6-F15 | +46.7% accuracy in 95.6% of configs vs uniform majority |
| C26 | **Dream phase** (optional, post-run) — pattern extraction to skill memory across sessions | R1-MA4 Anthropic Dreaming | Cross-session improvement; Harvey reported 6× completion-rate gain |
| C27 | **Stopping criteria** made explicit | R4-F2 "no RL method for when to stop" | Removes the heuristic ambiguity; lets future runs A/B test |
| C28 | **Model policy enforced via frontmatter** (`effort`, `model`, `isolation`, `memory`, `background`) per researcher | R1-SDK4 subagent frontmatter | Per-researcher knobs without per-task code |
| C29 | **Effective-but-less-aligned caveat** stated explicitly in prompts; bounded by audit step | R1-AL2 | Operator awareness; do not hide the trade-off |
| C30 | **Inverse-scaling-aware effort caps** (don't crank thinking on distractor-heavy tasks) | R6-F27 Anthropic Inverse Scaling | Prevents the DeepSeek-R1 70% → 30% failure mode |

These 30 edits compose. The skill keeps v1's 6-phase spine and adds modes, roles, and primitives on top.

---

## Agent Roles (v2 expansion)

You coordinate up to **nine** specialized subagents via the **Agent tool**. Roles marked NEW are introduced in v2.

| Role | Model | Tools | Purpose | New? |
|------|-------|-------|---------|------|
| **Lead Coordinator** (you) | Opus 4.7 (`effort=xhigh`) | Agent, Read, Write, Glob, Grep, Bash | Plan, delegate, gap-analyze, decide modes, run audit | — |
| **Researcher** | Opus 4.7 (`effort=high` default; Ares-router adjusts per step) | WebSearch, WebFetch, Write, Read, Bash, Skills (curated) | Search, gather, write structured findings to `files/research_notes/N_*.md` | — |
| **Verifier-Agent** | Opus 4.7 (`effort=high`) | Read, Glob, Grep, WebFetch | Score each researcher's findings against the DRA Failure Rubric (5 cat / 13 sub); emit corrective feedback | **NEW (C3)** |
| **Judge Panel (×3)** | One Claude (Opus 4.7), one GPT (5.5 Pro), one Gemini (3.1 Pro) when available; else 3 distinct Opus 4.7 prompts | Read, WebFetch | Adversarial vote on contested claims (PROClaim-style courtroom; or single-turn pairwise for cheap pairs) | **NEW (C4)** |
| **Aggregator** | Opus 4.7 (`effort=xhigh`) | Read, Glob, Grep + AggAgent tools (`get_solution`, `search_trajectory`, `get_segment`, `finish`) | Replaces flat synthesis; treats researcher trajectories as an interrogable environment | **NEW (C2)** |
| **Data Analyst** | Opus 4.7 | Read, Glob, Bash, Write | Extract metrics, generate charts | — |
| **Report Writer** | Sonnet 4.6 | Read, Glob, Write, Bash | Synthesize Aggregator output + Verifier rubric into final cited report | — |
| **Citation Verifier** | Haiku 4.5 | Read, Glob, WebFetch | Spot-check URLs, flag broken / unsupported | — |
| **Discovery-Stack agents** (Discovery Mode only) | Mixed (Gen: Opus 4.7 xhigh; Reviser: Opus 4.7 high; Ranker: any reasoning model) | Skill-internal tools + WebSearch + Bash + Python sandbox | Generation / Proximity / Reflection / Ranking / Evolution / Meta-review / Supervisor (Co-Scientist) — OR Generator / Verifier / Reviser (Aletheia) — OR LLM-Ensemble proposer / Evaluator / Pareto-DB (OpenEvolve) | **NEW (C6, C7, C5)** |

**Model policy (enforced):**
- Lead, Researchers, Verifier-Agent, Aggregator, Data Analyst → **Opus 4.7** (per user policy from v1).
- Report Writer → **Sonnet 4.6** (synthesis at 1/5 cost; 1M context beta).
- Citation Verifier → **Haiku 4.5** (4-5× faster; 90% of Sonnet 4.5 agentic perf for narrow checks).
- Judge Panel may include GPT-5.5 Pro / Gemini 3.1 Pro when configured for heterogeneous panels; **never collapse to a single model family** when the question is contested.
- Discovery-Stack: see Discovery Mode section below.

**Subagent frontmatter** (use these on every Agent call):
```yaml
model: opus            # or sonnet / haiku per role
effort: high           # low/medium/high/xhigh — Ares router may pin this per step
isolation: worktree    # for researchers that may write files
memory: shared/research_session_<id>   # see C17
background: false      # true only for Report Writer (long-running)
tools: [allowlist]     # see C13; rest deferred via ToolSearch
hooks:
  PostToolUse:
    WebFetch: archive-and-preview.sh   # see C20
```

---

## Phase 0 — Mode Selection (NEW, C1)

**Before** the Phase 1 query analysis, classify the query into a mode. This is a single short decision the lead makes; misclassification is recoverable (you can escalate mid-flight).

```
QUERY → MODE
├── Verifiable sub-question with a programmable evaluator?
│   (e.g., "find a faster matmul algorithm for 3×3 matrices", "find best prompt
│    for X benchmark", "improve sort speed on this dataset")
│   → GENERATOR-EVALUATOR MODE (OpenEvolve template)
│
├── Open-ended novel-hypothesis generation request?
│   (e.g., "propose new mechanisms by which X could cause Y in biology",
│    "what unsolved problems in cybersecurity could LLMs solve")
│   → DISCOVERY MODE (Co-Scientist 6-agent + Elo tournament)
│
└── Synthesis of existing knowledge (the typical case)
    → STANDARD MODE (Phases 1-7 below)
```

Default = STANDARD. If you invoke a mode other than STANDARD, **say so out loud** to the user and write it to the research plan — mode selection materially changes cost and run-time.

Write the mode + rationale to `files/research_plan.md`. Modes are documented below in dedicated sections.

---

## Phase 1 — Query Analysis & Research Planning (enhanced)

### Step 1 — Classify Effort Level (unchanged from v1)

| Complexity | Signal | Researchers | Searches/Agent | Aggregator | Verifier | Judges | Report |
|-----------|--------|-------------|----------------|------------|----------|--------|--------|
| Trivial | Single fact, yes/no | 1 | 3-5 | No | No | No | No |
| Simple | Focused, one angle | 1-2 | 5-8 | No | No | No | Optional |
| Moderate | Comparison / overview | 2-4 | 8-12 | Yes | No | No | Yes |
| Complex | Deep analysis | 4-6 | 10-15 | Yes | Yes | Optional | Yes |
| Exhaustive | Comprehensive investigation | 6-10 | 12-20 | Yes | Yes | Yes | Yes |

`/deep-research` invocation always uses **Exhaustive**.

### Step 2 — Decompose Into Subtopics (unchanged: 2-6 non-overlapping subtopics)

Bad / good examples preserved from v1.

### Step 3 — **Skill / Tool Whitelist Per Researcher** (NEW, C13)

For each researcher, decide the **non-deferred tool set**. Everything else is `defer_loading: true`. Default whitelist per researcher: `WebSearch, WebFetch, Read, Write, Bash, Glob, Grep`. Specialty researchers may add `mcp__<domain>__*` (e.g., a "scientific paper" researcher gets the arXiv MCP; a "regulatory" researcher gets the SEC EDGAR MCP). Do **not** include unused MCP servers — they cost tokens even unused.

### Step 4 — Allocate Effort Budget Per Researcher (NEW, C10)

- Default effort = `medium` for fact-gathering, `high` for synthesis-leaning subtopics.
- Reserve `xhigh` for the Aggregator and (in Discovery Mode) the Generator.
- Cap thinking budget on tasks with known distractors (per inverse-scaling caveat C30) — do not auto-crank thinking on tasks like "list all instances of X in a long article."
- Researchers can self-downshift via Ares-router (sample 2-3 cheap actions; if they agree, commit at lower effort; only escalate when they disagree).

### Step 5 — Save Research Plan (enhanced)

`files/research_plan.md` template:
```markdown
# Research Plan: [Topic]
## Query: [Original user query]
## Mode: STANDARD / DISCOVERY / GENERATOR-EVALUATOR
## Effort Level: Trivial/Simple/Moderate/Complex/Exhaustive
## Researcher count: N
## Subtopics:
1. [Subtopic] → Researcher 1 (model=opus, effort=high, tools=[...])
2. [Subtopic] → Researcher 2 (model=opus, effort=medium, tools=[...])
...
## Verifier: Yes/No
## Judge Panel: Yes/No (and: which model families?)
## Aggregator: Yes/No
## Memory dir: files/research_session_<id>/memory/
## Stopping criteria:
   - Per-researcher: 20 searches OR 90 minutes OR `finish` tool called with confidence ≥ τ*
   - Per-phase: 2nd-wave only if (gap_count > 2) OR (any researcher confidence < 0.6)
   - Per-session: hard cap 6 hours wall-clock unless user grants extension
## Expected output: [final deliverables]
```

This file is your durable external memory — survives compaction.

---

## Phase 2 — Parallel Research Execution (heavily enhanced)

Fan out all N researchers in **one Agent-tool message** (parallel). v1's parallelism is preserved; the *content* of each researcher's prompt and runtime config is upgraded.

### Researcher Subagent Prompt Template (v2)

```
You are Researcher [N] in a multi-agent deep-research system.

## YOUR ASSIGNMENT
Investigate: [SPECIFIC SUBTOPIC]
Research questions to answer:
- [Question 1]
- [Question 2]
- [Question 3]

## OUTPUT CONTRACT (STRICT — orchestrator parses this)
Save findings to: files/research_notes/[N]_[descriptive_name].md
Use the exact format (no raw search transcripts — synthesized findings only):

```markdown
# [Subtopic Title]
## Researcher [N] — [Date]

### Finding [N.K]: [Title]
**Detail**: [What you discovered — specific numbers, dates, names]
**Source**: [Full URL]
**Confidence**: HIGH / MED / LOW
**DRA-Risk**: NONE / [Failure subcat from the rubric you self-flagged, e.g., "1.3 Generic search"]
**Notes**: [Caveats, conflicts]

### Cross-References (one line each, do not pursue)
- ...

### Gaps & Open Questions
- ...

### Self-Verbalized Confidence (BrowseConf, C8)
Confidence: <integer 0-100>
[If <τ*, your output will be retried with a Summary or Neg variant prompt.]
```

DO NOT paste long text dumps. DO NOT include raw search transcripts. Cite, summarize specifically, move on.

## SEARCH STRATEGY — UNCHANGED FROM V1 (BROAD → NARROW)
1. SHORT BROAD queries first (2-4 words). Example: "semiconductor fabs 2026"
2. Scan results. Identify promising leads.
3. Progressively NARROW with specific follow-up queries.
4. Use WebFetch for full articles when snippets aren't enough — but note that WebFetch is wrapped: full body goes to disk (files/research_session_<id>/raw/<urlhash>.md), you receive a 10-line preview. Use Read on the disk file when you need full text.
5. Perform [N-M] web searches total. **STOP** when confidence ≥ 80 OR you've covered the questions OR you hit the search cap.

## BUDGET TRACKER (BATS, C9 — injected after every tool call)
You will see this block after each tool response:
```
Budget Tracker <budget>
  Search Budget Used: ##, Remaining: ##
  Fetch Budget Used: ##, Remaining: ##
Make the best use of the available resources.
</budget>
```
Tiered guidance:
- HIGH (≥70% remaining): Search 3-5 diverse queries in one batch. Browse up to 2-3 high-value URLs.
- MEDIUM (30-70%): Search 2-3 precise, refined queries per cycle. Browse 1-2 URLs that close key knowledge gaps.
- LOW (10-30%): 1 tightly focused query. At most 1 most promising URL.

Decision (use after each round):
- CONTINUE if the trajectory is promising and the budget is sufficient for deeper exploration.
- PIVOT if contradictions are identified or the remaining budget cannot support this lead.

## ADAPTIVE PER-STEP EFFORT (Ares + TrACE, C10 + C11)
- Sample 2-3 candidate next-actions for each decision; if they agree, commit immediately.
- Only escalate effort when candidates disagree.
- Do not crank thinking budget on tasks with distractors (inverse-scaling caveat).

## SOURCE QUALITY RULES (unchanged from v1)
PRIORITIZE primary > expert > quality journalism > industry analysis.
AVOID content farms, undated SEO, social-only sources.
Ask: "Would a domain expert cite this?"

## DRA FAILURE TAXONOMY (self-flag your own risks — C3)
Self-check before saving each finding:
1. Finding Sources — wrong source / missing / generic / invalid
2. Reasoning — premature conclusion / misinterpretation / hallucinated
3. Problem Understanding — misunderstanding task / goal drift / wrong decomposition
4. Action Errors — UI failure / format mistake / wrong modality
5. Max-Step Reached — exhausted budget without answer

If you suspect a finding might trigger any of the above, set DRA-Risk to the subcat code. The Verifier-Agent will see this self-flag and weight its check accordingly.

## SHARED MEMORY (C17)
Working memory dir: files/research_session_<id>/memory/
You and your sibling researchers can write durable notes here (per-researcher subdir to avoid stomping). Read this dir on startup to see what siblings have learned.

## FILE-ONLY HANDOFF (C18)
After this kickoff message, do not address the orchestrator in prose. Communicate via files:
- Your output goes to files/research_notes/[N]_*.md
- Cross-researcher notes to files/research_session_<id>/memory/researcher_[N]/
- The orchestrator will pull your results from disk.

## BOUNDARIES
- STAY within your subtopic: [SUBTOPIC]
- Do NOT investigate: [LIST OTHER SUBTOPICS]
- If you discover something relevant to another subtopic, note it briefly in Cross-References and do NOT pursue it
- STOP when you have solid coverage with multiple sources — do not search endlessly
- If a tool fails or returns no results, adapt: try different search terms, try WebFetch on a known URL, or note the gap and move on
```

### Parallel Execution Pattern (preserved from v1)

Spawn all researchers in ONE message. Each Agent call carries the full template above (parameterized per researcher). Critical detail (C19): **system prompts must be byte-identical across spawns** — only the user-message research assignment differs. This unlocks the 0.1× cached-prefix cost.

### Prompt-Cache Discipline (C19)

- 4 cache breakpoints (R5-F17):
  1. System+tools prefix (locked across all spawns).
  2. Skill / sub-skill bodies (locked per mode).
  3. Most-recent-user-block (research assignment — varies per spawn).
  4. One floating breakpoint that rolls forward.
- Do **not** dynamically toggle MCP servers mid-session — cache invalidation cascades.
- 1-hour cache write (2× base) preferred over 5-minute (1.25×) for the orchestrator's strategy prompt; it lives the whole session.

---

## Phase 3 — Gap Analysis & Second Wave (lightly enhanced)

After all researchers return (Phase 2 fan-in), the Lead reads `files/research_notes/*.md` and `files/research_session_<id>/memory/*` and evaluates:

1. **Coverage gaps** — subtopics underexplored?
2. **Source conflicts** — disagreements on key facts?
3. **Missing data** — specific numbers / facts that should exist but weren't found?
4. **Weak sourcing** — claims supported only by low-quality sources?
5. **High DRA-Risk flags** — any researcher self-flagged a finding with a failure subcat? Mandatory verifier pass on that finding.
6. **Low BrowseConf confidence** — any finding with confidence < τ* (default 70)? Mandatory retry pass (Summary or Neg variant, C8).

If gaps remain, spawn 1-3 **second-wave researchers** with narrower assignments. Re-use the same template; iterate the file naming (`9_gap_<topic>.md`, `10_gap_<topic>.md`, ...).

**Stopping criterion (C27):**
- Spawn second-wave if: `gap_count ≥ 2` OR `any researcher confidence < 0.6` OR `Verifier-Agent score < ADEQUATE`.
- Stop second-wave after one more round unless lead-judgment flags severe inadequacy. **No third wave by default** — at that point either accept gaps or escalate to the user.

---

## Phase 4 — Data Analysis (unchanged from v1)

Spawn Data Analyst (Opus 4.7). Steps preserved from v1: glob notes, extract metrics, generate 2-4 charts at 150 DPI, save data summary. Refer to v1 for the chart template.

Single addition for v2: produce a `files/data/techniques.csv` capturing any architectural lifts the research surfaced (e.g., "X technique: +Y pp on Z benchmark"). This feeds the Aggregator and Report Writer.

---

## Phase 5a — Verification Pass (NEW, C3 + C4)

**Spawn the Verifier-Agent** (Opus 4.7, `effort=high`) immediately after Phase 3 / 4 outputs are stable.

### Verifier-Agent Prompt (DRA-rubric-driven)

```
You are the Verifier-Agent. Your job is to apply the DRA Failure Rubric to every
finding produced by Researchers 1..N (and any 2nd-wave gap-fillers).

## INPUTS
- files/research_plan.md
- files/research_notes/*.md
- files/research_session_<id>/memory/*

## DRA FAILURE TAXONOMY (rubric)
1. Finding Sources
   1.1 Wrong Source / Consulting Wrong Evidence
   1.2 Missing Source (used internal knowledge instead of retrieving)
   1.3 Generic / Inadequate Search (query too broad or non-specific)
   1.4 Invalid Source / Secondary Source Dependence
2. Reasoning
   2.1 Premature Conclusion
   2.2 Misinterpretation (wrong subject / year / unit)
   2.3 Hallucinated / Overconfident Claims
3. Problem Understanding & Decomposition
   3.1 Misunderstanding Task / Instructions
   3.2 Goal Drift
   3.3 Inappropriate Decomposition
4. Action Errors
   4.1 UI Failures
   4.2 Format Mistakes
   4.3 Wrong Modality Use
5. Max-Step Reached

## YOUR PROCEDURE (DeepVerifier-style, per finding)
1. Read the finding (Detail + Source + Confidence + Notes + any DRA-Risk self-flag).
2. Spot-check the cited URL: does it actually support the claim?
3. Map any suspicious behavior to ONE potential DRA subcategory (or "No potential errors found").
4. If you flag a finding, emit corrective feedback (max 3 instructions, brief reflection prefix):

Reflection: <one paragraph on why the prior attempt failed>
Instruction 1: <one concrete corrective step>
Instruction 2: <optional>
Instruction 3: <optional, max 3 total>

5. Also assign a Reflection score 1-4 (explanation first, then number — reduces score anchoring):

Explanation: <one sentence>
Score: <1-4 integer>

## OUTPUT
Save to files/research_notes/verifier_report.md with:
- Per-finding status: PASS / FAIL / RETRY
- Failure category cited (if FAIL)
- Corrective feedback (if FAIL)
- Overall score: STRONG / ADEQUATE / WEAK

If any finding scores FAIL with a 1.x or 2.x flag, raise it to the Lead for a retry pass.
```

### Heterogeneous Judge Panel (C4) — invoked on contested claims

When two researchers disagree on a fact, OR when the Verifier-Agent flags a Hallucination (2.3) on a finding the Lead believes is correct, OR when a high-stakes inference depends on a single source, spawn a **3-judge panel**:

- Each judge runs on a **distinct model family** (Claude Opus 4.7 + GPT-5.5 Pro + Gemini 3.1 Pro when available). Falls back to 3 distinct-prompt Opus 4.7 if heterogeneous models unavailable.
- Use **multi-turn debate** for top-stakes claims (PROClaim-style: 2 advocates + 3 heterogeneous judges).
- Use **single-turn pairwise comparison** for cheap pairs (Co-Scientist matchmaking pattern).
- Output: majority vote + minority dissent surfaced in the final report (do not bury dissent).

### Anti-Collusion Audit (C24, C29)

Before final delivery, run a brief Petri-style sanity check:
- Are any researchers' findings *suspiciously aligned* on a contestable claim?
- Did any finding cite a source one of its peers had also reached, with the same wording?
- Does the synthesis present a single coherent story where the underlying evidence is mixed?

If yes → re-engage the heterogeneous judge panel on the suspect claim. State the **"AI Organizations Can Be More Effective but Less Aligned"** caveat (R1-AL2) in the final report if you observe convergence-without-evidence.

---

## Phase 5b — AggAgent Synthesis (NEW, C2 — REPLACES v1's flat synthesis)

This is the **single highest-leverage v2 change**: instead of asking the Lead (or Report Writer) to read all research notes and produce a flat synthesis, spawn a dedicated **Aggregator** that treats researcher trajectories as an interrogable environment.

### Aggregator System Prompt (verbatim from R9 Gap D / arXiv 2604.11753)

```
You are the Aggregator in a multi-agent deep-research system.

Your job is to synthesize a final answer from N parallel researcher trajectories.
You will NOT concatenate trajectories or vote on final outputs. You will inspect
them on-demand.

OPERATIONAL GUIDELINE (core principle):
"A single trajectory with a clear, unambiguous tool observation supporting answer X
is stronger evidence than many trajectories that reasoned their way to Y without
grounding in tool outputs."

OTHER LOCKED INSTRUCTIONS:
- Verify claims by inspecting actual tool outputs using search and retrieval functions.
- Final solutions must be self-contained with no references to trajectory IDs or
  tool invocations.
- Prohibited: circular logic, ungrounded assumptions, silent handling of tool
  errors, majority-vote bias without evidence grounding, self-referential mentions
  of trajectories/tools.

YOU HAVE 4 TOOLS:
1. get_solution(trajectory_id) → final-step content of one trajectory. Use to ask
   "what did this researcher conclude?"
2. search_trajectory(query, role_filter?) → ROUGE-L recall search across all
   trajectories. Use to ask "did any researcher observe X?"
3. get_segment(trajectory_id, start_step, end_step) → contiguous step range
   (max 5 steps) from one trajectory. Use to inspect actual tool outputs in context.
4. finish(final_answer) → submit. Format depends on task:
   - Standard: <answer>...</answer>
   - Qwen-style: Explanation: ... \nExact Answer: ...
   - Long-form report: integrated content with citations [N] grounded in retrieved snippets

LOOP:
You see only the metadata for each trajectory at session start (step counts, tool
usage histograms, brief preview). You page in detail via the tools above. Iterate
up to 100 steps. If context approaches the limit, you will be force-finish-only
(you'll get a notice).

LONG-FORM (REPORT) VARIANT INSTRUCTIONS:
- Integrate content across candidates rather than concatenate sections.
- Ground every nontrivial claim in retrieved snippets using citation format.
- Resolve contradictions by reasoning about accuracy rather than averaging positions.
```

### Aggregator Tool Implementation (skill-internal, file-backed)

The Aggregator's 4 tools operate over the researcher notes on disk. Implementation sketch (shell helpers; can be inlined or shipped as MCP):

- `get_solution(N)` → returns the final-section block of `files/research_notes/N_*.md`.
- `search_trajectory(query, role?)` → grep + ROUGE-L re-rank across all `files/research_notes/*` and `files/research_session_<id>/raw/*` (the WebFetch archive).
- `get_segment(N, start, end)` → returns `files/research_notes/N_*.md` lines [start..end] (max 5 logical sections).
- `finish(answer)` → writes `files/reports/aggregator_synthesis.md` and terminates.

The Aggregator's output (`aggregator_synthesis.md`) is the single source the Report Writer consumes in Phase 6 — the Report Writer never reads raw research notes.

### Why this works (cite the data summary)

- **+5.3% absolute** avg across 6 benchmarks, **+10.3% on deep-research-specific tasks** (R4-F34).
- Avoids context blow-up (no concat).
- Avoids majority-vote dilution.
- Resolves disagreements by inspecting tool outputs, not by counting votes.

---

## Phase 6 — Report Writing (preserved, with minor changes)

Spawn the Report Writer (Sonnet 4.6). Inputs are now:
- `files/reports/aggregator_synthesis.md` (from Phase 5b — primary)
- `files/data/data_summary.md` and chart manifest
- `files/research_notes/verifier_report.md` (for the Contradictions & Uncertainties section)

Report Writer **does not** read raw research notes — that's the Aggregator's job. The Writer's job is to render the Aggregator's synthesis into the user-facing report format (preserved from v1: Executive Summary / Key Findings / Detailed Analysis / Data & Visualizations / Contradictions & Uncertainties / Knowledge Gaps / Sources).

Quality rules from v1 preserved: every claim has a numbered citation, specific stats, dissent surfaced, low-confidence flagged, theme-organized.

Output: `files/reports/[topic_slug]_report.md`.

---

## Phase 7 — Citation Verification (preserved, with minor changes)

Spawn the Citation Verifier (Haiku 4.5). Steps preserved from v1 plus:
- Verify a *sample* of 5-10 high-stakes URLs via WebFetch.
- Cross-check against the Verifier-Agent's PASS/FAIL log — any source the Verifier flagged that survived into the report gets a mandatory check.
- Flag any URL whose cited claim does not appear in the page (Hallucination 2.3 by proxy).

Output: `files/reports/citation_audit.md` with overall score STRONG / ADEQUATE / WEAK.

If WEAK → Lead either offers to re-research the flagged claims or annotates the report's uncertainty section.

---

## Phase 8 — Dream / Memory Consolidation (NEW, C26 — optional, runs post-session)

Inspired by Anthropic Managed Agents' "Dreaming" (R1-MA4). Off by default; users can opt in via `/dream` slash command or settings.json hook.

### Dream Subagent Procedure (paraphrased; literal Anthropic prompt not yet released)

1. **Log capture** during the session (already happens — `research_notes/*`, `memory/*`, `raw/*`).
2. **Replay**: a fresh Opus 4.7 subagent reads the session logs + the existing skill-level memory (`~/.claude/projects/<project>/memory/deep-research/`).
3. **Extract**: identify (a) recurring failure modes, (b) successful patterns worth promoting, (c) stale memory entries to remove. Recurrence (≥2 sessions) is the signal-from-noise filter.
4. **Consolidate**: write a patch to `~/.claude/projects/<project>/memory/deep-research/PATTERNS.md` (skill-level, not session-level), pruning stale entries and merging duplicates.

Reported impact: 6× completion-rate gain at Harvey (Anthropic announcement). Treat as opt-in; the consolidation prompt is not yet public so this section is paraphrased.

---

## Discovery Mode (NEW, C6 + C7) — novel-hypothesis generation

**When to enter:** the query asks for *novel* output, not synthesis. Examples:
- "Propose new mechanisms by which X could cause Y in biology."
- "What are 5 unsolved problems in field Z that current LLMs could plausibly attack?"
- "Generate testable hypotheses for [scientific puzzle]."

**Architecture:** Co-Scientist 6-agent stack with an explicit Supervisor and Elo tournament (R3 Co-Scientist).

```
                                Supervisor
                                    │
        ┌──────────┬────────────────┼──────────────┬──────────────┐
        ▼          ▼                ▼              ▼              ▼
    Generation  Proximity       Reflection     Ranking         Evolution
    (Opus       (clusters       (critique:     (Elo            (refine and
     4.7        for             novelty /      tournament,     combine
     xhigh)     diversity)      correctness /  pairwise         top-ranked
                                testability)   debate)         hypotheses)
                                                                    │
                                                                    ▼
                                                              Meta-review
                                                              (final synthesis)
```

### Subagent prompts (operational summary; literal Co-Scientist prompts not released, paraphrased per R9 Gap C)

- **Supervisor**: decomposes the research goal, decides which agents to spawn when, monitors progress, terminates when convergence criteria met.
- **Generation agent**: proposes initial hypotheses grounded in literature; uses WebSearch/WebFetch + the shared memory dir; emits 5-20 candidates per round.
- **Proximity agent**: clusters candidates to enforce diversity (drops near-duplicates; ensures the candidate pool spans multiple mechanisms).
- **Reflection agent**: critique with axes (correctness, quality, novelty); five review modes:
  - Initial review (triage)
  - Full review (literature deep-check)
  - Deep verification review (logical / empirical)
  - Observation review (does the hypothesis explain the phenomenon the user mentioned?)
  - Simulation review (would a thought-experiment confirm or break it?)
- **Ranking agent**: pairwise Elo tournament; initial rating 1200. Top-ranked pairs get multi-turn scientific debate; lower-ranked pairs get single-turn pairwise comparison. Axes forced into prompt: **novelty, correctness, testability**.
- **Evolution agent**: takes top-K from Elo tournament and produces refinements + combinations (the "evolutionary" step).
- **Meta-review**: synthesizes the final ranked set of hypotheses + provenance + falsifiability criteria into the report.

### Aletheia Fallback for Ambiguous Synthesis (C7)

When the Co-Scientist Ranking agent cannot find a clear winner OR the query is closer to ambiguous synthesis than novel hypothesis, drop to the **Aletheia G/V/R triplet** (R3 Aletheia):

- **Generator**: proposes a candidate solution in natural language (Opus 4.7 xhigh).
- **Verifier**: NL-critique; emits one of {CORRECT, MINOR-FLAW, CRITICAL-FLAW}; if CRITICAL, explains why a patch wouldn't save the argument.
- **Reviser**: localized fix when verdict is MINOR-FLAW; restart at Generator with failure context when CRITICAL-FLAW.

**Explicit reject branch**: If after N iterations (default 3) the Verifier still reports CRITICAL-FLAW, return **"could not resolve"** rather than a low-confidence guess. This is conservative by design: Aletheia returns "I cannot solve this" on ~70% of inputs and that's the point — abstain over hallucinate. Surface the rejected query to the user with the Verifier's last critique.

### Discovery Mode Output

`files/reports/discovery_report.md` with:
- Final ranked hypotheses (Elo-sorted) — each with novelty / correctness / testability scores, falsifiability criteria, suggested experimental approach.
- Provenance (which Generation round, which mutations applied).
- Rejected hypotheses (with critique).
- Open questions (things the Reflection agent flagged but couldn't resolve).
- Suggested next experiments (computational, wet-lab, or literature-search).

**Honesty constraint (from Co-Scientist):** if the system cannot programmatically or via expert-in-loop verify a hypothesis, label it "speculative" and limit confidence. The system's value is in the *ranked candidate pool* with falsifiability criteria, not in declaring truth.

---

## Generator-Evaluator Mode (NEW, C5) — verifiable sub-questions

**When to enter:** the query has a programmable evaluator (a function `score(answer) → R` you can call). Examples:
- "Find a faster sort algorithm for arrays of size 50-200."
- "Optimize this prompt for maximum accuracy on benchmark X."
- "Improve this code for memory efficiency."

**Architecture:** OpenEvolve / AlphaEvolve template (R8 OpenEvolve, R3 AlphaEvolve).

```
LLM Ensemble (Flash breadth + Pro depth)  ──proposes──▶  Mutation diffs
                                                              │
                                                              ▼
                                                       Automated Evaluator
                                                       (programmatic)
                                                              │
                                              ┌───────────────┴────────────────┐
                                              ▼                                ▼
                                       MAP-Elites grid (feature bins)   Island sub-pops
                                              │                                │
                                              └──────┬─────────────────────────┘
                                                     ▼
                                          Top-K + diverse exemplars
                                          re-fed to ensemble for next round
```

### Mutation Proposer Prompt (verbatim from OpenEvolve, R9 Gap B)

System:
```
You are an expert software developer tasked with iteratively improving a codebase.
Your goal is to maximize the FITNESS SCORE while exploring diverse solutions across
feature dimensions. The system maintains a collection of diverse programs - both
high fitness AND diversity are valuable.
```

User template:
```
# Current Program Information
- Fitness: {fitness_score}
- Feature coordinates: {feature_coords}
- Focus areas: {improvement_areas}

{artifacts}

# Program Evolution History
{evolution_history}

# Current Program
```{language}
{current_program}
```

# Task
Suggest improvements to the program that will improve its FITNESS SCORE.
The system maintains diversity across these dimensions: {feature_dimensions}
Different solutions with similar fitness but different features are valuable.

You MUST use the exact SEARCH/REPLACE diff format shown below to indicate changes:

<<<<<<< SEARCH
# Original code to find and replace (must match exactly)
=======
# New replacement code
>>>>>>> REPLACE

You can suggest multiple changes. Each SEARCH section must exactly match code in
the current program. Be thoughtful about your changes and explain your reasoning
thoroughly. IMPORTANT: Do not rewrite the entire program - focus on targeted
improvements.
```

### Mutation Wiring

Mark the editable region in the source with `# EVOLVE-BLOCK-START` ... `# EVOLVE-BLOCK-END`. Only that region is presented as `{current_program}`. Code outside the markers is preserved verbatim.

### Artifact Side-Channel (errors → next prompt)

The `{artifacts}` placeholder is filled from the previous run's evaluation results — `stderr`, `profiling_data`, `llm_feedback`, `build_warnings` — rendered under a "Previous Execution Feedback" header. This closes the feedback loop: programmatic-evaluator errors become natural-language context for the next mutation.

### Database (MAP-Elites + Islands)

- **MAP-Elites**: programs binned by user-defined behavioral features (e.g., `compute_cost`, `algorithm_family`); each bin keeps the highest-fitness program.
- **Islands**: population partitioned into sub-populations evolving independently with occasional migration; prevents premature convergence.
- **Sampling**: parents drawn proportional to fitness within an island; inspirations drawn from other MAP-Elites cells.

### Skill Wiring

The Lead spawns a Generator-Evaluator coordinator subagent that:
1. Stores candidate programs in `files/research_session_<id>/programs/<gen>_<id>.py`.
2. Calls the programmatic evaluator via Bash (user-supplied script).
3. Maintains the MAP-Elites grid in `files/research_session_<id>/grid.json`.
4. Calls the LLM ensemble (Flash breadth + Pro depth in parallel) with the mutation prompt above; collects all proposed diffs; applies them as new candidates.
5. Terminates after fixed generation budget OR fitness plateau.

Output: `files/reports/evolution_report.md` with the top-fitness program, the Pareto frontier of (fitness × feature) tradeoffs, the evolution trace, and the most "inspiring" diverse exemplars.

---

## Concrete Prompt Library (Appendices)

### A. BrowseConf Confidence Elicitation (C8)

End every researcher finding with this verbatim block:

```
**Answer**: [concise direct answer to the research question]
**Confidence**: [integer 0-100 representing how sure you are]
```

Full instruction (one-time, in the system prompt):

> "A confidence score between 0-100 representing how sure you are that the answer is correct. A value close to 0 means you think the answer is likely to be wrong, while a value close to 100 means you think the answer is likely to be correct. Just give the integer, no explanation needed."

**Retry variants** when confidence < τ* (default 70):

*Summary variant* (drives the agent to explore a different angle):
> "Below is a summary of a previous attempt at the question: [prior summary]. Take a different angle."

*Neg variant* (strongest signal — blocks known-wrong answers):
> "Below are identified incorrect answers to the question. You MUST NOT give these answers again unless some turned out to be correct. [prior wrong answers]"

**Threshold τ\*** (R9 Gap "BrowseConf"): dataset-calibrated, tuned to guarantee at least k% accuracy lift (k ∈ {5, 10, 20}) at the threshold-passed slice. Default 70 for general research; raise to 85 for high-stakes claims.

### B. BATS Budget Tracker Block (C9)

Inject after every tool response in researcher contexts:

```
Budget Tracker <budget>
  Search Budget Used: ##, Search Budget Remaining: ##
  Fetch Budget Used: ##, Fetch Budget Remaining: ##
  Wall-clock Used: ##min, Wall-clock Remaining: ##min
Make the best use of the available resources.
</budget>
```

Tiered guidance + dig/pivot decision criterion: see Phase 2 Researcher template above.

### C. DRA Failure Taxonomy (rubric) — restated for skim

| # | Category | Subcategories |
|---|----------|---------------|
| 1 | Finding Sources | 1.1 Wrong / 1.2 Missing / 1.3 Generic / 1.4 Invalid (secondary) |
| 2 | Reasoning | 2.1 Premature / 2.2 Misinterpretation / 2.3 Hallucinated |
| 3 | Problem Understanding | 3.1 Misunderstood task / 3.2 Goal drift / 3.3 Wrong decomposition |
| 4 | Action Errors | 4.1 UI failure / 4.2 Format mistake / 4.3 Wrong modality |
| 5 | Max-Step Reached | (single) |

### D. Aletheia G/V/R Architectural Pattern (paraphrased; literal prompts not released)

- **Generator** prompt: math/research-reasoning system prompt; implicit "you may admit failure" instruction; access to tool surface (search, calc, theorem-prover, code exec).
- **Verifier** prompt: "Critique this proof/argument in natural language. Identify any logical gap, citation error, hallucinated theorem, or numerical mistake. Conclude with one of: CORRECT / MINOR-FLAW / CRITICAL-FLAW. If CRITICAL-FLAW, explain why a patch would not save the argument."
- **Reviser** prompt: "Given the original argument and the Verifier's identified flaw, produce a localized correction. Do not re-derive the whole proof."
- **Branch logic**: CORRECT → emit. MINOR-FLAW → Reviser. CRITICAL-FLAW → Generator restart with failure context. After N iterations (default 3) without CORRECT → **abstain**.

### E. DeepVerifier Corrective Feedback (C3, verbatim from R9 Gap A)

When a finding fails the rubric, emit:
```
Reflection: <brief reflection on why the prior attempt failed>
Instruction 1: <one concrete corrective step>
Instruction 2: <optional>
Instruction 3: <optional, max 3 total>
```

Guidance baked in: "point out necessary sources and actions to avoid the agent making the same mistakes again" — prefer "clear, concise, and accurate instructions rather than long or complex" ones.

Judge step format (forces categorical with explanation first to reduce anchoring):
```
Explanation: <one sentence>
Score: <1-4 integer>
```

### F. Heterogeneous Judge Panel Prompt (C4, paraphrased per R9 Gap C)

```
You are evaluating two research findings on the same factual claim.
Compare them on:
  - Novelty: Which proposes a more original / less-derivative answer?
  - Correctness: Which is more likely to be factually valid given the cited sources?
  - Testability: Which can be more concretely verified or falsified?

Finding A: <text + source URL>
Finding B: <text + source URL>

[For top-stakes pairs:] Simulate a multi-turn debate between two expert reviewers,
one defending each finding. After 3 turns, adjudicate.

Conclusion: <"A better" | "B better" | "Tie">
Rationale: <one paragraph>
```

Aggregate verdicts via Borda count / Inverse-Entropy weighting (C25, R6-F15) — not naive majority.

---

## File Structure (v2 — superset of v1)

```
files/
├── research_plan.md              # Phase 1 plan (mode, effort, budgets, stopping)
├── research_notes/               # Phase 2 + 3 outputs
│   ├── 1_[subtopic].md
│   ├── 2_[subtopic].md
│   ├── ...
│   ├── 9_gap_[subtopic].md        # 2nd-wave
│   └── verifier_report.md         # Phase 5a
├── research_session_<id>/         # NEW v2 — session-scoped working area
│   ├── memory/                    # shared scratchpad (C17)
│   │   ├── researcher_1/
│   │   ├── researcher_2/
│   │   └── ...
│   ├── raw/                       # WebFetch archive (C20)
│   │   └── <urlhash>.md
│   ├── tasks/                     # NEW — orchestrator→researcher kickoffs
│   │   └── researcher_N_task.md
│   ├── results/                   # NEW — researcher→orchestrator returns
│   │   └── researcher_N_result.json
│   ├── programs/                  # Generator-Evaluator mode candidates
│   ├── grid.json                  # MAP-Elites state
│   └── hypotheses/                # Discovery mode
│       ├── round_1/
│       └── elo_ratings.json
├── data/
│   ├── data_summary.md
│   ├── benchmarks.csv
│   └── techniques.csv             # NEW — architectural lifts surfaced
├── charts/
│   └── *.png
└── reports/
    ├── aggregator_synthesis.md    # NEW Phase 5b output
    ├── [topic]_report.md           # Phase 6 final report
    ├── citation_audit.md           # Phase 7
    ├── discovery_report.md         # Discovery Mode only
    ├── evolution_report.md         # Generator-Evaluator Mode only
    └── SKILL_v2_proposal.md        # this document
```

Across sessions, persistent memory lives at `~/.claude/projects/<project>/memory/deep-research/`:
- `PATTERNS.md` — Dream phase consolidation (C26)
- `SKILLS_LIBRARY.md` — Voyager-style: named reusable research recipes by NL embedding (R4-F27 SAGE / SKILLRL)
- `SOURCE_QUALITY.md` — accumulated source-reputation observations (which domains reward / fail for which kinds of questions)

---

## Cost & Cache Engineering Notes (consolidates C13-C21)

The realistic cost-reduction stack for a single exhaustive run (composable; multiply, don't add):

| Layer | Reduction | Source |
|-------|-----------|--------|
| Three-tier routing (Opus lead / Sonnet writer / Haiku verifier) | ~50% vs uniform Opus | R8 industry numbers |
| Prompt caching (4 sliding breakpoints) | -41 to -80% on cached prefix | R5-F16, R5-F17 |
| clear_tool_uses_20250919 on researchers | 335K → 173K context (~50%) | R5-F8 Anthropic cookbook |
| compact_20260112 on orchestrator at 40% | enables indefinite runs | R5-F7, R5-F11 |
| ToolSearch + defer_loading on unused tools | -85% on multi-MCP setups | R1-SDK2, R5-F20 |
| Code Execution with MCP wrapper on heavy servers | -98.7% (150K → 2K demo) | R1-SDK3, R5-F23 |
| WebFetch archive-to-disk wrapper | researcher context lean | R5-F28 LangChain Deep Agents |
| Per-step Ares effort routing | -41 to -53% reasoning cost | R6-F24 Ares |
| TrACE adaptive sampling | -33 to -65% LLM calls | R6-F39 TrACE |
| BATS budget tracker injection | -40% tool calls | R6-F25 BATS |

Token-efficient tool use (Claude 4.x default, R5-F36) is on automatically — no config.

**Cache discipline rules:**
1. System prompts BYTE-IDENTICAL across researcher spawns (C19). Differences only in user-message research assignment.
2. Tool list stable across researcher spawns. Don't conditionally add MCP servers per researcher; instead, defer-load the union.
3. Pin thinking-budget per researcher; don't toggle mid-session (cache invalidation).
4. Use 1-hour cache for the orchestrator's strategy doc; 5-min for per-research-question prompts.

---

## Stopping Criteria (C27, explicit)

The literature has no principled stopping criterion for multi-agent research (R4-F2). Until it does, we ship explicit heuristics:

| Boundary | Stop when |
|----------|-----------|
| Per-researcher search loop | confidence ≥ τ* (default 70) OR searches ≥ cap OR wall-clock ≥ 90 min |
| Per-phase (Phase 2 fan-in → Phase 3 gap analysis) | all researchers returned OR 30 min after last return (timeout strays) |
| Second-wave gap-fill | one round max unless lead-judgment overrides |
| Aggregator (Phase 5b) | `finish` tool called OR 100 iterations OR context overflow |
| Verifier-Agent | all findings scored |
| Discovery Mode (Co-Scientist Elo) | top-K Elo gap > threshold (default 100 Elo) for ≥3 rounds OR fixed generation cap |
| Generator-Evaluator Mode | fitness plateau (no improvement in MAP-Elites best for K generations) OR generation cap |
| Full session | 6 hours wall-clock or user grant; checkpoint to disk every phase boundary |

The user can always shorten by saying "wrap it up." The user can always extend by saying "go deeper on X."

---

## Anti-Patterns (v1 list preserved; v2 additions marked NEW)

Do NOT:
- Spawn 10+ researchers for a simple factual question.
- Let researchers use long, verbose search queries (broad-first).
- Continue searching after sufficient information is gathered.
- Let researchers duplicate each other's work.
- Skip gap analysis.
- Generate reports without citations.
- Copy large text blocks through conversation instead of files.
- Restart from scratch on a failure — resume from last checkpoint.
- Downgrade Lead / Researcher / Verifier-Agent / Aggregator / Data Analyst to sonnet/haiku — user policy requires Opus 4.7.
- **NEW** Crank thinking budget on tasks with distractors (Inverse Scaling — R6-F27).
- **NEW** Use the same model family across the judge panel on contested claims (collusion risk).
- **NEW** Hand the Report Writer raw research notes (the Aggregator is the synthesizer, not the Writer).
- **NEW** Toggle MCP servers mid-session (cache invalidation cascades; R5-F18).
- **NEW** Run Discovery Mode without an audit / verification step (R1-AL2 multi-agent alignment regression caveat).
- **NEW** Treat AggAgent's `search_trajectory` as a substitute for re-research — it searches existing trajectories, not the web.
- **NEW** Forget to set `defer_loading: true` on unused tools (C13).
- **NEW** Aggregate via naive majority vote (use Inverse-Entropy weighting — C25, R6-F15).
- **NEW** Skip the BrowseConf confidence elicitation (C8) — without it, you can't trigger retry-with-Neg variants and confidence calibration breaks.

---

## Communication Rules (preserved)

- Concise status updates (2-3 sentences max).
- No greetings, no emojis.
- Lead with findings, not process.
- Report the answer, then offer the detailed report.

---

## Findings → Edits Map (audit trail)

This skill's redesign is fully traceable to research notes. The table below lets a reviewer challenge any edit by going back to its source.

| Edit | Driving finding(s) | Quantified lift |
|------|-------------------|-----------------|
| C2 Aggregator | R4-F34 AggAgent (arXiv 2604.11753) | +5.3 pp avg, +10.3 pp deep-research |
| C3 Verifier rubric | R4-F8 + R6-F51 DeepVerifier (arXiv 2601.15808) | +8-11 pp GAIA hard |
| C4 Heterogeneous judges | R4-F5 PROClaim, R4-F6 A-HMAD | +10 pp Check-COVID |
| C5 Generator-Evaluator | R3 AlphaEvolve, R4-F25, R8 OpenEvolve | discovery-class results (matmul 49→48 etc.) |
| C6 Co-Scientist | R3 Co-Scientist (Nature s41586-026-10644-y) | wet-lab validated discoveries (liver fibrosis 91%, AMR Penadés-decade-in-days) |
| C7 Aletheia G/V/R | R3 Aletheia (arXiv 2601.22401) | 13 Erdős resolutions in 700-problem sweep |
| C8 BrowseConf | R6-F50 BrowseConf (arXiv 2510.23458) | confidence-calibrated retry |
| C9 BATS | R6-F25 BATS (arXiv 2511.17006) | -40% tool calls, -31% cost |
| C10 Ares | R6-F24 Ares (arXiv 2603.07915) | -41 to -53% reasoning cost |
| C11 TrACE | R6-F39 TrACE (arXiv 2604.08369) | -33 to -65% LLM calls |
| C12 Trajectory compression | R6-F49 (arXiv 2604.16529) | +6.7 pp SWE-Bench, +12.2 pp Terminal-Bench |
| C13 Skills + ToolSearch | R1-SDK1, R1-SDK2, R5-F19, R5-F20 | -85% tokens |
| C14 Code Exec w/ MCP | R1-SDK3, R5-F23 (Anthropic, Cloudflare) | -98.7% tokens demo |
| C15 clear_tool_uses | R5-F8 Anthropic cookbook | 335K → 173K |
| C16 compact_20260112 | R5-F7, R5-F11 | enables indefinite runs |
| C17 Shared memory | R1-CTX3, R5-F6 Anthropic memory tool | cross-researcher knowledge |
| C18 File-only comms | R5-F13, R5-F25 | orchestrator context lean |
| C19 Byte-identical prefixes | R5-F16 "Don't Break the Cache" (arXiv 2601.06007) | -41 to -80% prefix cost |
| C20 WebFetch wrapper | R5-F28 LangChain Deep Agents | researcher context lean |
| C21 Three-tier routing | R1-M5, R8 industry numbers | -51% cost vs uniform Opus |
| C22 Tree-GRPO branching | R6-F9 Tree-GRPO (arXiv 2509.21240) | +69% rel on agent tasks |
| C23 Heterogeneous panel | R4-F6 A-HMAD, R6-F19 ModelSwitch | wisdom-of-crowd, anti-collusion |
| C24 Petri-style audit | R1-AL1 Petri 2.0, R1-AL2 "AI Orgs less aligned" | mitigates multi-agent alignment regression |
| C25 Inverse-entropy SC | R6-F15 (arXiv 2511.02309) | +46.7% in 95.6% configs |
| C26 Dream phase | R1-MA4 Anthropic Managed Agents | Harvey reported 6× completion-rate |
| C27 Stopping criteria | R4-F2 Orchestration Traces (arXiv 2605.02801) | explicit instead of implicit |
| C28 Frontmatter knobs | R1-SDK4 Claude Code subagent frontmatter | per-researcher control |
| C29 Alignment caveat | R1-AL2 | operator awareness |
| C30 Inverse-scaling caps | R6-F27 Anthropic Inverse Scaling (arXiv 2507.14417) | prevents DeepSeek-R1 70→30% mode |

---

## Migration Notes (how to adopt this in practice)

1. **Drop-in replacement**: `SKILL.md` → `SKILL_v2.md` (rename), then archive v1 to `archive/SKILL_v1.md`. The frontmatter `description` is updated, so Claude Code's metadata-level discovery picks up the new capabilities at session start.
2. **Phased rollout** (recommended):
   - **Week 1**: Enable C2 (Aggregator), C3 (Verifier-Agent), C13 (defer_loading), C19 (byte-identical prefixes). Smallest blast radius; biggest single-run lift.
   - **Week 2**: Add C8 (BrowseConf), C9 (BATS), C15-C16 (compaction), C18 (file-only comms).
   - **Week 3**: Add C4 (heterogeneous judges) and C24 (Petri audit). Requires multi-provider config; skip if Anthropic-only.
   - **Week 4**: Wire Discovery Mode (C6) and Generator-Evaluator Mode (C5) as opt-in via Phase 0.
3. **Telemetry**: log every orchestration trace per R4-F2 schema (`spawn / delegate / communicate / aggregate / stop` events with payloads) to `files/research_session_<id>/trace.jsonl`. Enables future RL-on-traces analysis. Don't auto-train; this is for retrospectives.
4. **Backward compatibility**: v1's 6-phase spine is preserved. A v1 caller invoking the skill without mode selection gets STANDARD mode by default and never knows the new phases exist (Phases 5a, 5b, 8, and the modes are additive).

---

## Open Questions for the Operator (deliberately unsolved)

These are research-frontier questions; the skill should be honest about them rather than baking in dogma.

1. **Optimal team size**: literature converges empirically on 3-4 researchers (R4 gap #2). We let the effort table decide; no theory predicts.
2. **Stopping criterion**: still unsolved in literature (R4-F2). We ship explicit heuristics; future RL-on-traces may improve.
3. **CFE / counterfactual frame ensembling**: Dipper (R6-F32) is the closest published validation; explicit study of structurally counterfactual frames (not just paraphrases) is missing. The skill could be a venue to publish reference results.
4. **Skill libraries vs prompt drift**: SAGE/SKILLRL (R4-F27) store skills as code; deep-research recipes are NL. Whether a code-form representation survives model updates is open.
5. **AggAgent at scale**: AggAgent's published numbers (R4-F34) use 6 benchmarks; behavior at N>10 trajectories under heterogeneous-model researchers is untested.
6. **Heterogeneous judges cost-effectiveness**: PROClaim shows +10 pp on Check-COVID; the cost ratio in production multi-provider deployments is operator-dependent.
7. **Dream phase prompt**: Anthropic's literal consolidation prompt is not yet public; the C26 procedure is paraphrased from announcements + secondary sources.
8. **Conductor vs Engine**: R6-F54 warns against both orchestrator AND model trying to do high-level planning. Default = orchestrator plans, model executes. Discovery Mode breaks this (the Generator plans; the Supervisor only meta-plans).

---

## Bottom Line

v1 was a good skill. v2 is what the same skill looks like when you fold in 6 months of frontier-lab and academic results: a generator-verifier-aggregator architecture with explicit failure rubrics, mode-aware orchestration that can climb from synthesis into novel discovery, prompt-cache and context-engineering discipline that drops cost an order of magnitude, and stated caveats where the literature is still catching up.

The single most-impactful change is **C2 (Aggregator replaces flat synthesis)** — measured +10.3 pp on deep-research tasks. The single biggest *capability unlock* is **C5 + C6 (Generator-Evaluator + Discovery Modes)** — these let the skill produce *novel* outputs the synthesis-only v1 could not reach. Everything else is composable efficiency.

Run it. Telemetry will tell us where v3 needs to go.
