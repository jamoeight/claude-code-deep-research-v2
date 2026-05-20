# Test-Time Compute & Reasoning for Agents (Nov 2025 – May 2026)
## Researcher 6 — 2026-05-20

Scope: techniques (not specific models) for trading compute for capability at inference time, with emphasis on the agentic / multi-turn setting. Many headline TTC results from 2024-2025 (Snell et al., DeepSeek-R1, ThinkPRM) targeted single-turn reasoning; the dominant frontier through 2026 is porting those ideas to long-horizon agent trajectories — and discovering that the naive ports fail.

---

### Verifier-Guided Search (PRMs, value functions)

**Finding 1 — PRMs migrate from math to agent trajectories ("AgentPRM").**
AgentPRM proposes step-wise "promise and progress" scoring for LLM agent trajectories using TD estimation + GAE. Trained via Monte Carlo rollouts in actor-critic style; 8x more compute-efficient than baselines; on ALFWorld a 3B model trained with AgentPRM outperforms GPT-4o.
- Source: https://arxiv.org/abs/2511.08325 ; ACM Web Conf 2026 https://dl.acm.org/doi/10.1145/3774904.3792551
- Confidence: High (clean numbers, code released)
- Skill-Impact: High — provides a concrete recipe for step-level verifier on agent trajectories.
- Apply: When a skill needs trajectory-aware verification, use "promise" (closeness to goal) + "progress" (advancement) as two-axis reward instead of binary success.

**Finding 2 — ToolPRMBench: PRM benchmark dedicated to tool-using agents.**
First systematic eval of PRMs in tool-use settings; converts agent trajectories into step-level cases (history + correct action + incorrect alternative + tool metadata). Online and offline sampling pipelines. Finding: tool-specialized PRMs significantly beat general PRMs and LLM-as-judge.
- Source: https://arxiv.org/html/2601.12294
- Confidence: High
- Skill-Impact: Medium — confirms that generic PRMs underperform on tool-use; skills with their own verifier should domain-specialize.
- Apply: Don't reuse a math PRM for tool-using verification — train or prompt-specialize.

**Finding 3 — Course-correcting SWE agents with PRMs (SWE-PRM, NeurIPS 2025).**
Inference-time PRM intervenes during execution to detect redundant exploration, looping, and failure-to-terminate. Taxonomy-guided feedback; lightweight sliding window over past steps. SWE-bench Verified: 40.0% → 50.6% (+10.6pp) at ~$0.20 extra inference cost. Largest gains on medium/hard tasks.
- Source: https://arxiv.org/abs/2509.02360
- Confidence: High
- Skill-Impact: High — directly applicable pattern: midstream verifier that detects pathological trajectories.
- Apply: Inject periodic "are we stuck/looping/done?" check using a taxonomy of failure modes rather than scoring all steps.

**Finding 4 — ThinkPRM (generative long-CoT PRM).**
Discriminative PRMs are expensive to train (PRM800K-scale labels). ThinkPRM is a verifier that writes a verification CoT, fine-tuned on 1K synthetic verification chains from 8K labels (1% of PRM800K). Beats LLM-as-judge and discriminative PRMs on ProcessBench/MATH-500/AIME'24; +8% on GPQA-Diamond OOD, +4.5% on LiveCodeBench. Verifier compute itself can be scaled (think longer / parallel).
- Source: https://arxiv.org/abs/2504.16828
- Confidence: High (model published: ThinkPRM-7B based on DeepSeek-R1-Distill-Qwen-7B)
- Skill-Impact: High — generative verifier means the verifier benefits from TTC scaling too.
- Apply: For a skill's quality gate, prefer a generative verifier that produces a critique — costs more per call but is data-efficient and scales with thinking budget.

**Finding 5 — Value-Guided Search (VGS) for long CoT.**
Avoids fine-grained "step" annotations by training a 1.5B token-level value model on 2.5M reasoning traces; applies block-wise to DeepSeek models. VGS + final weighted majority vote outperforms majority voting / best-of-N. With 64 generations, VGS + DeepSeek-R1-Distill-1.5B reaches o3-mini-medium parity on AIME/HMMT math (avg 45.7%).
- Source: https://arxiv.org/pdf/2505.17373
- Confidence: High
- Skill-Impact: High — strong alternative to PRMs when "step" is fuzzy (true for agent traces).
- Apply: When trajectories don't decompose into discrete steps, train/prompt a token-level value function and use it to weight final voting.

**Finding 6 — E-valuator: sequential hypothesis testing on verifier scores (Dec 2025).**
Converts any black-box verifier into a decision rule with provable false-alarm-rate control. Uses e-processes for sequential hypothesis tests valid at every step; can terminate problematic trajectories early to save tokens. Outperforms ad-hoc thresholds on 6 datasets × 3 agents.
- Source: https://arxiv.org/abs/2512.03109
- Confidence: High
- Skill-Impact: Medium-High — gives statistical rigor to "stop if verifier flags trouble."
- Apply: Wrap verifier scores with e-process sequential test instead of a fixed threshold — better termination guarantees.

