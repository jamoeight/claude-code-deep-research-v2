# Data Summary — Deep-Research Skill Redesign
## Data Analyst output · 2026-05-20

This file aggregates quantitative findings extracted from the 8 researcher notes in `files/research_notes/`. Numbers are drawn from primary sources (Anthropic / OpenAI / DeepMind blogs and docs, arXiv papers, public leaderboards) cited in the underlying research notes. Vendor-self-reported values are flagged; standardized values (Scale SEAL, Steel.dev, METR Inspect, BenchLM) are preferred where they exist.

---

## 1. Benchmark Landscape (Nov 2025 → May 2026)

**Source data**: `files/data/benchmarks.csv`
**Visualizations**: `chart1_benchmark_deltas.png`, `chart5_saturation_status.png`

### Headline numbers (single-model SOTA)

| Benchmark | Nov 2025 | May 2026 | Δ (pp) | Status |
|---|---|---|---|---|
| SWE-Bench Verified | 77.2% (Sonnet 4.5) | **93.9% (Mythos Preview)** | +16.7 | Saturated; contamination suspected |
| SWE-Bench Multilingual | ~52% | **87.3%** | +35.3 | Active |
| SWE-Bench Pro (vendor) | — | **77.8%** | — | Open (Scale-SEAL standardized: ~46%) |
| HLE | 41.0% (Gemini 3 DT, no tools) | **64.7% (Mythos)** | +23.7 | Active; ~35 pp gap to ceiling |
| GPQA Diamond | ~91% | **94.3% (Gemini 3.1 Pro)** | +3.3 | Saturated |
| AIME 2025 | 94.6% (GPT-5) | **100% (GPT-5)** | +5.4 | Saturated |
| FrontierMath | 40% (Gemini 3 DT) | **52.4% (GPT-5.5 Pro)** | +12.4 | Near-saturation |
| GAIA single-model | 67.4% (OpenAI DR) | **52.3% (Mythos)** | -15.1 | BenchLM single-model plateau |
| GAIA system-level | ~67% | **92.4% (OPS-Agentic-Search)** | +25.4 | Active |
| BrowseComp | 51.5% (OpenAI DR) | **90.1% (GPT-5.5 Pro)** | **+38.6** | Largest single delta |
| TAU-Bench | 86.2% (Sonnet 4.5) | **89.2% (Mythos)** | +3.0 | Near-saturation |
| OSWorld | ~61% | **72.7% (Opus 4.6)** | +11.7 | At human (72.4) |
| WindowsAgentArena | 19.5% (Navi) | **50.6% (UI-TARS-2)** | +31.1 | Open (human 74.5) |
| ARC-AGI-2 | 31.1% (Gemini 3 Pro) | **85.0% (GPT-5.5)** | **+53.9** | Effectively solved |
| ARC-AGI-3 | n/a | **0.51%** | — | Embarrassingly hard (humans 100%) |
| Cybench | mid-range | **100% (Mythos)** | ~+50 | Saturated |
| MLE-Bench | 22.4% (RD-agent) | **34.2% (Neo)** | +11.8 | Open |
| Terminal-Bench 2.0 | 54.2% (Gemini 3) | **82.7% (GPT-5.5)** | +28.5 | Active |

### Saturation buckets (May 2026)

- **Saturated (6)**: MMLU-Pro, GPQA Diamond, AIME 2025, SWE-Bench Verified, ARC-AGI-2, Cybench.
- **Near-saturation (3)**: TAU-Bench retail, FrontierMath, GAIA single-model.
- **Open (9)**: HLE, SWE-Bench Pro (Scale SEAL), BrowseComp, METR ≥16h, Vending-Bench 2, MLE-Bench, WindowsAgentArena, OSWorld verified, AIME 2026.
- **Embarrassingly hard (1)**: ARC-AGI-3 (0.51% vs 100% human — the largest known human-AI gap).

### Key observations

1. **BrowseComp jumped 38.6 pp in 6 months** (51.5 → 90.1%) — the largest single-benchmark gain in this window. Top systems exercise multi-hop navigation and citation verification, not just keyword search. **Direct argument for the deep-research skill to add citation-chain traversal + verify-before-cite loops.**

