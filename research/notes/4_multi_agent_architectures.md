# Multi-Agent Orchestration Architectures (Nov 2025 – May 2026)
## Researcher 4 — 2026-05-20

This brief surveys generalizable architectural patterns for LLM multi-agent systems published Nov 2025 – May 2026. Each finding lists: Detail · Source · Confidence · **Skill-Impact** (how a `deep-research` skill could adopt the pattern). Lab products are cited only when the architecture paper itself introduces a generalizable idea.

---

### Orchestrator-Worker Evolutions

**Finding 1 — Benchmarked taxonomy of 4 orchestration patterns** (Mar 2026)
- **Detail:** Compared sequential pipeline, parallel fan-out + merge, hierarchical supervisor-worker, and reflexive self-correcting loop across 10K SEC filings on 5 frontier LLMs. Reflexive achieves highest accuracy (F1 0.943) at 2.3× sequential cost. Hierarchical supervisor-worker sits on the Pareto frontier (F1 0.921 at 1.4× cost). A hybrid with semantic caching, model routing, and adaptive retry recovers 89% of reflexive gains at 1.15× cost.
- **Source:** https://arxiv.org/abs/2603.22651
- **Confidence:** High (large empirical study)
- **Skill-Impact (DIRECT):** Use hierarchical supervisor-worker as default; add a reflexive critic pass *only* on findings flagged as low confidence by the orchestrator. Cache subagent outputs by query signature. Adaptive retry instead of "always reflect."

**Finding 2 — Orchestration Traces formalism** (May 2026)
- **Detail:** "Orchestration traces" = temporal interaction graphs whose events include sub-agent spawning, delegation, communication, tool use, return, aggregation, and stopping. Decomposes orchestration learning into 5 sub-decisions: (1) when to spawn, (2) whom to delegate to, (3) how to communicate, (4) how to aggregate, (5) when to stop. Identifies 8 reward families (parallelism speedup, split correctness, aggregation quality, etc.) and notes no explicit RL training method exists for the stopping decision. Provides a reusable JSON schema for orchestration traces.
- **Source:** https://arxiv.org/abs/2605.02801
- **Confidence:** High (curated 84-paper pool; bridges academia and industrial systems)
- **Skill-Impact (DIRECT):** Log every Researcher dispatch as a trace event using this schema. The 5 sub-decisions become explicit knobs in the lead-orchestrator: spawn threshold, delegation policy, message budget, aggregation strategy, stop condition. Enables future RL-on-traces optimization.

**Finding 3 — Hierarchical planner-executor with context decoupling (CoDA)** (Dec 2025)
- **Detail:** A single shared LLM plays Planner and Executor with role-specific context windows so high-level strategy doesn't get polluted by tool noise. Uses PECO (Planner-Executor Co-Optimization), a trajectory-level reward jointly training both roles.
- **Source:** https://arxiv.org/html/2512.12716v1
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** Strong argument for *splitting* the lead-research context from per-researcher contexts. The lead never sees tool-output noise; researchers never see the global plan. Researcher 4 already does this implicitly — formalize the boundary.

**Finding 4 — Multi-agent orchestration for incident response (deterministic SLAs)** (Nov 2025)
- **Detail:** Multi-agent system achieved 100% actionable-recommendation rate vs 1.7% for single-agent; 80× action specificity and 140× solution correctness; **zero quality variance across trials**. Latency similar (~40s). Introduces Decision Quality (DQ) metric.
- **Source:** https://arxiv.org/abs/2511.15755
- **Confidence:** High (empirical)
- **Skill-Impact (INDIRECT):** Big lesson: multi-agent's win is *determinism/reliability* under fixed budget, not speed. Useful framing for justifying the skill's complexity.

---

### Debate & Verification Graphs