**Finding 7 — Process Reward Agents (PRA) — verifier as agent.**
Reframes verification as a separate agent that observes the policy's reasoning trace, decides when to retrieve external evidence, and assigns step rewards. Decouples frozen reasoner from domain-specific reward module. SOTA 80.8% on MedQA with Qwen3-4B; generalizes to 0.5B–8B frozen policies, +up to 25.7% accuracy without policy updates.
- Source: https://arxiv.org/abs/2604.09482
- Confidence: High
- Skill-Impact: High — verifier-as-agent pattern is novel and clearly works for knowledge-intensive tasks.
- Apply: For knowledge-intensive sub-tasks, deploy a separate retrieval-capable verifier-agent rather than embedding verification in the policy.

**Finding 8 — PRINTS for long-horizon information seeking (Nov 2025).**
Reward modeling specifically targeted at deep-research-style information-seeking agents; companion to AgentPRM but for research/browsing rather than embodied tasks.
- Source: https://arxiv.org/pdf/2511.19314
- Confidence: Medium (less coverage at time of writing)
- Skill-Impact: Medium — relevant if skill does long-horizon retrieval.
- Apply: For research agents, score "information gain per step" rather than goal-progress.

---

### MCTS / Tree Search for Agents

**Finding 9 — Tree-GRPO (ICLR 2026): tree-search-based grouped RL for agents.**
Each tree node = full Thought/Action/Observation step (not token or sentence). Shared prefixes amplify rollouts within fixed token+tool budget. Implicit step preferences from outcome rewards alone, no extra PRM needed. Up to +69% relative improvement, especially for small LLMs.
- Source: https://arxiv.org/pdf/2509.21240 ; code https://github.com/AMAP-ML/Tree-GRPO
- Confidence: High
- Skill-Impact: High — this is the dominant 2026 pattern for sampling agent trajectories.
- Apply: When sampling N parallel agent rollouts, branch from shared prefixes (tree) rather than running N independent rollouts — much cheaper.

**Finding 10 — AlphaProof / AlphaEvolve — generalized tree search for discovery.**
AlphaProof (Nature 2025/2026): AlphaZero-style tree search over Lean tactics; IMO silver. AlphaEvolve: LLM-guided evolutionary search over code (program-as-action-space). Both demonstrate the same principle: when you can verify (formal proof, code execution), tree search at inference time produces superhuman results on bounded problems. AlphaEvolve advanced Ramsey theory bounds in 2026.
- Sources: https://www.nature.com/articles/s41586-025-09833-y ; https://arxiv.org/pdf/2511.02864
- Confidence: High (Nature paper)
- Skill-Impact: High — the meta-pattern: spend TTC by searching the action space when verifier is cheap.
- Apply: If a skill operates on a verifiable artifact (code, proof, structured output), wrap generation in a search loop with the verifier as evaluator.

**Finding 11 — RethinkMCTS / I-MCTS / ExACT R-MCTS family.**
- I-MCTS (Jan 2026 v2): "introspective" MCTS for agentic AutoML; LLM critiques its own subtree at each expansion.
- RethinkMCTS: explicitly rewrites erroneous thoughts mid-search for code generation.
- ExACT (Reflective-MCTS): contrastive reflection over past interactions; multi-agent debate at evaluation step.
- Sources: https://arxiv.org/abs/2502.14693 ; https://arxiv.org/html/2409.09584v1 ; https://openreview.net/forum?id=GBIUbwW9D8
- Confidence: High
- Skill-Impact: Medium — MCTS variants are crowded; main lessons are reflection-in-the-loop and contrastive evaluation.
- Apply: When using MCTS over LLM actions, add a reflection/critique step at node expansion — substantially better than vanilla LLM-MCTS.

**Finding 12 — Empirical-MCTS (Feb 2026): MCTS becomes a learner.**
Turns MCTS from stateless inference into a non-parametric online learner. Accumulates "wisdom" across problem instances by storing experience traces keyed by state features. Significant gains on AIME25, ARC-AGI-2, MathArena Apex.
- Source: https://arxiv.org/html/2602.04248v1
- Confidence: Medium-High
- Skill-Impact: High — bridges TTC and persistent memory.
- Apply: Persist successful sub-trees across invocations; reuse on similar problems instead of starting search from scratch.

**Finding 13 — PRM-guided tree search has known limits.**
"Limits of PRM-Guided Tree Search for Mathematical Reasoning" (Oct 2025): branching factor and depth explode; PRMs miscalibrate on intermediate steps and search collapses to local optima or noise. Motivates VGS-style token-level value functions and outcome-only Tree-GRPO.
- Source: https://arxiv.org/pdf/2510.20272
- Confidence: High
- Skill-Impact: Medium — informs when NOT to use PRM-guided tree search.
- Apply: If PRM confidence is low on intermediate steps, fall back to outcome-only search or sample-then-verify.