2. **Vendor-vs-standardized gap on SWE-Bench Pro ≈ 30 pp** (Anthropic 77.8% vs Scale SEAL 45.9% top). When the skill cites coding-agent benchmarks, prefer Scale SEAL/standardized values.

3. **GAIA shows the system-vs-model gap clearly**: 52% single-model best vs 92% system-level (OPS-Agentic-Search). The skill should be evaluated as a *system*, not a model.

4. **AIME 2026 (91.3% Qwen3.5-plus) suggests benchmark refresh is the new defense** against saturation. Expect HLE-2, ARC-AGI-4, FrontierMath-2 in 2026 H2.

---

## 2. METR Time Horizons (50% horizon)

**Visualization**: `chart2_metr_time_horizons.png`

| Date | Model | 50% Horizon |
|---|---|---|
| Nov 2023 | GPT-4 | ~5 min |
| Apr 2024 | Claude 3 Opus | ~12 min |
| Sep 2024 | o1-preview | ~27 min |
| Apr 2025 | o3 | ~1.5 h |
| Nov 2025 | frontier | **~2 h** |
| Nov 24 2025 | Claude Opus 4.5 | **4 h 49 min** (CI 1h49m–20h25m) |
| Q1 2026 | Claude Opus 4.6 | ~5–6 h |
| Apr 2026 | frontier cluster | ~12 h |
| May 8 2026 | Claude Mythos Preview | **≥16 h** (CI 8.5–55 h) |

- **6× growth in 6 months** (Nov 2025 → May 2026).
- Doubling time ≈ 4 months.
- METR explicitly notes ≥16 h is at the upper limit of measurability (5/228 tasks).
- Methodology change: TH 1.1 (Jan 29 2026) — task suite 170→228, 8h+ task coverage doubled, moved to UK AISI Inspect framework.

---

## 3. Architectural / Harness Technique Lifts

**Source data**: `files/data/techniques.csv`
**Visualization**: `chart3_technique_lifts.png`

### Absolute lift (percentage points)

| Technique | Target | Lift | Source |
|---|---|---|---|
| Asymmetric Verification | BrowseComp (GLM-4.5) | **+27 pp** | arXiv:2510.06135 (R6-F52) |
| Best-of-N + voting | BrowseComp | +20 pp | OpenAI BrowseComp paper (R2) |
| Trajectory Compression | Terminal-Bench 2.0 | +12.2 pp | arXiv:2604.16529 (R6-F49) |
| SWE-PRM (midstream verify) | SWE-Bench Verified | +10.6 pp | arXiv:2509.02360 (R6-F3) |
| AggAgent (aggregation) | deep-research | **+10.3 pp** | arXiv:2604.11753 (R4-F34) |
| PROClaim (Progressive RAG) | Check-COVID | +10 pp | arXiv:2603.28488 (R4-F5) |
| DeepVerifier (rubric verify) | GAIA hard | +9.5 pp (mid of +8-11) | arXiv:2601.15808 (R4-F8) |
| Trajectory Compression | SWE-Bench Verified (Opus 4.5: 70.9 → 77.6) | +6.7 pp | arXiv:2604.16529 (R6-F49) |

### Relative lift (% improvement)

| Technique | Target | Lift | Source |
|---|---|---|---|
| Anthropic multi-agent vs single Opus | research tasks | **+90.2 %** | Anthropic blueprint (R1-MA1) |
| Tree-GRPO | agent tasks | **+69 %** | arXiv:2509.21240 (R6-F9) |
| Inverse Entropy SC | reasoning configs | +46.7 % | arXiv:2511.02309 (R6-F15) |
| PRA (verifier-as-agent) | knowledge-intensive | +25.7 % | arXiv:2604.09482 (R6-F7) |
| ACE (Agentic Context Eng) | agent tasks | +10.6 % | arXiv:2510.04618 (R5-F10) |

### Key takeaway

