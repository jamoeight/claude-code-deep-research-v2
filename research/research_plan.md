# Research Plan: SOTA in LLM Research Agents & Harnesses (Post-Nov 2025)

## Query
Ground yourself in the latest (post-Nov 2025) AI/LLM research / SOTA architecture
from top labs (Anthropic, OpenAI, DeepMind). Focus heavily on breakthroughs in
**LLM research agents & harnesses**. For each actionable finding, propose a
concrete change to this `deep-research` skill so it scales to produce extremely
rich research and possible novel discoveries. The new skill should be this exact
one — scaled by adding the recent breakthroughs.

## Effort Level
**EXHAUSTIVE** — invoked via `/deep-research`. 8 parallel first-wave researchers,
12-20 searches each, with second-wave gap-fillers as needed. Lead = Opus 4.7,
researchers = Opus 4.7, data analyst = Opus 4.7, report writer = Sonnet 4.6,
verifier = Haiku 4.5.

## Date Window
Primary: 2025-11-01 → 2026-05-20 (today). Secondary: late-2025 papers/releases
referenced as foundation.

## Subtopics (No Overlap — Strict Boundaries)

1. **Anthropic frontier work** → Researcher 1
   - Claude 4.6/4.7 capability releases, Skills, Claude Agent SDK, MCP evolution,
     Computer Use / coding agents, "How we built our multi-agent research system"
     follow-ups, Constitutional AI / RLAIF papers, alignment research relevant to
     agents (sandbagging, scheming, interpretability for agents).
   - **Excludes**: OpenAI/DeepMind work, generic open-source frameworks.

2. **OpenAI frontier work** → Researcher 2
   - GPT-5 / o4 / o5 / agentic releases, Deep Research product, Operator,
     ChatGPT agentic features, OpenAI papers on reasoning, RFT, evals,
     swarm/MAS releases.
   - **Excludes**: Anthropic/DeepMind work, third-party harnesses.

3. **Google DeepMind frontier work** → Researcher 3
   - Gemini 2.5/3 releases, AlphaEvolve / AlphaProof / AlphaCode evolutions,
     scientific discovery agents (Co-Scientist, materials discovery), Genie,
     Gemma 3, DeepMind agent papers.
   - **Excludes**: Anthropic/OpenAI, non-DeepMind academic work.

4. **Multi-agent orchestration architectures (recent papers)** → Researcher 4
   - Orchestrator-worker patterns beyond the original, hierarchical agents,
     debate/critique/verification graphs, agent-to-agent protocols (A2A),
     async vs sync execution, dynamic team composition, role specialization.
   - Focus on **architectures**, not specific lab products (those are 1-3).

5. **Agent harness & context engineering** → Researcher 5
   - Context-window management for long-running agents, hierarchical memory
     (working/episodic/semantic/procedural), file-based scratchpads,
     attention-sink and KV-cache strategies, subagent isolation, compaction
     techniques, prompt-caching for agents, "context rot" mitigations.

6. **Test-time compute & inference-time reasoning for agents** → Researcher 6
   - Verifier-guided search, MCTS for agent action selection, self-consistency,
     reasoning RL (post-DeepSeek-R1), o-series-style deliberation, parallel
     sampling + selection, ensembles, debate-as-TTC, "thinking tokens" budget
     allocation for agents.

7. **Benchmarks, evals, and capability landscape** → Researcher 7
   - HLE (Humanity's Last Exam), SWE-Bench Verified, GAIA, TAU-Bench, BrowseComp,
     ARC-AGI-2/3, METR HCAST + RE-Bench (50% / 80% time horizons), AgentBench,
     MLE-Bench, novel 2026 benchmarks. What's saturated vs. open.

8. **Open-source agent frameworks & emerging architectural patterns** →
   Researcher 8
   - SWE-agent / OpenHands / Devin successors, CrewAI / AutoGen / LangGraph
     evolutions, MetaGPT, open multi-agent research systems, novel
     architectures (e.g., neurosymbolic agents, RL-trained orchestrators).
   - **Excludes**: pure lab products (1-3) and pure architectural theory (4).

## Expected Output

1. `files/research_notes/{1..8}_*.md` — raw findings per researcher.
2. `files/research_notes/9..._gap_*.md` — second-wave gap-fill notes.
3. `files/data/data_summary.md` — benchmark numbers + capability deltas.
4. `files/charts/*.png` — visualizations of capability progression,
   architecture-pattern frequency, benchmark deltas.
5. `files/reports/sota_agents_2026_report.md` — synthesized cited report.
6. **`files/reports/SKILL_v2_proposal.md`** — concrete, actionable redesign of
   this `deep-research` skill, mapping each finding → skill change. This is
   the user's primary deliverable.
7. `files/reports/citation_audit.md` — citation verification.

## Operating Principles for This Run

- Researchers MUST run on Opus 4.7 (user policy).
- Hard stop per researcher: 20 searches OR 90 minutes of investigation.
- All findings cite full URLs.
- Findings preferring PRIMARY sources (papers, lab blogs, official model cards).
- If a researcher hits a dead end on a sub-question, they note the gap and move on.
- Each finding tagged with **Confidence** (HIGH/MED/LOW) and **Skill-Impact**
  (DIRECT / INDIRECT / NONE) so the SKILL_v2 author can filter quickly.