---

### Parallel Sampling + Selection (Best-of-N variants)

**Finding 14 — CarBoN (Oct 2025): calibrated best-of-N.**
Two-phase TTC: (1) explore via sampling, (2) learn per-input calibration (temperature + additive shift vectors) without retraining. Up to 4x fewer rollouts to reach same accuracy as vanilla BoN.
- Source: https://arxiv.org/abs/2510.15674
- Confidence: High
- Skill-Impact: High — practical efficiency improvement.
- Apply: Before scaling N in best-of-N, run a small calibration probe to set per-prompt temperature/shift.

**Finding 15 — Sequential edge: inverse-entropy weighted voting beats parallel SC (Nov 2025).**
Weighing answers by inverse entropy of their reasoning chains beats parallel majority voting in 95.6% of configurations; gains up to 46.7% accuracy. Sequential reasoning (chain + reflect) outperforms parallel sampling at matched compute.
- Source: https://arxiv.org/pdf/2511.02309
- Confidence: High
- Skill-Impact: High — directly actionable for self-consistency.
- Apply: When doing self-consistency, weight votes by inverse entropy of each chain, not uniform majority.

**Finding 16 — Ranked-voting self-consistency (May 2025).**
Generate ranked answers per chain; aggregate via Instant-Runoff / Borda / mean reciprocal rank. Outperforms first-choice majority.
- Source: https://arxiv.org/abs/2505.10772
- Confidence: Medium-High
- Skill-Impact: Medium — niche but easy upgrade to SC.
- Apply: When candidate answers form a small set, have each chain rank them and aggregate via Borda.

**Finding 17 — Semantic self-consistency (2024 update applied through 2026).**
Soft-match candidate answers via embedding similarity rather than exact-match majority. Scores = avg cosine similarity to all other samples.
- Source: https://arxiv.org/abs/2410.07839
- Confidence: Medium
- Skill-Impact: Medium — needed when answers are free-form text.
- Apply: For long-form answers, semantic voting > token-equality voting.

**Finding 18 — Budget-aware discriminative verification (Oct 2025).**
Generative verifiers are expensive (prefill + sequential decode). A discriminative verifier produces a scalar in one forward pass; hybridize with self-consistency consensus. Under fixed FLOP budget, discriminative+SC matches or beats generative verifier.
- Source: https://arxiv.org/pdf/2510.14913
- Confidence: High
- Skill-Impact: High — informs verifier-cost trade-off.
- Apply: If your verifier eats >50% of TTC, switch to a single-forward-pass discriminative verifier and recover compute for more samples.

**Finding 19 — Multi-LLM repeated sampling (AAAI 2026 ModelSwitch).**
Mix multiple (possibly weaker) models in repeated-sample-then-vote setup. Beats SOTA multi-agent debate at lower cost.
- Source: https://ojs.aaai.org/index.php/AAAI/article/view/39094
- Confidence: Medium-High
- Skill-Impact: High — argues against expensive debate, in favor of cheap diversification.
- Apply: For ensembling, prefer cheap multi-model sampling over expensive multi-agent debate when the task is verifiable.

---

### Reasoning RL & Inference-Time Manifestations

**Finding 20 — Post-DeepSeek-R1 recipe (RLVR + GRPO) is the standard.**
RLVR + GRPO replaced PPO-with-learned-RM as default recipe in 2025. GRPO drops the critic; verifier provides scalar reward; reference model regularizes via KL. Every major lab released a GRPO/DAPO-style reasoning variant by mid-2025. Inference-time manifestation: chain-of-thought emerges from training with binary verifier signal alone; quality of CoT scales with allowed thinking tokens.
- Sources: https://arxiv.org/pdf/2501.12948 ; https://llm-stats.com/blog/research/post-training-techniques-2026
- Confidence: High
- Skill-Impact: Medium (training topic, but inference behavior matters).
- Apply: Trust that modern reasoning models will produce useful CoT under heavy thinking budgets — but only on tasks where they were trained with verifiers.

**Finding 21 — Multi-turn GRPO variants (TL-GRPO, MURPHY, RC-GRPO).**
Outcome-only GRPO has sparse credit assignment over long horizons. New variants add turn-level rewards (TL-GRPO Jan 2026), self-correction (MURPHY Nov 2025), reward-conditioning (RC-GRPO Feb 2026 for multi-turn tool agents). Inference-time effect: agents trained with these become better at sustained multi-step trajectories — they don't just emit longer CoT, they emit longer correct trajectories.
- Sources: https://arxiv.org/html/2601.16480v1 ; https://arxiv.org/pdf/2511.07833 ; https://arxiv.org/pdf/2602.03025
- Confidence: High
- Skill-Impact: Medium — informs what to expect from new-gen multi-turn-trained models.
- Apply: When using a model trained with turn-level rewards, longer trajectories are safer than with vanilla GRPO models.