The **top three architecture moves** for a deep-research skill, ranked by published lift:
1. **Verifier role** (Asymmetric Verification +27 pp on BrowseComp; DeepVerifier +9.5 pp on GAIA hard).
2. **Aggregator role** (AggAgent +10.3 pp on deep-research; replaces flat synthesis).
3. **Multi-agent fan-out** (+90.2% over single Opus; Anthropic-validated).

---

## 4. Cost / Token Reduction Stack

**Visualization**: `chart4_cost_reductions.png`

These reductions are **independently composable** — stacking 3-4 of them is the realistic budget plan.

### Top context primitives (highest reduction first)

| Primitive | Reduction | Mechanism |
|---|---|---|
| Code Execution w/ MCP | **-98.7%** | 150K → 2K tokens; MCP as filesystem of TS interfaces |
| Dynamic toolsets (simple) | -96.7% | Speakeasy benchmark |
| ToolSearch (deferred tools) | **-85%** | `defer_loading: true`; on Opus 4.5 raised tool-pick accuracy 79.5→88.1% |
| Prompt caching (sliding 4 breakpoints) | -80% | 25-turn agentic investigation input cost |
| Opus 4.5 token-efficiency (medium) | -76% | vs Sonnet 4.5 output, matches its score |
| Token-efficient tool use (max) | -70% | Claude 4.x output |
| SAGE skill library | -59% | Output tokens, +8.9% SGC |
| DALA (VCG comms auction) | -55% | GSM8K tokens vs competitors |
| Ares per-step effort (TAU-Retail) | -52.7% | Reasoning cost; tiny router model |
| Three-tier model routing (industry) | ~-51% | Inferred from typical pricing differential |
| Compaction API (auto) | ~-50% | Long-run context (Anthropic) |
| Clear tool_uses | -48.4% | 335K → 173K context (Anthropic cookbook) |
| PASTE speculative tools | -48.5% | Task completion time |
| Opus 4.5 token-efficiency (high) | -48% | vs Sonnet 4.5 output, +4.3% accuracy |
| Ares (BrowseComp-Plus) | -41.8% | Tokens |
| BATS (Budget-Aware Tool-Use) | -40% | Tool calls |
| Programmatic Tool Calling | -37% | Task tokens |
| TrACE-4 (adaptive compute) | -33% | Calls at matched accuracy |
| BATS cost | -31% | Task cost |
| Token-efficient tool use (avg) | -14% | Claude 4.x output |

### Composability examples (from primary sources)

- **Code Execution + ToolSearch + Prompt Caching** is the canonical "context-engineering" stack — Anthropic cookbook documents these as orthogonal.
- **Clear tool_uses + Compaction**: stacked example in Anthropic cookbook took an agent's peak context 335K → 173K, then "ran indefinitely" once compaction kicked in at 150K.

---

## 5. Discovery Agent Verified Results

**Visualization**: `chart6_discovery_verifications.png`

| System | Verified discoveries | Notable |
|---|---|---|
| **AlphaEvolve** | 15 | 4×4 cplx matmul (48 mults — first improvement on Strassen in 56 yrs), kissing # in 11D (592 → 593), Erdős minimum overlap, Borg scheduler (+0.7% global compute), Gemini matmul kernel +23%, FlashAttention +32.5%, AC OPF feasibility 14% → 88%, DeepConsensus −30% variant errors, ML force fields 4× speedup (Schrödinger), Klarna 2× transformer training, compiler −9% storage, Spanner −20% write amp, earth-sci +5%, quantum circuits 10× lower error, plus more enterprise deployments. |
| **Aletheia** (Dec 2-9 2025 sweep) | 13 | 700 prompts → 27 promising → 13 verified: 4 autonomous (incl Erdős-1051 — likely first AI-autonomous non-trivial Erdős resolution), 4 independent rediscoveries, 5 literature identifications. Plus decade-old online submodular conjecture settled. |
| **AI Co-Scientist** | 6 | Liver fibrosis (91% scarring response blocked), AMR (Penadés decade in days), AML drug repurposing, cellular rejuvenation, Calico integrated stress response, plant immunity/ALS pipeline. Nature paper May 19 2026. |
| **Gemini Deep Think** | 2 | IMO 2025 gold (5/6, 35/42), ICPC 2025 World Finals gold (10/12 problems, P-C unsolved by humans). |
| **C2S-Scale 27B** | 1 | CK2 + low-dose interferon combo — confirmed novel cancer immunotherapy mechanism. First AI-generated *new* testable cancer therapy. |
| **ERA** | 1 | Beat U.S. CDC's official COVID hospitalization forecasting ensemble. |
| **AlphaProof** | 1 | IMO 2024 silver, 4/6 problems incl P6. |

