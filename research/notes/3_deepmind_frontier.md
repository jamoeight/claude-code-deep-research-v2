# DeepMind Frontier Work (Nov 2025 – May 2026)
## Researcher 3 — 2026-05-20

This note covers Google DeepMind's frontier work over the Nov 2025 → May 2026 window with a deliberate bias toward **agents that DO science** (AlphaEvolve, Co-Scientist, Aletheia, ERA, C2S-Scale) and multi-agent harness research. Each finding lists Detail + Source + Confidence + Skill-Impact + Notes.

Skill-Impact legend:
- **DIRECT** = architecture/technique we should copy or reference in our skill
- **INDIRECT** = useful framing, benchmark target, or capability claim
- **NONE** = context only

---

### Models & Capabilities (Gemini, Gemma)

**Gemini 3 Pro — released Nov 18, 2025**
- Detail: Frontier reasoning + agentic model. LMArena 1501 Elo. Benchmarks: **GPQA Diamond 91.9%**, **HLE 37.5%** (no tools), **SWE-Bench Verified 76.2%**, **MathArena Apex 23.4%** (SOTA), **MMMU-Pro 81%**, **Video-MMMU 87.6%**, **Terminal-Bench 2.0 54.2%**, **WebDev Arena 1487 Elo**, **SimpleQA Verified 72.1%**. 1M token context window. Native multimodal (text/image/video/audio/PDF) with output cap 65,536 tokens. Day-one rollout to Search, Gemini app, AI Studio, Vertex AI, Gemini CLI, and the **Antigravity** developer IDE (an agentic IDE that's DeepMind's analog to Claude Code / Cursor).
- Source: https://blog.google/products/gemini/gemini-3/ ; https://venturebeat.com/ai/google-unveils-gemini-3-claiming-the-lead-in-math-science-multimodal-and ; https://www.vellum.ai/blog/google-gemini-3-benchmarks
- Confidence: HIGH
- Skill-Impact: INDIRECT — sets benchmark targets and shows how Google ties a model to an agentic IDE (Antigravity) at launch.
- Notes: Lateral move signal — Google leads with Vending-Bench 2 (long-horizon planning) where Gemini 3 Pro has $5,478 net worth over simulated year, 272% above GPT-5.1. That's the bench to watch for *agentic harness* work.

**Gemini 3 Deep Think mode**
- Detail: Heavy-compute reasoning mode. **HLE 41.0%** (no tools), **GPQA Diamond 93.8%**, **ARC-AGI-2 45.1%** with code execution. Uses "parallel thinking" — simultaneously explores multiple solution paths before committing. Rolled out to AI Ultra subscribers in weeks after Nov 18.
- Source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-deep-think/ ; https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/
- Confidence: HIGH
- Skill-Impact: DIRECT — "parallel thinking" is the same idea as our CFE skill (multiple counterfactual frames in parallel). Validates the approach.
- Notes: Deep Think is the kernel of the **Aletheia** mathematics agent (see Discovery section). The pattern is: powerful base model + parallel sampling + natural-language verifier + iterative refinement.

**Gemini 3 Flash — Dec 17, 2025**
- Detail: Faster/cheaper Gemini 3 with same reasoning recipe. Aimed at high-volume agent workloads.
- Source: https://www.axios.com/2025/12/17/google-gemini-3-flash-pro-model
- Confidence: HIGH
- Skill-Impact: INDIRECT — relevant if we want to wire DeepMind models into a researcher subagent.

**Gemini 3.1 Pro — Feb 19, 2026**
- Detail: Mid-cycle refresh. **SWE-Bench Verified 80.6%**, **GPQA Diamond 94.3%**, **HLE 44.4%** (text + multimodal, no tools), **Terminal-Bench 2.0 68.5%**, **ARC-AGI-2 77.1%**, **APEX-Agents 33.5%**, **MCP Atlas 69.2%** (tool coordination), **BrowseComp 85.9%** (autonomous web research). Google reports leading on 13 of 16 benchmarks evaluated.
- Source: https://smartchunks.com/gemini-3-1-pro-benchmarks-gpqa-hle-lmsys-frontiermath/ ; https://almcorp.com/blog/gemini-3-1-pro-complete-guide/ ; https://gemini3.us/gemini-3.1-pro
- Confidence: HIGH
- Skill-Impact: INDIRECT — current best Google model. SWE-Bench statistically tied with Claude Opus 4.6 (80.8%).
- Notes: BrowseComp 85.9% is the highest benchmark *directly relevant* to a deep-research skill — that's the web-research equivalent.