**Finding 22 — Test-Time RL (Test-Time Reinforcement Learning).**
Adapt directly on the test instance using self-consistency or pseudo-labels from same query. "Amplification Effects" (Mar 2026) paper shows safety/reasoning vulnerabilities — TTRL can amplify both correct AND unsafe behaviors.
- Source: https://arxiv.org/pdf/2603.15417
- Confidence: Medium
- Skill-Impact: Medium — caveat for self-improving agents.
- Apply: Treat test-time self-training carefully — it can amplify whatever the model already prefers, including failure modes.

---

### Deliberative Reasoning / Thinking Budgets

**Finding 23 — Claude Opus 4.7 (April 2026) introduces xhigh effort and Task Budgets.**
New effort tier "xhigh" between high and max. Task Budgets cap total tokens (thinking + tool calls + tool results + output) across an agentic loop, minimum 20K, soft (model-visible). Extended Thinking Budgets removed in favor of adaptive thinking: `thinking: { type: 'adaptive' }` lets the model decide. Reasoning effort dial = engineering UX surface for TTC.
- Sources: https://platform.claude.com/docs/en/build-with-claude/task-budgets ; https://platform.claude.com/docs/en/build-with-claude/extended-thinking
- Confidence: High (vendor docs)
- Skill-Impact: High — direct interface to TTC.
- Apply: Skills should expose a budget knob and pass it through to the API as `effort` + task budget, rather than guessing.

**Finding 24 — Ares: adaptive reasoning effort per agent step (Mar 2026).**
Trains a 1.7B router (Qwen3-1.7B) to pick low/medium/high effort per step in multi-turn agent tasks. Effort labels via multi-trial verification ("minimum effort that reliably reproduces correct action"). GRPO RL on top of SFT. Results: TAU-Bench Retail -52.7% reasoning cost with slight gain over always-high; BrowseComp-Plus -41.8% tokens; WebArena -45.3% tokens with +1.5% perf.
- Source: https://arxiv.org/html/2603.07915v1
- Confidence: High
- Skill-Impact: High — concrete blueprint for per-step effort selection.
- Apply: Don't apply max reasoning to every step — use a tiny classifier to pick effort per step; most steps are easy.

**Finding 25 — Budget-Aware Tool-Use (Nov 2025) — BATS.**
Distinguishes thinking-token scaling from tool-call scaling. "Solely increasing internal thinking effort in agents proves suboptimal" — tool calls determine exploration depth/breadth. Budget Tracker module appends real-time budget status to context; with 10x less budget, achieves comparable accuracy with 40% fewer tool calls and 31% lower cost. Plug-and-play, no retrain.
- Source: https://arxiv.org/html/2511.17006v1
- Confidence: High
- Skill-Impact: High — agent-specific TTC insight.
- Apply: Show the model its remaining budget in every system message — it will self-pace.

**Finding 26 — "Increasing the Thinking Budget is Not All You Need" (Dec 2025).**
Single-knob "more thinking" hits a ceiling fast. Ensemble (summary-of-multiple-responses) wins even at zero thinking budget. Weaker models (Qwen3-4B, DeepSeek-8B) gain less from extended thinking than stronger ones.
- Source: https://arxiv.org/html/2512.19585v1
- Confidence: High
- Skill-Impact: High — challenges naive "scale thinking" approach.
- Apply: Prefer ensemble strategies (summary, SC, debate) over simply turning up the thinking budget — especially on weaker models.

**Finding 27 — Inverse scaling in test-time compute (Anthropic, Jul 2025).**
Longer CoT can actively hurt. DeepSeek R1: 70% → 30% on simple counting with 5 distractors. Frontier reasoning models susceptible across counting, regression, deduction, and "advanced AI risks" task families. Claude Sonnet 4 increases self-preservation expressions in longer traces.
- Source: https://arxiv.org/abs/2507.14417
- Confidence: High
- Skill-Impact: High — sets a ceiling on "just think more."
- Apply: Don't crank thinking budget on tasks with distractors or simple deductive structure — diminishing-to-negative returns.

**Finding 28 — Deliberative Alignment (Dec 2024) — safety as TTC.**
Train models to reason explicitly through safety specs before answering. o1-style models advance the Pareto frontier of jailbreak refusal vs. overrefusal. CADA (Jan 2026) follow-up: case-augmented version using RL on self-generated safety reasoning chains.
- Sources: https://arxiv.org/abs/2412.16339 ; https://arxiv.org/abs/2601.08000
- Confidence: High
- Skill-Impact: Medium — relevant for safety-sensitive skills.
- Apply: For high-stakes actions, force the model to spend thinking budget on policy compliance reasoning before tool calls.

---

### Debate as TTC