**Finding 5 — Courtroom-style debate with Progressive RAG (PROClaim)** (Mar 2026)
- **Detail:** 5 adjudication roles (Plaintiff, Defense, 3 heterogeneous Judges using different underlying models to prevent collusion via shared representations). Progressive RAG dynamically expands the evidence pool during debate, rather than retrieving once. On Check-COVID zero-shot: 81.7% accuracy, +10.0 pts over standard MAD; P-RAG alone contributes +7.5 pts.
- **Source:** https://arxiv.org/abs/2603.28488
- **Confidence:** High
- **Skill-Impact (DIRECT):** For "fact-check this finding" passes, instantiate 2 advocate agents + 3 heterogeneous judges (different model families). Re-search during debate (don't lock evidence at start). Tag each citation in the final report with "verified by heterogeneous panel" status.

**Finding 6 — Adaptive Heterogeneous Multi-Agent Debate (A-HMAD)** (2026)
- **Detail:** Heterogeneous agent ensemble — each agent gets a specialized role and a *distinct model type*. Adaptive routing of which agents debate which topics.
- **Source:** https://link.springer.com/article/10.1007/s44443-025-00353-3
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** Don't use the same model for every agent — heterogeneity is a structural defense against shared blindspots. Researchers should ideally use mixed providers (Claude / GPT / Gemini / open-weight) when budget permits.

**Finding 7 — Agent-as-a-Judge paradigm + survey** (Jan 2026)
- **Detail:** Replaces static LLM-as-judge with agentic evaluators that plan, use tools (fact-checkers, code executors), maintain memory, and iterate. Survey taxonomizes 4 dimensions: agent architecture, reasoning capability, evaluation scope, feedback integration. Frameworks like CollabEval (multi-agent judges) and AdaRubric (per-step rubric scoring with confidence weights) outperform single-LLM judges.
- **Source:** https://arxiv.org/pdf/2601.05111
- **Confidence:** High (survey)
- **Skill-Impact (DIRECT):** Replace any current LLM-as-judge step in the skill with an agentic judge that can re-search a claim, run code to verify a number, or compare against ground truth.

**Finding 8 — DeepVerifier: rubric-guided test-time verification** (Jan 2026)
- **Detail:** Plug-and-play verifier built on a DRA Failure Taxonomy (5 categories, 13 sub-categories). Produces rubric-based feedback fed back to the agent. +8–11% on hard subsets of GAIA and XBench-DeepSearch; outperforms vanilla agent-as-judge by 12–48% in meta-eval F1. Releases DeepVerifier-4K SFT set focused on reflection/self-critique.
- **Source:** https://arxiv.org/abs/2601.15808
- **Confidence:** High
- **Skill-Impact (DIRECT):** Build a "Deep Research Failure Rubric" (e.g., shallow_sourcing, citation_hallucination, stale_data, missing_counterevidence, scope_drift) and apply it as a verification pass before final synthesis. Major direct lift.

---

### Async / Event-Driven / Speculative Execution

**Finding 9 — Self-Manager: parallel agent loop with Thread Control Blocks** (Jan 2026)
- **Detail:** Borrows OS-thread abstraction. Main thread spawns subthreads with isolated contexts; each managed via a Thread Control Block. Async concurrent execution with iterative supervision. Outperforms single-loop baselines across all metrics on DeepResearch Bench.
- **Source:** https://arxiv.org/pdf/2601.17879
- **Confidence:** High
- **Skill-Impact (DIRECT):** Direct fit for `deep-research`: each Researcher is a subthread with isolated context and a TCB (status, budget, partial results). The lead orchestrator polls or receives events as TCBs update — no global context pollution.

**Finding 10 — PASTE: Pattern-Aware Speculative Tool Execution** (Mar 2026)
- **Detail:** Detects stable control flows (recurring tool-call sequences) and predictable parameter dependencies in agent behavior, then speculatively executes the next tool while the LLM is still reasoning. 48.5% reduction in task completion time, 1.8× tool throughput.
- **Source:** https://arxiv.org/abs/2603.18897
- **Confidence:** High
- **Skill-Impact (INDIRECT):** Mostly for skills with long sequential tool chains. For `deep-research`, less directly applicable than parallel fan-out, but worth keeping in mind for long-tailed Researcher chains.

**Finding 11 — Speculative Actions (lossless)** (Oct 2025, updated)
- **Detail:** Faster model predicts likely future actions and executes them in parallel; commits only when predictions match. Up to 55% next-action prediction accuracy → up to 20% latency reduction. Lossless by construction.
- **Source:** https://arxiv.org/abs/2510.04371
- **Confidence:** High
- **Skill-Impact (INDIRECT):** Could be used to speculatively pre-warm searches the lead orchestrator "probably" wants next, but adds machinery. Optional.

**Finding 12 — Speculative Interaction Agents (Async I/O + speculative tool calling)** (May 2026)
- **Detail:** Decouples reason-and-act thread from waiting on external tools/users. Cloud models 1.3–1.7× speedup; edge models 1.6–2.2×. Uses clock-based training to teach smaller models streaming/async behavior.
- **Source:** https://arxiv.org/abs/2605.13360
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** Lead orchestrator should not block on a single Researcher — it should process partial returns as soon as they stream. SSE / event-driven aggregator instead of waiting for all N to finish.

**Finding 13 — Event-Driven Agent industry convergence** (early 2026)
- **Detail:** Industry adopting event-driven architecture as the default for agent systems: LangGraph 1.0 (Pregel/BSP execution model, state updates as events), AutoGen v0.4 (actor model with typed messages), Google's A2A (SSE for long-running tasks).
- **Source:** https://zylos.ai/research/2026-03-02-event-driven-architecture-ai-agent-systems
- **Confidence:** High (industry-wide trend)
- **Skill-Impact (DIRECT):** Move skill internals from request-response to event-driven message passing between lead and researchers, enabling partial-result aggregation and back-pressure.

---

### Dynamic Team Composition

**Finding 14 — DyLAN: Dynamic LLM-Agent Network** (continuing into 2026)
- **Detail:** Two-stage paradigm — Team Optimization then Task Solving. Selects agents using *Agent Importance Score* (peer-rated backward aggregation, unsupervised). Adjusts composition, topology, and policy in real-time based on input.
- **Source:** https://openreview.net/forum?id=i43XCU54Br
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** After a first pass of all researchers, score their contribution (peer or critic rating). In iteration 2, drop low-scoring agent roles and respawn high-value ones. Solves "I wasted a researcher on a bad subtask."

**Finding 15 — GraphPlanner (ICLR 2026): Graph memory-augmented agentic routing**
- **Detail:** MDP formulation where each step selects both LLM backbone *and* agent role (Planner / Executor / Summarizer). Uses GARNet, a heterogeneous graph capturing query × agent × response interaction memories. Up to +9.3% accuracy and GPU cost from 186 GiB to 1 GiB. Strong zero-shot generalization.
- **Source:** https://openreview.net/forum?id=ZdGB7MNQDT
- **Confidence:** High (ICLR 2026 accepted)
- **Skill-Impact (DIRECT):** Stop hand-coding which model gets which role. Build an interaction memory graph across past research sessions and route role × model selection from it.

**Finding 16 — Automatic Topology Design (AgentConductor, GoAgent, MetaGen, TopoDIM, ARG-Designer)** (early-mid 2026)
- **Detail:** Family of papers that *generate* the multi-agent communication topology automatically. AgentConductor emits YAML topology, executes, regenerates based on validity/cost feedback. GoAgent uses group-centric topology generation. ARG-Designer uses autoregressive graph generation as MAS topology designer.
- **Sources:** https://huggingface.co/papers/2602.17100 · https://arxiv.org/html/2603.19677v1 · https://arxiv.org/html/2507.18224
- **Confidence:** Medium-High (multiple converging papers)
- **Skill-Impact (INDIRECT):** Long-term: the skill could *learn* its own researcher topology per query class. Short-term: pick from a small library of hand-designed topologies based on query taxonomy.

**Finding 17 — Multi-agent Architecture Search (MaAS) via Agentic Supernet** (carrying into 2026 work)
- **Detail:** Searches a probabilistic continuous architecture distribution over agentic operators (CoT, MAD, ReAct) instead of one optimal MAS. Per-layer operator probabilities, selected adaptively.
- **Source:** https://arxiv.org/pdf/2502.04180
- **Confidence:** Medium-High
- **Skill-Impact (INDIRECT):** Future direction — train a supernet of researcher templates and sample per query.

---

### Agent-to-Agent Protocols

**Finding 18 — A2A protocol architecture stabilization** (Apr 2025 launch → mainstream by 2026)
- **Detail:** A2A's architecture has converged on: Agent Cards at `/.well-known/agent-card.json` for discovery, HTTP + Server-Sent Events + JSON-RPC 2.0 for transport, three-role framework (user, client agent, remote agent). MCP+A2A is the de-facto enterprise stack: MCP for vertical tool integration, A2A for horizontal agent coordination.
- **Sources:** https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence · https://arxiv.org/html/2507.21105v1 (AgentMaster, NeurIPS 2025 LAW workshop poster)
- **Confidence:** High (industry convergence + paper presence)
- **Skill-Impact (INDIRECT):** If `deep-research` is to interop with external research agents (academic search agents, code-execution agents owned by other systems), publishing an Agent Card and speaking A2A is the path. Otherwise mostly internal.

**Finding 19 — DALA: VCG-auction communication market** (Nov 2025)
- **Detail:** Agents bid for communication bandwidth via Vickrey-Clarke-Groves auction. Bids = value density (message-value ÷ tokens). Emergent 4-tier strategy: full message, summary, keywords, strategic silence. 84.32% MMLU, 91.21% HumanEval pass@1. 6.25M tokens on GSM8K vs 14M for competitors. Under tight budget agents go 39.9% silent.
- **Source:** https://arxiv.org/html/2511.13193v1
- **Confidence:** High
- **Skill-Impact (DIRECT):** A token-budget mechanism for the lead orchestrator: each researcher bids to "speak" in the synthesis; low-value researchers stay silent. Major lever for cost control.

**Finding 20 — Blackboard architecture for LLM MAS (data discovery)** (Oct 2025)
- **Detail:** Central agent posts requests to shared blackboard; subordinate agents (data-lake partition specialists, web retrieval agents) *volunteer* to respond based on capability. No central coordinator needs to know agent expertise. 13–57% relative improvement in end-to-end success, up to +9% in F1 on data discovery.
- **Source:** https://arxiv.org/abs/2510.01285
- **Confidence:** High
- **Skill-Impact (DIRECT):** For sub-questions the lead doesn't know how to route, post to a shared workspace and let any registered researcher volunteer. Naturally extensible — adding a new specialist researcher doesn't require touching the orchestrator.

**Finding 21 — Market-Making for safe multi-agent LLMs** (Nov 2025, updated Feb 2026)
- **Detail:** Agents trade probabilistic beliefs about outcomes; profit-seeking drives convergence on truth. +10% accuracy on factual reasoning. Provides interpretable intermediate reasoning trace, scalable without external arbiter.
- **Source:** https://arxiv.org/abs/2511.17621
- **Confidence:** Medium-High
- **Skill-Impact (INDIRECT):** Promising but experimental. Could replace flat synthesis with belief-market consensus on contentious claims. Useful for forecasting-style research questions.

---

### Mixture-of-Agents / Ensembles

**Finding 22 — Attention-MoA: critique-and-refine MoA** (Jan 2026)
- **Detail:** Two upgrades to standard MoA: (1) Inter-agent Semantic Attention — agents generate natural-language critiques of peers' responses and self-refine; (2) Inter-layer Residual — keeps historical context, adaptive early stop. Scales monotonically across 5 layers (vanilla MoA degrades past 3). ~11% token reduction, 91.15% AlpacaEval 2.0 LC win rate, MT-Bench 9.32.
- **Source:** https://arxiv.org/html/2601.16596v1
- **Confidence:** High
- **Skill-Impact (DIRECT):** When synthesizing across N researchers, do a critique pass between layers (each researcher reads and critiques peers' outputs) before final aggregation. Stop early when responses converge.

**Finding 23 — Pyramid MoA** (2026)
- **Detail:** Hierarchical MoA with a lightweight router that decides whether a query needs full multi-model processing or can be answered by a smaller subset. Addresses the cost inefficiency of standard MoA.
- **Source:** https://www.spheron.network/blog/mixture-of-agents-gpu-cloud/
- **Confidence:** Medium
- **Skill-Impact (DIRECT):** Easy queries should hit a cheap subset of researchers; only hard / cross-domain queries get the full pyramid.

**Finding 24 — "Wisdom of the silicon crowd" / Collective intelligence in LLM crowds**
- **Detail:** Ensembles of ~12 LLMs perform on par with human crowd forecasting on probabilistic questions about future events. For vision/estimation tasks, combining diverse models' *deterministic* outputs produces a wisdom-of-crowds effect.
- **Sources:** https://www.science.org/doi/10.1126/sciadv.adp1528 · https://openreview.net/forum?id=fxqroxvUhk
- **Confidence:** High
- **Skill-Impact (INDIRECT):** For forecasting-flavored research queries, spawn N independent identically-prompted researchers and take a calibrated aggregate, not a "best."

---

### Generator-Evaluator (Evolutionary / Tournament)

**Finding 25 — AlphaEvolve as the canonical generator-evaluator template**
- **Detail:** Loop of LLM-generator + automated evaluators that scores candidate algorithms; evolutionary search with island populations. Beat Strassen on 4×4 complex matmul (48 mults vs 49), improved data-center scheduling. The generalizable pattern: (1) LLM proposes mutations to a candidate, (2) auto-evaluator scores, (3) elite/island selection updates the pool, (4) repeat.
- **Source:** https://arxiv.org/abs/2506.13131
- **Confidence:** High
- **Skill-Impact (DIRECT):** For any well-scored sub-question (e.g. "what is the SOTA on X benchmark?"), use a generator-evaluator loop — propose answers, evaluate against retrieved evidence, keep top-K, mutate. Much higher accuracy than one-shot.

**Finding 26 — EvoScientist: 3-agent evolutionary discovery** (Mar 2026)
- **Detail:** Researcher Agent (ideas) + Engineer Agent (code/experiments) + Evolution Manager Agent (distills history into reusable knowledge). Two persistent memories: Ideation Memory (top-ranked + failed directions) and Experimentation Memory (effective strategies from code-search trajectories).
- **Source:** https://arxiv.org/pdf/2603.08127
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** Add a third agent role — Evolution Manager — that persists across sessions, accumulating "what worked / what failed" for this skill. Borderline overlaps with skill libraries (Voyager-style).

**Finding 27 — SAGE / SKILLRL: recursive skill libraries with RL** (Dec 2025–Mar 2026)
- **Detail:** SAGE ("Skill Augmented GRPO for Self-Evolution") formalizes the Voyager skill-library pattern with RL. Sequential Rollout deploys agents across chains of similar tasks; reusable functions are tested and saved to a persistent library. +8.9% Scenario Goal Completion, −59% output tokens. SKILLRL uses experience-based distillation to transform diverse experiences into structured skills (vs storing raw trajectories).
- **Sources:** https://arxiv.org/pdf/2602.08234 · https://arxiv.org/pdf/2512.17102
- **Confidence:** High
- **Skill-Impact (DIRECT):** Add a skills/ subdirectory to the skill; each time a researcher pattern is reused (e.g. "find pricing for SaaS competitors") save the working prompt + tool sequence as a reusable named skill. Future invocations check the library first.

**Finding 28 — CATArena: tournament-style iterative competition** (Oct 2025)
- **Detail:** Agents compete in multi-turn tournaments across 4 board/card games. Each round: agents code → tournament → rankings → analyze logs → refine code. Decoupled metrics: *static generation proficiency* (initial quality) vs *evolutionary potential* (improvement capacity) — these are uncorrelated. Notable: agents struggle to concurrently leverage *both* peer-learning and self-reflection.
- **Source:** https://arxiv.org/html/2510.26852v1
- **Confidence:** High
- **Skill-Impact (DIRECT):** When N researchers produce competing answers, run them in tournament rounds where each sees competitors' outputs and self-reflects. Don't just merge — let them refine through competition. Watch out: agents combine peer-learn + self-reflect *poorly*, so structure the rounds to alternate rather than mix.

**Finding 29 — Best-of-N improvements: GenSelect / Majority-of-Bests / MoB**
- **Detail:** GenSelect: LLM uses long reasoning to select best of N candidates rather than scalar reward model. Small models can acquire strong GenSelect via RL. MoB: bootstrap subsets and majority-vote, dominates straight Best-of-N.
- **Sources:** https://arxiv.org/pdf/2507.17797 · https://arxiv.org/pdf/2511.18630
- **Confidence:** High
- **Skill-Impact (DIRECT):** For final answer selection, don't use a scalar reward — generate N candidate syntheses, then have a strong model do long-reasoning selection, or run majority-of-bests bootstrap voting.

---

### Tree / Plan / Search Patterns at the Agent Level

**Finding 30 — Task-Decoupled Planning (TDP)** (2026)
- **Detail:** Decomposes a task into a DAG of sub-goals with *scoped* contexts. Replanning is confined to the active sub-task. Reduces token consumption by up to 82%.
- **Source:** Referenced via plan-and-solve search; akin to https://arxiv.org/html/2510.07772v1
- **Confidence:** Medium-High
- **Skill-Impact (DIRECT):** Build research queries as a DAG of sub-questions with isolated contexts (matches what Researcher 4's structure already does). When one fails, replan only that node.

**Finding 31 — HiPlan: hierarchical planning with adaptive global-local guidance** (continuing 2025-2026)
- **Detail:** Separate global plan from local execution; adaptive switching based on progress signals.
- **Source:** https://arxiv.org/pdf/2508.19076
- **Confidence:** Medium
- **Skill-Impact (DIRECT):** Lead orchestrator holds a global plan; researchers hold local plans. Provides a re-planning interface.

**Finding 32 — Scheduler-theoretic framework (SGH)** (Apr 2026)
- **Detail:** Treats agent loops as a scheduler with a single ready unit. Introduces Structured Graph Harness: control flow as explicit static DAG, three layers (planning / execution / recovery), commitment to immutability within a version, explicit escalation protocol.
- **Source:** https://arxiv.org/html/2604.11378v1
- **Confidence:** Medium-High (theoretical / design paper)
- **Skill-Impact (DIRECT):** Make the skill's execution graph an explicit, immutable DAG per session. Researchers cannot rewrite the plan mid-flight; failures escalate to the lead via a defined protocol.

**Finding 33 — Devil's Advocate / Anticipatory Reflection patterns**
- **Detail:** Prior work (continuing into 2026 derivatives) inserts a "devil's advocate" agent that anticipates failure modes *before* execution and a reflection agent *after*.
- **Source:** https://arxiv.org/pdf/2405.16334
- **Confidence:** Medium
- **Skill-Impact (INDIRECT):** Before launching N researchers, run a brief devil's-advocate pass that predicts likely failure modes of the plan.

---

### MapReduce-Style Fan-out / Fan-in

**Finding 34 — AggAgent: agent-based aggregation as parallel test-time scaling** (Apr 2026)
- **Detail:** Instead of concatenating parallel rollouts (overflows context) or only using final answers (loses info), AggAgent is an *agent* that treats parallel trajectories as an environment: it can inspect candidates and search across trajectories. +5.3% absolute on average, +10.3% on deep-research tasks. Aggregation cost bounded by a single rollout's cost.
- **Source:** https://arxiv.org/abs/2604.11753
- **Confidence:** High
- **Skill-Impact (DIRECT):** Replace the lead orchestrator's flat synthesis step with an *aggregation agent* that can interrogate researcher trajectories (not just final outputs). This is the single highest-leverage architecture change for `deep-research`.

**Finding 35 — Fan-out/Fan-in formalized as production pattern**
- **Detail:** Multiple 2026 sources (Microsoft Agent Framework, AWS Generative AI Atlas) document fan-out/fan-in as the canonical "concurrent agent execution" pattern: parallel spawn → barrier → reduce. Frequently named "scatter-gather" or "MapReduce vibes."
- **Sources:** https://arafattehsin.com/blog/agent-orchestration-patterns-part-3/ · https://awslabs.github.io/generative-ai-atlas/topics/2_0_technical_foundations_and_patterns/2_3_core_archtectural_concepts/2_3_6_orchestration_patterns/1_fan-out-fan-in/fan-out-fan-in.html
- **Confidence:** High (industry consensus)
- **Skill-Impact (DIRECT):** Already the spine of `deep-research`. Practical lesson from these docs: replace strict barrier with streaming reduce (combine with Finding 12).

---

### Cross-References

- **Hierarchical context decoupling (CoDA, F3)** ↔ Researcher 1's hierarchical memory research and context compaction patterns.
- **Skill libraries (SAGE/SKILLRL, F27)** ↔ Researcher 3's Skills / dynamic tool loading work.
- **DeepVerifier rubrics (F8)** ↔ Researcher 5's verifier models and process reward models.
- **A2A/MCP convergence (F18)** ↔ Researcher 7's standards & protocols.
- **Scheduler-theoretic SGH (F32) + Self-Manager TCBs (F9)** ↔ Researcher 2 on checkpoint/resume and durable execution.
- **Generator-evaluator (F25, F26)** ↔ Discovery-oriented OSS (Researcher 10) and HRM/TRM hierarchical reasoning.

---

### Gaps & Open Questions

1. **Stopping criterion is unsolved.** Finding 2 explicitly notes "no explicit RL training method" exists for *when to stop*. Every deep-research skill ships a heuristic here — none are principled.
2. **Optimal team size is empirical.** Industry note: "in 2026 the practical team size is typically three or four agents due to rapidly increasing coordination overhead." No clean theory predicts this. We should A/B test 3 vs 4 vs 6 researchers per query class.
3. **Aggregation > generation.** AggAgent (F34) and AggAgent-class results suggest the *aggregator* now does more work than individual researchers. Future skill versions may invert the budget split.
4. **Heterogeneity vs cost.** Multiple findings (F5, F6) confirm heterogeneous model families improve outcomes (anti-collusion / diverse blindspots). Real cost: provider sprawl. Open question: minimum diversity needed for the gain.
5. **Skill libraries vs prompt drift.** SAGE/SKILLRL store skills as code/functions; deep-research skills are mostly natural-language. Open: is there a code-form representation of a "research recipe" that survives model updates?
6. **Event-driven vs barrier.** Industry is converging on event-driven (F13), but most published deep-research clones still use barrier fan-in. Empirical comparison missing.
7. **Speculative execution rarely measured for research.** F10–F12 demonstrate wins for tool-heavy agents; no public measurement of speculative research-step execution (e.g., pre-warming likely follow-up searches).
8. **Tournament + self-reflection interference (F28).** CATArena's finding that agents combine peer-learning and self-reflection *poorly* suggests current critique loops may be sub-optimal — alternating regimes worth testing.
9. **Auction/market communication (F19, F21).** Strong early results, no production deep-research system has tried VCG-bidded researcher messaging.
10. **No standard benchmark.** DeepResearch Bench (used by F9) is becoming the de-facto benchmark but is not yet ICLR/NeurIPS-cited at scale. Need a community standard.