**Total**: 6+ DeepMind systems with verified novel results — represents the "agents that DO science" frontier the deep-research skill should benchmark against (per researcher 3).

---

## 6. Other Quantitative Findings

### Model release / pricing snapshots
- **Claude Opus 4.5** (Nov 24 2025): $5 / $25 per M; SWE-Bench Verified 80.9%; 76% fewer output tokens vs Sonnet 4.5 at medium effort.
- **Claude Opus 4.6** (Feb 5 2026): SWE-Bench Verified 80.84%; SWE-Bench Multilingual 77.83% (25 trials, adaptive thinking).
- **Claude Sonnet 4.6** (Feb 17 2026): $3 / $15 per M; SWE-Bench Verified 79.2%; 1M context beta; Claude Code A/B: preferred 70% over 4.5, 59% over Opus 4.5.
- **Claude Opus 4.7** (Apr 16 2026): CursorBench 70% vs 4.6's 58%; XBOW Visual Acuity 98.5% vs 4.6's 54.5%; Rakuten-SWE-Bench 3× more production tasks resolved.
- **Claude Haiku 4.5** (Oct 15 2025): $1 / $5 per M; SWE-Bench Verified 73.3%; 4-5× faster than Sonnet 4.5; ~90% of Sonnet 4.5 agentic-coding performance.
- **GPT-5.2** (Dec 11 2025): FrontierMath T1-3 40.3%; ARC-AGI-2 52.9%; GDPval 70.9%; 38% error reduction vs 5.1.
- **GPT-5.3 Instant** (Mar 3 2026): ~$0.30 / $1.20 per M; -26.8% hallucinations vs 5.2.
- **GPT-5.5 / 5.5 Pro** (Apr 23-24 2026): Terminal-Bench 2.0 82.7%; GDPval 84.9%; OSWorld-Verified 78.7%; Tau2 Telecom 98.0%; FrontierMath T1-3 51.7%; SWE-Bench 88.7%; SWE-Bench Pro 58.6%; 1M context. **60% hallucination drop**.
- **Gemini 3 Pro** (Nov 18 2025): LMArena 1501; GPQA Diamond 91.9%; HLE 37.5%; SWE-Bench Verified 76.2%; Terminal-Bench 2.0 54.2%.
- **Gemini 3 Deep Think**: HLE 41.0%; GPQA Diamond 93.8%; ARC-AGI-2 45.1%.
- **Gemini 3.1 Pro** (Feb 19 2026): SWE-Bench Verified 80.6%; GPQA Diamond 94.3%; HLE 44.4%; ARC-AGI-2 77.1%; BrowseComp 85.9%.

### Multi-agent quality / cost numbers
- Multi-agent orchestration **+90.2% over single Opus** on research tasks (Anthropic); ~15× token cost.
- Multi-agent IR (incident response): **100% actionable-recommendation vs 1.7% single-agent**; zero quality variance.
- Reflexive orchestration F1 0.943 at 2.3× cost (SEC filings); **hybrid with caching + routing + adaptive retry recovers 89% of gain at 1.15× cost**.
- **CMU finding (May 2026)**: under fixed token budget with perfect context utilization, single-agent is information-efficient — multi-agent's win is often disguised TTC.