**Finding 29 — Single-agent matches multi-agent under equal token budget (CMU, May 2026).**
Data Processing Inequality argument: under fixed token budget with perfect context utilization, single-agent is information-efficient; MAS only wins when single-agent's context utilization is degraded OR when extra compute is genuinely spent. "Debate" is often just disguised TTC.
- Sources: https://arxiv.org/abs/2604.02460 ; https://beancount.io/bean-labs/research-logs/2026/05/31/single-agent-outperforms-multi-agent-equal-token-budget
- Confidence: High
- Skill-Impact: High — re-evaluate when debate is worth the cost.
- Apply: Before adding debate, check if you're just buying TTC — a single agent with more thinking budget may match it.

**Finding 30 — Revisiting Multi-Agent Debate as TTS (May 2025, systematic).**
Conditional effectiveness: debate helps when individual agents disagree productively, hurts when they collapse to consensus too fast. Suggests measuring divergence as a precondition for spending compute on debate.
- Source: https://arxiv.org/pdf/2505.22960
- Confidence: High
- Skill-Impact: High — gives a precondition test.
- Apply: Run cheap divergence probe (e.g., 2-3 samples) before committing to a debate; if they agree, skip debate.

**Finding 31 — MACI: budget-aware multi-agent debate (Oct 2025).**
Converts debate into a budget-aware, measurable, provably-terminating controller. Dual-dial control for reliable LLM reasoning.
- Source: https://arxiv.org/pdf/2510.04488
- Confidence: Medium-High
- Skill-Impact: Medium-High — production-grade debate framework.
- Apply: If debate is justified, use a debate controller with explicit termination conditions, not open-ended round counts.

---

### Ensembling & Frame Diversity

**Finding 32 — Dipper: diverse-prompt ensembling at inference.**
Single base model, multiple diverse prompts in parallel → ensemble. Dipper(3 × Qwen2-Math-1.5B) beats 7B baseline. Training-free; CFE-style ensemble.
- Source: https://arxiv.org/html/2412.15238v1
- Confidence: High
- Skill-Impact: Very High — direct validation of Counterfactual Frame Ensemble approach.
- Apply: CFE skill: this is the canonical reference for why diverse prompt frames over a single model beat a larger single-prompt model.

**Finding 33 — Universal Model Routing (UniRoute, Feb 2025) + 2026 follow-ups.**
Represent each LLM as a feature vector; learn router to send each query to smallest sufficient model. Handles 30+ unseen LLMs at test time. Clustering-based routing achieves Pareto-better accuracy at lower cost than any single model.
- Sources: https://arxiv.org/abs/2502.08773 ; https://arxiv.org/abs/2603.04445
- Confidence: High
- Skill-Impact: High — pattern for cost-aware orchestration.
- Apply: Skills with mixed difficulty queries should route, not always invoke the heavy reasoning model.

**Finding 34 — Consensus ensembles +7-15pp over best single model.**
Sending same prompt to multiple distinct models and aggregating responses raises accuracy 7-15 points over best single, with no fine-tuning. RMSE -18.6% in regression-style evals.
- Source: https://www.swfte.com/blog/intelligent-llm-routing-multi-model-ai
- Confidence: Medium (engineering blog, gets directionally right; cite Dipper-style academic sources for rigorous numbers)
- Skill-Impact: Medium-High
- Apply: For consequential decisions, query 3 distinct models (not just 3 samples from one).

---

### Compute-Optimal Allocation

**Finding 35 — T² scaling (Apr 2026): inference budget makes overtraining compute-optimal.**
Joint optimization of model size N, training tokens, and inference samples k under a single budget. Key formula: optimal k = C_inf / (2N) — smaller models get more samples because they're cheaper per sample. Tested with 21 newly-trained heavily-overtrained checkpoints; predictions hold across 8 downstream tasks.
- Source: https://arxiv.org/abs/2604.01411
- Confidence: High (validated by new training runs)
- Skill-Impact: High — informs choice between bigger model vs. more samples.
- Apply: Given fixed inference budget, prefer smaller model + more samples over larger model + fewer samples, up to where per-sample quality drops below threshold.

**Finding 36 — Kinetics (Jun 2025): memory access dominates compute in TTC.**
Prior compute-optimal analyses ignored memory access. Attention, not parameter count, is dominant cost in TTC because long generations + multiple samples blow up KV cache reads. Kinetics scaling law: smaller models are LESS efficient than prior work claimed once memory is counted. Sparse attention is the unlock.
- Source: https://arxiv.org/abs/2506.05333
- Confidence: High
- Skill-Impact: High — overturns intuition that small models + big N is always best.
- Apply: If using long-CoT TTC, switch to a sparse-attention backbone if available; small dense models lose their advantage.

**Finding 37 — Snell et al. (Aug 2024) — foundational compute-optimal TTC paper.**
Adaptive TTC allocation by prompt difficulty; compute-optimal scaling can beat 14x larger pretrained model. Two mechanisms: search against PRM, or adapt response distribution at test time. Inspired o1, R1, follow-up scaling-law work.
- Source: https://arxiv.org/abs/2408.03314
- Confidence: High (highly cited foundational paper)
- Skill-Impact: Very High — the baseline of the field.
- Apply: Treat per-prompt difficulty-aware TTC allocation as table stakes, not optional.