**Gemini 2.5 Pro (pre-window baseline) — May 20, 2025**
- Detail: 1M+ token context, native multimodal, video up to 3hrs, SWE-Bench Verified 63.8% (custom agent), MRCR 91.5% @128k, VideoMME 84.8%. Tech report on arXiv: https://arxiv.org/html/2507.06261v1
- Source: https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/
- Confidence: HIGH
- Skill-Impact: NONE — pre-window context only.

**Gemma 3 (open-weight) — March 12, 2025**
- Detail: 1B/4B/12B/27B sizes. **128K context**, multimodal (text + image), 140+ languages. Gemma 3 27B-IT comparable to Gemini-1.5-Pro on benchmarks per the tech report.
- Source: https://arxiv.org/pdf/2503.19786 ; https://deepmind.google/models/gemma/gemma-3/
- Confidence: HIGH
- Skill-Impact: INDIRECT — viable open-weight backbone for researcher subagents.

**Gemma 3 270M — Aug 2025 + FunctionGemma — Jan 2026**
- Detail: 270M parameter ultra-edge model. 125MB RAM at INT4. Designed for task-specific fine-tuning. **FunctionGemma** variant (Jan 2026) is fine-tuned for natural-language → structured function/API calls — directly aimed at *enabling AI agents to act, not just talk*.
- Source: https://developers.googleblog.com/en/introducing-gemma-3-270m/ ; https://www.infoq.com/news/2026/01/functiongemma-edge-function-call/
- Confidence: HIGH
- Skill-Impact: INDIRECT — FunctionGemma is a viable cheap "tool router" model.

**Gemini Robotics 1.5 / Robotics-ER 1.5 — Sept 26, 2025**
- Detail: VLA model + embodied reasoning model that "thinks before acting." ER 1.5 plans with web search and digital tools, then hands off motor commands. Available via Gemini API for ER 1.5.
- Source: https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/ ; https://arxiv.org/abs/2510.03342
- Confidence: HIGH
- Skill-Impact: NONE — embodied; off-topic for a research skill.

**Gemini Diffusion (research preview) — May 20, 2025**
- Detail: Diffusion-based, non-autoregressive text generation at 1479 tokens/sec (5x Flash-Lite). Trades quality (BBEH 15.0% vs 21.0%; Global MMLU 69.1% vs 79.0%) for speed.
- Source: https://blog.google/technology/google-deepmind/gemini-diffusion/
- Confidence: HIGH
- Skill-Impact: NONE — interesting tech, not skill-relevant.

---

### Scientific Discovery Agents — THE CORE SECTION FOR OUR SKILL

**AlphaEvolve — paper May 14, 2025; impact blog May 7, 2026**
- Architecture: Evolutionary coding agent. **Gemini Flash (breadth) + Gemini Pro (depth)** generate code proposals. An **automated evaluator** scores each proposal on user-defined metrics. An **evolutionary loop** keeps high-scoring variants in a database and mutates them. No RL fine-tuning needed — works as a *prompted ensemble over a frozen LLM*.
- Methodology: Given (a) a code skeleton with `# EVOLVE-BLOCK-START/END` markers and (b) an `evaluate()` function, AlphaEvolve mutates only the marked block. The LLM ensemble proposes diffs; the evaluator (which can be expensive, e.g., a 24h ML training run) returns scalar scores; the database keeps a Pareto-frontier of variants.
- VERIFIED DISCOVERIES (this is what matters for our skill):
  - **Matrix multiplication breakthrough**: 4×4 complex-valued matrices in **48 scalar multiplications** vs Strassen's 49 (1969). First improvement in 56 years. AlphaTensor (2022) only beat Strassen over binary arithmetic; this is over complex numbers.
  - **Kissing number in 11 dimensions**: improved lower bound from 592 to **593** (300-year-old problem class).
  - **Erdős minimum overlap problem**: improved construction.
  - **Mathematical sweep**: Applied to 50+ open problems in analysis/geometry/combinatorics/number theory. **Re-discovered SOTA in ~75%**, **beat SOTA in ~20%**.
  - **Google infrastructure** (continuously deployed): Borg scheduler heuristic that recovers **0.7% of Google's global compute** (1 year deployment). **23% speedup** of Gemini's matrix-mul kernel → 1% Gemini training time reduction. **Up to 32.5% speedup** of FlashAttention kernel. Verilog rewrite for TPU arithmetic logic. Cache replacement policy designed in 2 days vs months. Spanner write-amplification reduced 20%. Compiler optimization → 9% storage footprint reduction.
  - **Genomics (PacBio collab)**: DeepConsensus DNA sequencing accuracy improved → 30% reduction in variant detection errors.
  - **Grid optimization (AC Optimal Power Flow)**: feasible solutions increased from 14% → 88%.
  - **Earth sciences**: natural disaster risk prediction accuracy +5% across 20 categories (wildfires, floods, tornadoes).
  - **Quantum**: Suggested circuits with 10× lower error than baselines, enabling complex molecular sims on Google's Willow processor.
  - **Commercial 2026**: Klarna 2× transformer training speed; Substrate multi-fold speedup in computational lithography; FM Logistic 10.4% routing efficiency; Schrödinger 4× speedup in ML force fields.