### Anthropic context-engineering reductions (composable)
- Code execution w/ MCP: **150K → 2K tokens** (Drive-to-Salesforce demo, **-98.7%**)
- Cloudflare 2,500-endpoint API: 1.17M → <1K (-99.9%)
- Tool Search Tool: **~85% token reduction** on multi-MCP setups; Opus 4 tool-pick accuracy 49 → 74%; Opus 4.5 79.5 → 88.1%.
- Programmatic Tool Calling: **-37% tokens** on complex tasks; eliminates 19+ inference passes.
- Tool Use Examples: tool-param-handling accuracy **72 → 90%**.
- Prompt caching: 90% off cached input (Anthropic standard pricing); 5-min write 1.25×, 1-hour write 2×.
- Constitutional Classifiers: **-89% successful prompt-injection rate** at ~2× compute cost.

### Agent TTC ceilings
- **General AgentBench**: agent perf peaks at **3-7 turns** on general tasks before context-ceiling degradation.
- **Inverse scaling**: DeepSeek R1 70% → 30% on counting w/ 5 distractors at long CoT.
- **Trajectory compression (Claude-4.5-Opus)**: 70.9 → 77.6% on SWE-Bench Verified (+6.7 pp).
- **Asymmetric Verification (GLM-4.5 Heavy)**: 54.0% BrowseComp, 66.0% GAIA, 68.0% xbench-DeepSearch; **up to +27 absolute points**.

---

## 7. Chart manifest

All charts at 150 DPI, Agg backend, tab10/YlOrRd palettes, in `files/charts/`.

| File | What it shows | Key insight |
|---|---|---|
| `chart1_benchmark_deltas.png` | Horizontal grouped bars: Nov 2025 vs May 2026 SOTA across 12 key benchmarks, each with Δ pp annotation | BrowseComp (+38.6 pp) and ARC-AGI-2 (+53.9 pp) are the biggest movers; AIME 2025 hit 100% |
| `chart2_metr_time_horizons.png` | Log-y line chart of 50% time horizon vs date, 2023→2026 | 6× growth in 6 months; frontier crossed 16h in May 2026; doubling time ≈ 4 months |
| `chart3_technique_lifts.png` | Horizontal bars of measurable lift per architectural / harness technique; blue=pp, orange=relative | Asymmetric Verification +27 pp on BrowseComp and AggAgent +10.3 pp on deep-research are the highest-leverage moves for our skill |
| `chart4_cost_reductions.png` | Horizontal heat-bar chart of 20 token / cost reduction primitives | Stacking 3-4 of these (Code-exec MCP + ToolSearch + Caching + Compaction) is the realistic budget plan |
| `chart5_saturation_status.png` | Stacked horizontal bars grouped by saturation status: saturated / near / open / embarrassingly hard | ARC-AGI-3 (0.51%) is the only embarrassingly-hard benchmark; most popular benchmarks are saturated |
| `chart6_discovery_verifications.png` | Vertical bar chart: verified discoveries per DeepMind agent system | AlphaEvolve (15) and Aletheia (13) lead; the discovery-stack pattern (Generator + Verifier + Reviser + Tournament) is the canonical recipe |

---

## 8. Caveats

- **Vendor-reported** numbers are flagged on Chart 1 and in the CSV; where standardized (Scale SEAL, BenchLM single-model, METR Inspect) values exist, both are reported.
- **METR ≥16h**: only 5/228 tasks reach this duration; the upper CI bound (55h) reflects measurement noise, not a confident frontier estimate.
- **SWE-Bench Verified contamination**: SWE-ABS analysis estimates 19.78% of "solved" top-30 leaderboard cases are semantically incorrect — true coding capability likely ~10-15 pp below reported.
- **Discovery counts** are not strictly comparable across systems (different verification regimes: programmatic eval for AlphaEvolve, NL+human for Aletheia, wet-lab for Co-Scientist, ground-truth for ERA). Treat the absolute counts as illustrative rank, not strict equivalence.
- **Relative vs absolute lifts** (Chart 3) are not directly comparable — a +69% relative gain on a low baseline can equal a small absolute gain. Both are shown labeled.
- Numbers that don't appear in the underlying research notes were not fabricated; where the orchestrator's brief listed examples that the researchers had not fact-checked, I used only the researcher-verified values.