**Finding 38 — "Every Rollout Counts" (Jun 2025) — optimal resource allocation for TTC.**
Formalizes when to spend on parallel samples vs. tree depth vs. verification.
- Source: https://arxiv.org/pdf/2506.15707
- Confidence: Medium
- Skill-Impact: Medium
- Apply: For verifiable tasks, lean toward parallel sampling; for non-verifiable, lean toward sequential refinement.

---

### Adaptive Computation

**Finding 39 — TrACE (Apr 2026): inter-rollout action agreement is a FREE adaptive-compute signal.**
Sample candidate next actions at each step; commit immediately if they agree, sample more (up to a cap) if they disagree. No learned components, no verifier, no labels. TrACE-4 matches SC-4 with 33% fewer calls on GSM8K, 39% fewer on MiniHouse; TrACE-8 matches SC-8 with 55% / 65% fewer calls. Works at the agent step level, not just token level.
- Source: https://arxiv.org/abs/2604.08369
- Confidence: High
- Skill-Impact: Very High — pure plug-and-play adaptive compute for agents.
- Apply: At every agent step, sample 2-3 candidate actions; if they match, commit; if not, sample up to N more. Free win.

**Finding 40 — Anytime Verified Agents (AVA) — calibrated uncertainty + VoI search + selective verification cascades.**
Three-component framework: (1) calibrated uncertainty estimation, (2) value-of-information-guided search expansion, (3) selective verification with early exit. Reduces cost at matched reliability thresholds across GSM8K/MATH/HotpotQA/HumanEval with GPT-5/GPT-4o backends.
- Source: https://openreview.net/forum?id=JMDCMf7mlF
- Confidence: High
- Skill-Impact: High — production-quality adaptive controller.
- Apply: Skills with budget constraints should adopt this three-piece architecture explicitly.

**Finding 41 — "Adaptive TTC Allocation via Learned Heuristics" (Feb 2026, Apr 2026).**
Two-stage Solve-then-Learn pipeline: Lagrangian relaxation finds per-instance optimal "oracle action" balancing accuracy vs. cost; lightweight classifier predicts oracle from cheap features. +12.8% on MATH under matched budget; 91%+ imitation accuracy of oracle.
- Sources: https://arxiv.org/abs/2602.03975 ; https://arxiv.org/abs/2604.14853
- Confidence: High
- Skill-Impact: High — gives recipe for learning the right TTC dial.
- Apply: For a recurring skill workload, learn a small classifier that maps query features → compute budget.

**Finding 42 — "Learning When to Plan" (DeepMind, Sep 2025).**
There's a Goldilocks planning frequency — always-planning (ReAct) wastes compute and degrades long-horizon perf; never-planning caps capability. Two-stage SFT + RL training in Crafter learns dynamic planning. Agents become steerable by human plans.
- Source: https://arxiv.org/abs/2509.03581
- Confidence: High
- Skill-Impact: High — direct guidance on when agents should think.
- Apply: Don't think every turn; learn or heuristically detect "decision points" requiring planning.

**Finding 43 — D-LLM: token-adaptive compute allocation.**
Per-token decision on whether to spend compute. Up to 45% cost / KV-cache reduction on Q&A / summarization / math; 50% on commonsense.
- Source: https://openreview.net/forum?id=UIOjGTKHQG
- Confidence: Medium-High
- Skill-Impact: Medium — relevant for inference infra, less directly for skill design.
- Apply: If you control inference stack, look at token-level dynamic compute, not just request-level.

---

### Speculative & Draft-and-Verify at Agent Level

**Finding 44 — Speculative Actions (Oct 2025): lossless framework.**
Speculatively execute tool calls / API calls / MCP calls in parallel with LLM reasoning; verify by semantic match when LLM commits. 2-3x latency reduction; lossless (final outputs identical to sequential).
- Source: https://arxiv.org/pdf/2510.04371
- Confidence: High
- Skill-Impact: High — production latency win.
- Apply: For deterministic, side-effect-free tool calls, speculatively dispatch them based on action pattern prediction.

**Finding 45 — Pattern-Aware Speculative Tool Execution (SPAgent).**
Pattern Analyzer predicts upcoming tool calls; Online Scheduler launches them speculatively within compute budget. 1.08x–1.65x speedup over baseline. Specific to tool-call serial-dependency bottleneck.
- Source: https://arxiv.org/html/2603.18897
- Confidence: Medium-High
- Skill-Impact: Medium-High
- Apply: If tool calls follow patterns (e.g., search → read → search), prefetch the next likely call.

**Finding 46 — Reducing Latency of LLM Search Agents via Speculation (Nov 2025).**
Some speculative actions don't need verification if cost of wrong speculation is recoverable. Skips verification on early steps for further savings.
- Source: https://arxiv.org/pdf/2511.20048
- Confidence: Medium
- Skill-Impact: Medium
- Apply: For early-stage exploratory actions with cheap rollback, skip verification entirely.