- Source: https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ ; https://deepmind.google/blog/alphaevolve-impact/ ; https://arxiv.org/abs/2506.13131 ; https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf
- Confidence: HIGH
- Skill-Impact: **DIRECT — this is the prototype for any discovery skill we build.**
- Notes: The key recipe is *(LLM ensemble proposer) + (cheap automated evaluator) + (Pareto database) + (evolutionary loop)*. Our skill's "stretch goal" of agents-that-do-science should essentially be a less-engineered version of this. The crucial constraint: AlphaEvolve only works on problems with a programmable evaluator — that's the discovery-eligibility filter.

**Aletheia — Mathematics Discovery Agent (Gemini Deep Think) — Dec 2–9, 2025 sweep**
- Architecture: Specialized mathematics agent built on Gemini Deep Think. **Three-component multi-agent loop**: (1) **Generator** produces candidate solutions, (2) **Verifier** does natural-language critique to identify flaws, (3) **Reviser** refines based on feedback. Has access to Google Search + web browsing (prevents fabricated citations). Critically: the agent can recognize when problems exceed its capabilities and bail out.
- Methodology: From Dec 2–9, 2025, Aletheia was deployed against the **700 open Erdős problems** in Bloom's database. Of 700 prompts: **212 candidate responses** → filtered by NL verifier → **27 promising solutions** → human-mathematician evaluation. The verification stack is human-AI hybrid; LLMs propose, humans confirm.
- VERIFIED DISCOVERIES (13 problems total):
  - **Autonomous solutions (4)**: Erdős-652 (affirmative via literature reduction); **Erdős-1051** (irrationality of series with exponential growth condition — believed to be the first AI-autonomous resolution of a non-trivial open Erdős problem of broader mathematical interest); Erdős-654 (negative answer + counterexample); Erdős-1040 (μ(F) not determined by transfinite diameter).
  - **Independent rediscoveries (4)**: Erdős-397, -659, -935, -1089.
  - **Literature identification (5)**: Erdős-333, -591, -705, -992, -1105 — Aletheia found existing solutions in literature humans had overlooked.
- Additional Deep Think wins:
  - Settled a **decade-old conjecture in online submodular optimization** via counterexample.
  - Solved Max-Cut network optimization by porting continuous-mathematics theorems to discrete setting.
  - Novel solutions to **cosmic string gravitational radiation** using Gegenbauer polynomials.
  - **One autonomous paper** on arithmetic geometry eigenweights (no human intervention).
- Source: https://arxiv.org/html/2601.22401v3 ; https://deepmind.google/blog/accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think/ ; https://the-decoder.com/deepminds-research-ai-occasionally-solves-what-humans-cant-and-mostly-gets-everything-else-wrong/ ; https://mathstodon.xyz/@tao/115591487350860999 (Terence Tao's wiki)
- Confidence: HIGH
- Skill-Impact: **DIRECT — Aletheia's Generator/Verifier/Reviser triplet is exactly the multi-agent loop our skill should ape for math/science discovery.** Note especially the explicit "I-can't-do-this" reject branch.
- Notes: 6.5% accuracy across 700 problems is humbling — most LLM "solutions" are wrong. The verification stack matters more than the generator. Terence Tao endorsed transparency through figures and built a community wiki to track AI-assisted progress. **This is the closest analog in the wild to what our discovery-engine skill is trying to do.**