---

### TTC for Tool-Using Agents Specifically

**Finding 47 — General AgentBench (Feb 2026): agent TTC has hard limits.**
Systematic study across search/coding/reasoning/tool-use. Two failure modes: (1) Sequential scaling = context ceiling: agent perf peaks at 3-7 turns on general tasks; beyond that, accumulated context degrades performance. (2) Parallel scaling = verification gap: more trajectories raises upper bound but model self-selection can't close the gap.
- Sources: https://arxiv.org/abs/2602.18998 ; https://effloow.com/articles/agent-test-time-compute-scaling-context-ceiling-2026
- Confidence: High (10 leading agents evaluated)
- Skill-Impact: Very High — empirical ceiling on agent TTC.
- Apply: Default agent budget = 3-7 turns; for parallel scaling, an external verifier is non-optional.

**Finding 48 — Agentic TTC for WebAgents (CATTS).**
Uniformly increasing per-step compute saturates in long-horizon environments. CATTS dynamically allocates per-step compute. Reinforces General AgentBench thesis.
- Source: https://arxiv.org/abs/2602.12276
- Confidence: High
- Skill-Impact: High
- Apply: For web agents, allocate compute per step adaptively, not uniformly.

**Finding 49 — Scaling TTC for Agentic Coding (Apr 2026).**
Trajectory compression: convert each rollout into structured summary (hypotheses + progress + failure modes) instead of raw trace. Two scaling axes: Recursive Tournament Voting (parallel) + Parallel-Distill-Refine (sequential). Claude-4.5-Opus: 70.9% → 77.6% on SWE-Bench Verified; Terminus 1: 46.9% → 59.1% on Terminal-Bench v2.0.
- Sources: https://arxiv.org/abs/2604.16529 ; https://www.emergentmind.com/papers/2604.16529
- Confidence: High
- Skill-Impact: Very High — agent TTC needs summaries, not raw replay.
- Apply: When scaling N for coding agents, summarize each rollout (~1K tokens) instead of feeding raw trajectories; tournament-vote between summaries.

**Finding 50 — BrowseConf (Oct 2025): confidence-driven retry for web agents.**
Verbalized confidence after long action sequences correlates with accuracy (high conf ≈ accurate; low conf ≈ near-zero). Retry with summary-guided or negative-constrained variants until confidence threshold met. Cuts tokens while matching fixed-budget baselines.
- Source: https://arxiv.org/abs/2510.23458
- Confidence: High
- Skill-Impact: High
- Apply: Have agents self-report confidence; retry low-confidence answers up to N times.

**Finding 51 — DeepVerifier (Jan 2026): rubric-guided verification for deep research agents.**
Construct DRA Failure Taxonomy (5 categories, 13 subcategories); generate rubrics per failure mode. Plug-and-play verifier feeds critique back to agent for refinement. +12-48% F1 in meta-eval; +8-11% accuracy on GAIA / xbench-DeepResearch. Published DeepVerifier-4K SFT dataset (4646 high-quality verification steps).
- Source: https://arxiv.org/abs/2601.15808
- Confidence: High
- Skill-Impact: Very High — best-documented agent-level verifier with full taxonomy.
- Apply: For deep-research skills, build a failure taxonomy and a rubric-based verifier specific to your domain.

**Finding 52 — Asymmetric Verification for Deep Search (Oct 2025).**
Verifying is often cheaper than generating. Allocate small fraction of compute to verifier; scale parallel generation. Open-source GLM-4.5 Heavy: 54.0% BrowseComp, 66.0% GAIA, 68.0% xbench-DeepSearch. Tongyi-DeepResearch Heavy: 69.0% BrowseComp. Up to +27 absolute points.
- Source: https://arxiv.org/abs/2510.06135
- Confidence: High
- Skill-Impact: Very High
- Apply: Allocate ~10-20% of TTC to verifier; use the rest for parallel generation.

**Finding 53 — MATTRL (Jan 2026): test-time RL for multi-agent reasoning.**
Inject structured textual experience into multi-agent deliberation at inference time. Turn-level experience pool re-injected into dialogue. +3.67% over multi-agent baseline; +8.67% over single-agent. Robust to distribution shift, no tuning required.
- Source: https://arxiv.org/abs/2601.09667
- Confidence: High
- Skill-Impact: High
- Apply: Maintain a persistent textual experience pool across runs; replay relevant snippets at the right turn.

---

### Reasoning Models Orchestrating Non-Reasoning Models

**Finding 54 — The Conductor and the Engine (Sep 2025).**
When both an external orchestration framework (Conductor) and the internal reasoning model (Engine) try to do high-level reasoning, they produce redundant or conflicting operations. Co-designed reasoning: one of them must defer.
- Source: https://arxiv.org/pdf/2509.19762
- Confidence: Medium-High
- Skill-Impact: High — directly informs agent architecture.
- Apply: Pick one — either the orchestrator plans and the model executes (engine mode), or the model plans and the orchestrator dispatches (conductor mode). Not both.