**AI Co-Scientist — Nature paper May 19, 2026 (preprint Feb 2025)**
- Architecture: **Multi-agent system on Gemini.** Six specialized agents + supervisor:
  1. **Generation agent** — proposes initial research focus + novel hypotheses grounded in literature.
  2. **Proximity agent** — clusters hypotheses for diversity.
  3. **Reflection agent** — critically evaluates correctness, quality, novelty.
  4. **Ranking agent** — orchestrates pairwise comparisons via "scientific debates" (Elo-style tournament).
  5. **Evolution agent** — iteratively refines and combines top-ranked hypotheses.
  6. **Meta-review agent** — synthesizes debate insights, generates final research proposals.
  7. **Supervisor agent** — adaptive planner, decomposes research goals, coordinates parallel ops.
- Test-time compute scaling: agents continuously generate, critique, refine. Quality improves with compute.
- Independent CBRN safety classifiers screen unethical research goals.
- VERIFIED SCIENTIFIC DISCOVERIES:
  - **Liver fibrosis (Gary Peltz, Stanford)**: identified drug-repurposing candidate that **blocks 91% of scarring-linked fibrosis response** in lab tests.
  - **Antimicrobial resistance (José Penadés, Imperial College Fleming Initiative)**: Co-Scientist proposed **same hypothesis Penadés's team had reached over a decade** of lab work — generated in *days*.
  - **Acute Myeloid Leukemia (AML)**: novel drug-repurposing candidates; experimental validation confirmed drugs inhibit tumor viability at clinically relevant concentrations across multiple AML cell lines.
  - **Cellular rejuvenation (Omar Abudayyeh's lab)**: dataset analysis compressed from months → days; lab-validated genetic leads.
  - **Calico Life Sciences**: hypothesis about integrated stress response, experimentally confirmed.
  - **Plant immunity, ALS, cellular aging, aging biology** — additional research-focus areas.
- Validated across **100+ research institutions**. Enterprise customers include Daiichi Sankyo (pharma) and Bayer Crop Science.
- Source: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/ ; https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/ ; https://www.nature.com/articles/s41586-026-10644-y
- Confidence: HIGH
- Skill-Impact: **DIRECT — this is the canonical multi-agent science architecture. The 6-agent + supervisor pattern, the Elo-tournament ranking, and the iterative Generate→Debate→Evolve cycle are all directly applicable to our skill.**
- Notes: The "scientific debate" Elo tournament is a critical idea — instead of asking one agent "is this good?", you make N agents *argue* about which of M hypotheses is best, then aggregate. This is the same idea as multi-agent debate papers (see below).

**ERA — Empirical Research Assistance — Nature paper May 19, 2026**
- Architecture: Gemini-backed coding agent for empirical research code. Combines LLM with a **search strategy that explores and refines thousands of code pieces** in parallel — analogous to AlphaEvolve but for general scientific software, not just algorithmic optimization.
- VERIFIED: **Outperformed the U.S. CDC's official COVID-19 hospitalization forecasting ensemble** in a head-to-head evaluation. Other domains: solar forecasting, epidemiology.
- Source: https://www.techtimes.com/articles/316901/20260520/gemini-science-launches-peer-reviewed-benchmarks-era-beat-cdc-forecasting-model.htm ; https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026/ ; https://seas.harvard.edu/news/ai-system-automates-coding-scientific-research
- Confidence: HIGH
- Skill-Impact: DIRECT — ERA is a "search-over-code" pattern that we should consider for any phase where our skill needs to explore code/algorithm/model space.

**Gemini for Science — Google I/O May 19, 2026**
- Detail: Umbrella product bundling **three tools**:
  1. **Hypothesis Generation** — powered by Co-Scientist (multi-agent idea tournament).
  2. **Computational Discovery** — powered by AlphaEvolve + ERA (search over code variants).
  3. **Literature Insights** — powered by NotebookLM (structures lit, generates reports/presentations).
- "Science Skills" data layer integrates **30+ life science databases** (UniProt, AlphaFold Database, AlphaGenome API, InterPro) directly inside the Antigravity agentic IDE. Available through Google Labs (with enterprise path via Google Cloud).
- Source: https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026/
- Confidence: HIGH
- Skill-Impact: **DIRECT** — this is Google's first-party answer to "what does a discovery skill look like." The three-pillar split (Hypothesize / Compute / Literature) is a clean architecture our skill could mirror.

**C2S-Scale 27B — Oct 17, 2025 (Google + DeepMind + Yale)**
- Architecture: 27B-param foundation model built on **Gemma-2 27B** decoder. Trained on 57M+ human/mouse cells from 800+ datasets (CellxGene, Human Cell Atlas). Represents scRNA-seq profiles as **"cell sentences"** — ranked lists of gene symbols an LLM can directly reason about.
- VERIFIED DISCOVERY: **Novel cancer immunotherapy mechanism — confirmed experimentally**. Hypothesis: **combine CK2 inhibition (silmitasertib / CX-4945) with low-dose interferon** → significantly increases tumor antigen presentation, turning "cold" immune-evading tumors into immunotherapy targets. First AI model to generate a *new* testable cancer therapy hypothesis (not just analyze existing data) that experimental validation confirmed.
- Source: https://www.marktechpost.com/2025/10/17/google-ai-releases-c2s-scale-27b-model-that-translate-complex-single-cell-gene-expression-data-into-cell-sentences-that-llms-can-understand/ ; https://www.biorxiv.org/content/10.1101/2025.04.14.648850v2 ; https://huggingface.co/vandijklab/C2S-Scale-Gemma-2-27B
- Confidence: HIGH
- Skill-Impact: INDIRECT — illustrates domain-specific tokenization (cells → sentences) as a route to LLM-driven discovery in biology.

**AlphaProof — Nature paper Nov 12, 2025**
- Architecture: RL agent that proves theorems in **Lean**. Pairs a pre-trained LM with **AlphaZero-style RL**. Curriculum of millions of **auto-formalized** problems. **Test-Time RL (TTRL)** generates variants of the target theorem and uses successful variant proofs as policy improvement signal.
- VERIFIED: **IMO 2024 silver medal** with AlphaGeometry 2 — solved 4/6 problems including problem 6 (the hardest, solved by only 5/609 humans). Saturates **MiniF2F** benchmark, scores **56% on PutnamBench**. Guarantees 100% correctness via Lean verification.
- Source: https://www.nature.com/articles/s41586-025-09833-y ; https://deepmind.google/blog/ai-solves-imo-problems-at-silver-medal-level/ ; https://www.julian.ac/blog/2025/11/13/alphaproof-paper/
- Confidence: HIGH
- Skill-Impact: DIRECT — TTRL (generate variants of target problem, use successes as signal) is a powerful pattern for discovery where ground-truth verification is cheap.
- Notes: Now superseded for *natural-language* math by Gemini Deep Think + Aletheia, but AlphaProof remains the best system for **formal-verifier-guaranteed** outputs. Use AlphaProof's TTRL idea if our skill ever has a verifier.

**Gemini Deep Think IMO 2025 Gold — July 21, 2025**
- Detail: Solved **5/6 IMO 2025 problems, 35/42 points** (gold-medal threshold, top ~67/630 humans). End-to-end natural language (no manual Lean translation). 4.5-hour standard contest time. RL-trained for multi-step reasoning + theorem proving, plus access to curated past-IMO solutions. **First general-purpose, natural-language AI to officially reach gold.** Last year's silver required Lean translation and 2–3 days compute; this year was natural-language and competition-time.
- Source: https://deepmind.google/blog/advanced-version-of-gemini-with-deep-think-officially-achieves-gold-medal-standard-at-the-international-mathematical-olympiad/ ; https://simonwillison.net/2025/Jul/21/gemini-imo/
- Confidence: HIGH
- Skill-Impact: INDIRECT — proves natural-language verifier loops can scale to elite math. Bench target.

**Gemini 2.5 Deep Think ICPC 2025 Gold — Sept 4, 2025**
- Detail: At ICPC World Finals (Baku), Gemini 2.5 Deep Think solved **10/12 problems in 677 minutes** — gold-medal level, would have placed **2nd overall** among university teams. **Solved Problem C — a complex optimization task no human team solved.**
- Source: https://deepmind.google/blog/gemini-achieves-gold-medal-level-at-the-international-collegiate-programming-contest-world-finals/ ; https://github.com/google-deepmind/gemini_icpc2025
- Confidence: HIGH
- Skill-Impact: INDIRECT — establishes that the same Deep Think pattern transfers from math to competitive programming.

**AlphaGeometry 2 — Feb 5, 2025 (Nature)** 
- Detail: Extended representation language for object motion and linear angle/ratio/distance equations. Coverage of IMO 2000–2024 geometry from prior 65% → **88%**. (No AlphaGeometry 3 announcement found through May 2026 — Gemini Deep Think appears to be the de facto successor.)
- Source: https://en.wikipedia.org/wiki/AlphaGeometry
- Confidence: HIGH
- Skill-Impact: NONE.

**GNoME materials discovery (status update)**
- Detail: Original GNoME (Nov 2023) predicted 2.4M stable materials; dataset since expanded to **520K+ materials within 1 meV/atom of the convex hull** (as of Aug 2024). External labs have **independently synthesized 736** of GNoME's predicted structures. A-Lab (autonomous synthesis) realized **41 of 58 novel-compound targets in 17 days** of continuous operation. Includes 52,000 new graphene-like layered compounds with potential superconducting applications (vs ~1,000 known prior).
- Source: https://deepmind.google/blog/millions-of-new-materials-discovered-with-deep-learning/ ; https://github.com/google-deepmind/materials_discovery
- Confidence: HIGH
- Skill-Impact: NONE — domain-specific GNN, not LLM-agent.

**AlphaFold 3 — public availability Feb 2025 + applications 2025–26**
- Detail: AF3 (released May 8, 2024) predicts structure of protein + DNA/RNA + post-translational modifications + ligands/ions. **50% accuracy improvement** on protein interactions; **up to 200%** in some categories. Architecture: **Pairformer + diffusion** refining a cloud-of-atoms into 3D structure. Source code + weights open for non-commercial use Feb 2025. **9,000+ citations by Nov 2025.**
- Source: https://blog.google/innovation-and-ai/products/google-deepmind-isomorphic-alphafold-3-ai-model/
- Confidence: HIGH
- Skill-Impact: NONE — direct prediction model.

**AlphaMissense — ongoing**
- Detail: Adapted AlphaFold for missense variant pathogenicity. **89% of variants classified at 90% precision** on known-disease DB; classifies **89% of all 71M possible missense variants** as pathogenic/benign. Ongoing validation in clinical genomics 2025–26 (e.g., inherited retinal diseases).
- Source: https://deepmind.google/research/publications/21083/
- Confidence: HIGH
- Skill-Impact: NONE.

**AlphaQubit — quantum error correction**
- Detail: 30% error reduction vs traditional decoders. **Scaling factor 2.14×** — logical error rate drops exponentially as code distance increases (3→5→7). Integrated into custom ASIC controllers in 2025, removing latency-bottleneck concerns. Marks end of NISQ era.
- Source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphaqubit-quantum-error-correction/ ; https://www.nature.com/articles/s41586-024-08148-8
- Confidence: HIGH
- Skill-Impact: NONE.

---

### Reasoning / RL / Search Papers

**AlphaProof TTRL pattern** — see above. Generate variants of target problem, train policy on successful variant proofs at test time. Direct DIRECT-impact for our skill.

**Gemini 2.5 tech report (arXiv July 2025)** — https://arxiv.org/html/2507.06261v1 . Long-form details on RL for reasoning, multimodality, long context, agentic capabilities.

**Multi-agent debate (external, but pattern is DeepMind-influenced)**
- "Efficient LLM Safety Evaluation through Multi-Agent Debate" (Nov 2025) — https://arxiv.org/pdf/2511.06396
- "Debating Truth: Debate-driven Claim Verification" — https://arxiv.org/pdf/2507.19090
- Pattern: Two Debaters argue opposing stances, a Judge agent decides; surfaces subtle errors that single-agent assessments miss. **This is the kernel idea inside Co-Scientist's "scientific debate" Elo tournament.**
- Skill-Impact: DIRECT — useful for our verification stack.

**Co-Scientist Ranking agent's "scientific debate" mechanism** — the Elo-tournament pairwise comparison among hypotheses is the cleanest published recipe for "use multi-agent debate inside a discovery agent." See Co-Scientist source above.

---

### Agentic Products (Astra, Mariner, Antigravity, Deep Research)

**Project Mariner** — browser agent. Powered by Gemini 2.0 originally; **WebVoyager 83.5%** single-agent, **90.5% with tree-search**. Cloud-based execution (10 parallel task streams). "Teach & Repeat" feature added at I/O 2025. **In 2026 DeepMind absorbed Project Mariner organizationally** to consolidate the agent stack.
- Source: https://markets.financialcontent.com/wral/article/tokenring-2026-1-2-the-agentic-era-arrives-googles-project-mariner-and-gemini-20-redefine-the-browser-experience ; https://www.reactionarytimes.com/googles-strategic-pivot-deepmind-absorbs-project-mariner-to-win-the-ai-agent-war/
- Confidence: HIGH
- Skill-Impact: INDIRECT — competing approach to browsing/research.

**Project Astra** — universal multimodal assistant; full integration into Gemini app targeted across 2026. Proactive, multimodal, cross-device.
- Source: https://markets.financialcontent.com/wral/article/tokenring-2025-12-25-the-rise-of-the-universal-agent-how-googles-project-astra-is-redefining-the-human-ai-interface
- Skill-Impact: NONE — consumer assistant.

**Google Antigravity (Nov 18, 2025)** — Agentic IDE launched alongside Gemini 3 Pro. Direct competitor to Cursor + Claude Code. Surfaces AlphaEvolve / Co-Scientist / Science Skills inside the IDE.
- Source: https://blog.google/products/gemini/gemini-3/
- Skill-Impact: INDIRECT — example of "agentic IDE as harness" architecture.

**Deep Research + Deep Research Max — April 22, 2026**
- Detail: Built on Gemini 3.1 Pro. Supports **MCP**, native visualizations, long-horizon research workflows over web or custom private sources. "Deep Research Max" is the heavy-compute tier. Launched first via Interactions API in Dec 2025, then GA in April 2026.
- Source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/ ; https://venturebeat.com/technology/googles-new-deep-research-and-deep-research-max-agents-can-search-the-web-and-your-private-data ; https://siliconangle.com/2026/04/22/google-launches-ai-research-agents-powered-gemini-3-1-pro/
- Confidence: HIGH
- Skill-Impact: **DIRECT — Google's first-party "deep research agent" product.** This is our direct competitor on the deep-research side of the skill. **MCP support** is a notable adoption signal.

---

### World Models / Embodied Agents

**Genie 3 — research preview Aug 2025; public via Project Genie Jan 29, 2026**
- Detail: First real-time interactive general-purpose world model. Generates navigable 3D worlds from text prompts at **24 fps, 720p, ~minutes of consistency**. Public via Project Genie for AI Ultra subscribers ($250/mo) in US only.
- Source: https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
- Confidence: HIGH
- Skill-Impact: NONE.
- Notes: Feb 2026 — Waymo built a specialized "Waymo World Model" on Genie 3 for AV simulation.

**SIMA 2 — Nov 13, 2025; tech report Dec 2025 (arXiv 2512.04797)**
- Detail: Generalist embodied agent on Gemini foundation. Acts in 3D virtual worlds. **Doubled SIMA 1's performance.** Zero-shot generalization to unseen games and Genie-3-generated photorealistic worlds. **Can autonomously learn new skills in a new environment by leveraging Gemini to generate tasks and provide rewards** (self-curriculum).
- Source: https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/ ; https://arxiv.org/abs/2512.04797 ; https://techcrunch.com/2025/11/13/googles-sima-2-agent-uses-gemini-to-reason-and-act-in-virtual-worlds/
- Confidence: HIGH
- Skill-Impact: INDIRECT — the "LLM generates tasks + rewards for self-curriculum" trick is a powerful pattern.
- Notes: SIMA 2 ↔ Genie 3 deployment is interesting: Genie 3 simulates environment changes, SIMA 2 acts inside them, both LLM-driven → autonomous open-ended training loop.

**WeatherNext 2 — Nov 17, 2025**
- Detail: Functional Generative Network. **8× faster** than predecessor (GenCast) at probabilistic forecasts. Beats GenCast on **99.9% of variables/lead-times**. Powers Google Search, Maps, Pixel Weather, Maps Weather API. Integrated into U.S. National Hurricane Center workflow for 2025 hurricane season.
- Source: https://deepmind.google/discover/blog/weathernext-2/ ; https://www.marktechpost.com/2025/11/17/google-deepminds-weathernext-2-uses-functional-generative-networks-for-8x-faster-probabilistic-weather-forecasts/
- Confidence: HIGH
- Skill-Impact: NONE.

---

### Cross-References

- **The "Discovery Stack" emerging from DeepMind looks like this**:
  - **Generator**: Gemini Deep Think (or AlphaEvolve's Flash+Pro ensemble)
  - **Verifier**: NL-verifier agent (Aletheia) OR programmatic eval (AlphaEvolve) OR Lean (AlphaProof) OR experimental wet-lab validation (Co-Scientist) OR ground-truth comparison (ERA vs CDC)
  - **Refiner/Reviser**: explicit revise agent (Aletheia) or evolutionary loop (AlphaEvolve, FunSearch)
  - **Tournament/Ranker**: Co-Scientist's Elo "scientific debate"
  - **Diversity**: Co-Scientist's Proximity agent (clusters hypotheses) ; AlphaEvolve's Pareto-frontier database
  - **Meta-control**: supervisor agent (Co-Scientist) ; "I-can't-do-this" reject branch (Aletheia)
- **This stack maps almost 1:1 onto what we want our discovery-engine skill to do.** Our skill should explicitly mention these as the canonical examples (FunSearch → AlphaEvolve → Co-Scientist → Aletheia → ERA → Gemini for Science).
- **Multi-agent debate** is everywhere — Co-Scientist's tournament, the Anthropic-Claude debate papers, Aletheia's Verifier ↔ Reviser. Our skill should include this primitive.
- **Verifier diversity is the gating factor.** AlphaEvolve works when you have a programmable evaluator. AlphaProof works when Lean covers the domain. Co-Scientist needs wet-lab partners. **Aletheia is the only one where the verifier is itself an LLM-as-judge with human-in-loop confirmation** — that's the most general (and least reliable, at 6.5% accuracy) approach. Our skill needs to be honest about which verifier regime it's in.

---

### Gaps & Open Questions

1. **No GAIA, MLE-Bench, METR HCAST, or FrontierMath scores** for Gemini 3 surfaced in my searches. Either DeepMind hasn't published these or they're buried. Skills' competing-research narrative might note this absence.
2. **No "AlphaCode 3" or "AlphaGeometry 3"** — DeepMind has effectively rolled these into Gemini Deep Think. The narrative is consolidation: separate domain agents → general-purpose Deep Think + domain harnesses.
3. **Aletheia's exact prompt structure / architecture diagram** is not in my sources — I have the conceptual triplet (Generator/Verifier/Reviser) but not the prompt templates. Worth a follow-up read of arXiv 2601.22401.
4. **Co-Scientist's compute cost per discovery** is not published. The "drug-repurposing hit blocking 91% of fibrosis response" is a great result but we don't know the $/discovery.
5. **AlphaEvolve's evolutionary database structure** is described but specifics of mutation prompting / Pareto-frontier maintenance / sampling-temperature schedule are paper-only — worth a deep paper read.
6. **Open-weight versions of any of these discovery agents** do not appear to exist. Gemma 3 is open but Co-Scientist / AlphaEvolve / Aletheia are not. Builds on Gemini API only.
7. **No public benchmark for "multi-agent discovery"** — Co-Scientist's wet-lab validations and Aletheia's Erdős sweep are bespoke. The field lacks a standardized "discovery-bench."
8. **The relationship between Aletheia and AlphaEvolve** is not fully clear. AlphaEvolve is closer to FunSearch (code mutation); Aletheia is closer to Co-Scientist (NL reasoning + verifier). Both are deployed against math problems but with different methodologies. Worth confirming whether they share infrastructure.
9. **Project Mariner being absorbed into DeepMind in 2026** — strategic signal but specifics of org change are limited.
10. **Frontier Safety Framework details for agentic models** — DeepMind's 145-page AGI safety paper (Apr 2025) discusses framework but actual Gemini 3 / Aletheia / Co-Scientist safety classifier details are thin.