**Finding 55 — Routing reasoning vs. non-reasoning models in practice.**
2026 deployments commonly use a strong reasoner (o3, Opus 4.7-xhigh) for orchestration and planning, with cheaper non-reasoning models (GPT-4o-mini, Haiku, Flash) handling subroutines like summarization, classification, tool-result parsing. Direct evidence: pricing differentials (DeepSeek V4-Flash at $0.28/MTok, o3-pro at $20/$80) make this economic.
- Source: https://awesomeagents.ai/pricing/reasoning-model-pricing/
- Confidence: Medium (industry pattern, not single paper)
- Skill-Impact: High
- Apply: Default architecture: reasoning model as orchestrator only; delegate every "deterministic transformation" subtask to a cheap non-reasoning model.

**Finding 56 — Interspeech 2026 Audio Reasoning Challenge: agent-as-orchestrator wins.**
Agent track allows multi-model orchestration (ASR, separators, captioners, planners). Results: agent systems lead in reasoning quality vs. monolithic large reasoning models, by iteratively orchestrating tools.
- Source: https://audio-reasoning-challenge.github.io/
- Confidence: High (formal benchmark)
- Skill-Impact: High — empirical validation in audio domain.
- Apply: For multi-modal subtasks, an orchestrating reasoner + specialist tools beats one monolithic model.

---

### Cross-References

- **General AgentBench (#47)** and **Agentic TTC for WebAgents (#48)** are the canonical "agent TTC has limits" papers — cite together when discussing why naive TTC fails on agents.
- **Tree-GRPO (#9)** and **AgentPRM (#1)** are the canonical training-time pairings to the inference-time techniques in this report.
- **TrACE (#39)** and **AVA (#40)** are both adaptive-compute, but TrACE is training-free and AVA is more sophisticated — TrACE first, AVA second.
- **Dipper (#32)** is the academic backing for the CFE skill (Counterfactual Frame Ensemble).
- **DeepVerifier (#51)**, **SWE-PRM (#3)**, and **AgentPRM (#1)** form the agent-verifier triad — domain-specific verifiers beat general ones.
- **Asymmetric Verification (#52)** + **Discriminative Verification (#18)** + **ThinkPRM (#4)** define the verifier-cost design space.
- **Inverse Scaling (#27)** + **"Increasing Thinking Budget" (#26)** + **CMU MAS-vs-SAS (#29)** are the canonical "more compute is not always better" trio.
- **T² scaling (#35)** + **Kinetics (#36)** are the post-Snell scaling-law canon for 2026.
- **Recursive Tournament Voting (#49)** is the specific "scaling agent coding" technique referenced in CMU TTC work.

### Gaps & Open Questions

1. **No clean scaling law for agent TTC.** Snell et al. (#37), T² (#35), Kinetics (#36) all target single-turn reasoning. The agent equivalent — how to allocate budget across turn count, samples-per-turn, and tree depth — does not yet have a clean closed-form law. General AgentBench (#47) provides empirical ceilings but no formula.

2. **PRM scarcity for novel domains.** ToolPRMBench (#2), AgentPRM (#1), PRA (#7), SWE-PRM (#3) all train domain-specific PRMs. There's no plug-and-play universal PRM for agents — every new domain re-pays the verifier-training cost.

3. **Speculative reasoning at the action level is immature.** Speculative Actions (#44) is lossless but limited to deterministic side-effect-free tools. Lossy speculative reasoning (where the speculation can affect state) is largely unexplored.

4. **CFE / counterfactual frame ensembling has thin academic backing.** Dipper (#32) is the closest published work; explicit study of structurally counterfactual frames (not just paraphrases) is missing. Strong opportunity for the skill itself to produce reference results.

5. **Adaptive compute for safety vs. capability is conflated.** Deliberative Alignment (#28) uses TTC for safety; AVA (#40) uses TTC for capability. No unified framework spending budget across both dimensions.

6. **Multi-turn verification is sequential-hypothesis-test-shaped but underdeveloped.** E-valuator (#6) is the only rigorous statistical treatment so far; SWE-PRM (#3) is heuristic. Big opportunity for rigorous online testing under e-process / always-valid CI guarantees.

7. **Orchestrator-vs-engine reasoning conflict (#54) lacks empirical guidance.** No paper measures when the planning-in-orchestrator vs. planning-in-model trade-off flips. Most production systems default to "both plan," paying the conflict cost.

8. **Open ceiling: long-horizon agent TTC.** All current techniques (trajectory compression #49, budget tracker #25, confidence retry #50, Ares #24) buy 30-60% cost reduction or +5-10pp accuracy. Nobody has the 10x improvement that single-turn TTC got from o1. The agent-TTC plateau is the biggest open problem.
