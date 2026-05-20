# Benchmarks & Capability Landscape (Nov 2025 – May 2026)
## Researcher 7 — 2026-05-20

Note on methodology: Numbers below are drawn from public leaderboards (swebench.com, arcprize.org, metr.org/time-horizons, Steel.dev, Princeton HAL, llm-stats.com, BenchLM.ai snapshot dated May 20, 2026, Epoch AI, PricePerToken, Scale Labs). Where leaderboards conflict, multiple values are reported. Vendor-marketing-only numbers are flagged "self-reported."

---

### Coding Agents (SWE-Bench Verified, Pro, Multilingual)

| Benchmark | SOTA (May 2026) | Score | Model + Harness | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| SWE-Bench Verified | Claude Mythos Preview | 93.9% | Anthropic internal harness | May 2026 | Claude Sonnet 4.5 ~77.2% (single-attempt avg); ~82.0% with high compute | +11.9 to +16.7 pp |
| SWE-Bench Verified #2 | Claude Opus 4.7 (Adaptive) | 87.6% | Anthropic Adaptive | Apr 2026 | — | — |
| SWE-Bench Verified #3 | GPT-5.3 Codex | 85.0% | OpenAI Codex harness | Mar 2026 | — | — |
| SWE-Bench Multilingual | Claude Mythos Preview | 87.3% | Anthropic harness | May 2026 | ~52% Claude Sonnet 4.5 region (est.) | ≈ +35 pp |
| SWE-Bench Multilingual #2 | Claude Opus 4.6 | 77.8% | Anthropic | Apr 2026 | — | — |
| SWE-Bench Multilingual #3 | Kimi K2.6 | 76.7% | Moonshot agent | Apr 2026 | — | — |
| SWE-Bench Pro (public) | Claude Mythos Preview | 77.8% | Anthropic | May 19, 2026 | not yet on board (Pro launched late 2025) | — |
| SWE-Bench Pro #2 | Claude Opus 4.7 (Adaptive) | 64.3% | Anthropic Adaptive | Apr 2026 | — | — |
| SWE-Bench Pro #3 | GPT-5.5 | 58.6% / GPT-5.4 (xHigh) 59.1% on Scale SEAL | OpenAI | Apr–May 2026 | — | — |
| SWE-Bench Pro (Scale SEAL standardized) | Claude Opus 4.5 | 45.9% | mini-swe-agent (Scale standardized) | Q1 2026 | Claude Opus 4.5 ~45.9% | flat |

Key observation: Vendor-reported SWE-Bench Pro numbers (e.g., Anthropic 77.8% / 64.3%) diverge substantially from Scale's standardized SEAL board (~45.9% top). The Verified vs Pro gap (~94 vs ~46-78%) is widely cited as evidence of contamination on Verified's Python-only set.

Saturation note: SWE-Bench Verified is effectively saturated for differentiation; top-5 cluster within 8 pp. The "real" frontier benchmark has migrated to SWE-Bench Pro (1,865 tasks, multi-language) and SWE-rebench / SWE-bench-Live (continuously refreshed).

**Skill-Impact (Coding Agents):** Coding-heavy research questions can rely on patch-quality evals; deep-research's skill should adopt a "code-grounded answer" mode that runs found code in a sandbox (Verifier role) before citing, since 19.78% of "solved" SWE-Bench entries are reportedly semantically incorrect — surface-level scoring is unreliable.

---

### Reasoning (HLE, GPQA, AIME, FrontierMath, MMLU-Pro)

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| HLE (Humanity's Last Exam) | Claude Mythos Preview | 64.7% | Anthropic | May 2026 | Gemini 3 Deep Think 41.0% (no tools); Grok 4 Heavy 44.4% (with tools) | +20–24 pp |
| HLE #2 | GPT-5.4 Pro | 58.7% | OpenAI | Q2 2026 | — | — |
| HLE #3 | GPT-5.5 Pro | 57.2% | OpenAI | May 2026 | — | — |
| HLE alt-board (PricePerToken) | Gemini 3.1 Pro Preview | 44.7% | Google | May 1, 2026 | — | — |
| GPQA Diamond | Gemini 3.1 Pro Preview | 94.1–94.3% | Google | May 16, 2026 | Gemini 3 Deep Think ~91% (est.); GPT-5.1 ~90% | +3–4 pp |
| GPQA Diamond #2 | Claude Mythos Preview | 94.6% (alt) / GPT-5.4 92.0% | Anthropic / OpenAI | May 2026 | — | — |
| AIME 2025 | GPT-5 | 100% (perfect) | OpenAI | Q1 2026 | GPT-5 ~94.6% | +5.4 pp |
| AIME 2026 | Qwen3.5-plus | 91.3% | Alibaba | Q2 2026 | n/a (just released) | — |
| AIME 2026 #2 | Gemma 4 (31B dense, no tools) | 89.2% | Google | Q1 2026 | — | — |
| FrontierMath | GPT-5.5 Pro | 52.4% | OpenAI | Apr 24, 2026 | Gemini 3 Deep Think ~40% | +12 pp |
| FrontierMath #2 | GPT-5.5 | 51.7% | OpenAI | Apr 2026 | — | — |
| FrontierMath #3 | GPT-5.4 Pro | 50.0% | OpenAI | Q1 2026 | — | — |
| MMLU-Pro | (saturating, no clear SOTA tracker by May 2026 — relegated to component-weight in composite indices) | — | — | — | — | — |

Saturation status: GPQA Diamond is saturated (top cluster 92-94%, PhD experts score 65%). AIME 2025 has a perfect-100% entry. FrontierMath top-4 are within 2.4 pp — nearing saturation but still useful. HLE remains the leading "reasoning at the frontier" benchmark.

**Skill-Impact (Reasoning):** Reasoning benchmarks are now solved by single-shot frontier models — deep-research doesn't add much value here. The skill should not invoke multi-agent search for pure reasoning queries; instead, route to a single-pass "Reasoner" with reasoning-mode budget rather than parallel researchers.

---

### Research / Browse / Open-Web (GAIA, BrowseComp, DeepResearch Bench, TAU-Bench)

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| GAIA (BenchLM single-model) | Claude Mythos Preview | 52.3% | Anthropic | May 2026 | OpenAI Deep Research 67.36% (validation set; system w/ tools) | depends on board |
| GAIA (Steel.dev system-level) | OPS-Agentic-Search | 92.36% | multi-model agent stack | Q2 2026 | OpenAI Deep Research ~67% | +25 pp |
| GAIA #2 (BenchLM) | GPT-5.4 Pro | 50.5% | OpenAI | Q2 2026 | — | — |
| BrowseComp | GPT-5.5 Pro | 90.1% | OpenAI | May 1, 2026 | OpenAI Deep Research 51.5%; Kimi K2 Thinking 60.2% | +30–38 pp |
| BrowseComp #2 | GPT-5.4 Pro | 89.3% | OpenAI | Q2 2026 | — | — |
| BrowseComp #3 | Claude Mythos Preview | 86.9% | Anthropic | May 2026 | — | — |
| TAU-Bench (Sierra) | Claude Mythos Preview | 89.2% | Anthropic | Apr 30, 2026 | Claude Sonnet 4.5 ~86.2% (retail) / 70% (airline) | +3-19 pp |
| TAU-Bench #2 | Claude Sonnet 4.6 | 87.5% | Anthropic | Q1 2026 | — | — |
| TAU-Bench #3 | Claude Sonnet 4.5 | 86.2% | Anthropic | Nov 2025 | (was SOTA Nov 2025 on retail) | — |
| DeepResearch Bench | GPT-5.5 (under GPT-5.5 evaluator) | top score; legacy Gemini-2.5-Pro evaluator deprecated June 17, 2026 | OpenAI | May 2026 | n/a (benchmark new) | — |

Note: GAIA leaderboards differ wildly because Princeton HAL / Steel.dev allow multi-model ensemble "systems" while BenchLM tracks single-model scores. Cite which.

**Skill-Impact (Research/Browse):** BrowseComp jumped 30+ pp because top systems exercise *persistence* and *multi-hop navigation*, not just keyword search. Deep-research skill should adopt: (a) a "page-rank-traversal" search policy that follows citation chains 2-3 hops, (b) a "verify-before-cite" loop that re-fetches and quotes, and (c) a system-level evaluation (not single-model) since SOTA is system-mode.

---

### Computer-Use (OSWorld, WindowsAgentArena)

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| OSWorld (llm-stats independent verified) | Claude Opus 4.6 | 72.7% | Anthropic computer-use | May 2026 | Claude Sonnet 4.5 ~61% / GPT-5.1 ~55% (range) | +12–17 pp |
| OSWorld #2 | Claude Sonnet 4.6 | 72.5% | Anthropic computer-use | Q1 2026 | — | — |
| OSWorld #3 | Qwen3 VL 235B A22B | 66.7% | Alibaba | Q2 2026 | — | — |
| OSWorld (self-reported) | GPT-5.4 | 75.0% | OpenAI (claim: beats 72.4% human baseline) | Mar 2026 | — | first model to claim human-baseline crossover |
| OSWorld (Coasty board) | Coasty | 82% | proprietary agent | Q2 2026 | — | — |
| WindowsAgentArena | UI-TARS-2 | 50.6% | ByteDance UI agent | Q1 2026 | Navi 19.5% (Microsoft baseline); human ~74.5% | +31 pp |
| AndroidWorld | UI-TARS-2 | 73.3% | ByteDance | Q1 2026 | — | — |

Gap to human: OSWorld nominal human baseline = 72.4%. Claude Opus 4.6 (72.7%) and GPT-5.4 self-reported (75.0%) sit at/above this — but in narrow verified subsets. WindowsAgentArena remains well below human (~50% vs 74.5%).

**Skill-Impact (Computer-Use):** Computer-use SOTA is now mostly determined by the agent-loop (screen-grounding + action prediction), not the LLM. The skill itself doesn't need GUI control unless extended with a browser-agent role.

---

### Time-Horizon (METR HCAST + RE-Bench)

| Benchmark | SOTA (May 2026) | 50% Horizon | 80% Horizon | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|---|
| METR Time Horizons (TH 1.1) | Claude Mythos Preview (early) | ≥16 hrs (CI 8.5–55 hrs) | not reliably measured | Anthropic | May 8, 2026 | Claude Sonnet 4.5 ~1.5–2 hrs (est.); Opus 4.5 came later at ~4h49m | ≈ +8x growth |
| METR Time Horizons #2 | Claude Opus 4.5 | 4 hrs 49 min (CI 1h49m–20h25m) | 27 min | Anthropic | late Nov 2025 | — | first to break 4-hour barrier |
| METR Time Horizons #3 | Claude Opus 4.6 | ~5–6 hrs (cluster) | — | Anthropic | Q1 2026 | — | — |
| METR Time Horizons (frontier cluster) | top GPT-5.x / Claude Opus | ~12 hrs at frontier; doubling time ~4 months | — | — | May 2026 | ~2 hrs frontier (Nov 2025) | ~6x in 6 months |

Key methodology change: Jan 29, 2026 — METR released **TH 1.1**: task suite expanded from 170 to 228 tasks (73 added from HCAST, 15 removed, 53 updated), doubled the number of 8+ hour tasks (14 → 31), moved infrastructure from Vivaria to **Inspect** (UK AISI open-source eval framework). Upper-bound CIs tightened (Opus 4.5 upper-bound shrank from 4.4x to 2.3x of point estimate).

Limitation: METR notes Mythos Preview's 16-hour result is "at the upper end of what we can measure" — only 5/228 tasks are 16+ hours. Doubling-time hypothesis ("10x/year" per LessWrong analysis) appears to be holding.

**Skill-Impact (Time-Horizon):** Suggests deep-research can comfortably run multi-hour multi-agent investigations — frontier models maintain coherence over 12+ hour task durations. But task lengths in deep-research are typically <30min, so this is more relevant for downstream applications than the skill itself.

---

### ML Engineering (MLE-Bench, WeirdML, RE-Bench)

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| MLE-Bench | Neo (autonomous ML engineer) | 34.2% (median bronze-medal-or-higher across competitions) | Neo agent | late 2025 | OpenAI o1-preview + AIDE scaffold ~16.9%; Microsoft RD-agent 22.4% | +12–17 pp |
| MLE-Bench Lite | MiniMax M2.7 | 66.6% (single entry) | MiniMax | May 2026 | n/a | — |
| WeirdML v2 | (Epoch maintains rolling; top is general capability proxy) | — | — | ongoing | — | — |
| RE-Bench | (included in METR Time Horizons) | — | — | — | — | — |

MLE-Bench note: leaderboard paused as of Apr 24, 2026 pending fairer submission process (per OpenAI repo). Neo's 34.2% is current public top.

WeirdML v2: enforces TITAN V GPU + 12GB + 600s timeout; 5 iterations/task with feedback; mean across 15 runs/model. Groups with FrontierMath in Epoch capability analyses (i.e., loads on a general "non-memorization" capability factor).

**Skill-Impact (ML-Engineering):** Not directly relevant to a research skill, but suggests that "agent-loop with iterative code execution + feedback" is the dominant architecture for ML eng — could inform a "code-grounded synthesis" mode.

---

### ARC-AGI-2 and ARC-AGI-3

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| ARC-AGI-2 (BenchLM) | GPT-5.5 | 85.0% | OpenAI | May 13, 2026 | Gemini 3 Pro 31.11%; Gemini 3 Deep Think (Preview) 45.14% | +40–54 pp |
| ARC-AGI-2 #2 | GPT-5.4 Pro | 83.3% | OpenAI | Q2 2026 | — | — |
| ARC-AGI-2 #3 | Gemini 3.1 Pro | 77.1% | Google | May 2026 | — | — |
| ARC-AGI-3 (interactive) | All frontier models | <1% (0.51% best) | — | Mar 25, 2026 launch | n/a (launched 2026) | — |
| ARC-AGI-3 (human baseline) | Humans | 100% | — | Mar 2026 | — | — |

Big news: **ARC-AGI-2 effectively saturated by GPT-5.5 (85%)**; ARC-AGI-3 launched March 25, 2026 with humans at 100% and frontier AI at **0.51%** — the new "embarrassingly hard" benchmark. ARC-AGI-3 is the first **interactive** benchmark in the series (hundreds of turn-based environments, no NL instructions — agents must perceive, choose actions, adapt). $2M prize pool; final submission Nov 2, 2026.

Gap to human: ARC-AGI-3 = roughly 99.5 percentage points — the largest known human-AI gap in any popular benchmark.

**Skill-Impact (ARC):** ARC-AGI-3 measures *exploration / planning / continuous learning* inside unfamiliar environments. Deep-research's structure (decompose → parallel search → synthesize) doesn't directly help here, but the "continuous learning" finding suggests session memory and feedback loops are a research direction.

---

### Cybersecurity (Cybench, BountyBench, CyberGym)

| Benchmark | SOTA (May 2026) | Score | System | Date | Nov 2025 SOTA | Δ |
|---|---|---|---|---|---|---|
| Cybench (llm-stats) | Claude Mythos Preview | 100.0% | Anthropic | May 2026 | (Cybench used by US/UK AISI on Sonnet 3.5 and o1; mid-range scores) | saturating |
| Cybench #2 | Grok-4.1 Thinking | 39.0% | xAI | Q1 2026 | — | — |
| CAIBench (cybersecurity meta-benchmark) | newly released | — | — | 2025 | — | — |
| BountyBench | newly active (real-world vuln find/exploit/patch with $ impact) | — | — | 2025–26 | — | — |
| CyberGym | active (UC Berkeley, real-world capabilities) | — | — | 2025 | — | — |

Cybench is essentially saturated for top models (Mythos at 100%). Frontier evaluation has shifted to BountyBench (real exploits with dollar-impact scoring) and CyberGym.

**Skill-Impact (Cybersecurity):** Not directly applicable to a research skill, but the "real-world impact scoring" methodology (BountyBench's $-impact) is a methodology pattern worth borrowing for any task with verifiable real-world outcomes.

---

### Discovery-Oriented Evals

| Benchmark | What it measures | Status May 2026 |
|---|---|---|
| PaperBench (OpenAI) | Replicate 20 ICML 2024 Spotlight/Oral papers from scratch; 8,316 individually gradable tasks | Active |
| ScienceAgentBench (OSU) | Data-driven scientific discovery; 102 tasks from 44 peer-reviewed papers across 4 disciplines, ICLR'25 | Active |
| AutoResearchBench (2026) | Complex scientific literature discovery over 3M+ arXiv papers; agents must reason about exploration/verification/stopping | New 2026 |
| ResearchBench | Scientific discovery sub-tasks: inspiration retrieval, hypothesis composition, hypothesis ranking across 12 disciplines | Active |
| AI Idea Bench 2025 | LLM-generated AI research idea quality vs original papers; 3,495 AI papers w/ inspired works | Active |
| DeepResearch Bench | 100 PhD-level tasks across 22 fields; RACE + FACT metrics for report quality and citation accuracy | Active |
| DiscoveryWorld / ScienceWorld | End-to-end scientific capabilities in simplified virtual worlds | Active |
| FIRE-Bench (2026) | Rediscovery of scientific insights | New 2026 |
| Vending-Bench 2 | Long-term coherence — 1-year vending machine simulation (60-100M tokens/run); Gemini 3 Pro ($5,478) and Claude Opus 4.5 ($4,967) starting from $500 | Replaces Vending-Bench 1 |

Discovery-oriented evals are the **fastest-growing category** in 2025-26. The consensus is that task-completion benchmarks are saturating, so the field is moving toward (a) novel-output evaluation (PaperBench, AI Idea Bench), (b) long-coherence evaluation (Vending-Bench 2, OdysseyBench), and (c) interactive/exploratory environments (ARC-AGI-3, DiscoveryWorld).

**Skill-Impact (Discovery):** ResearchBench's task decomposition (inspiration retrieval → hypothesis composition → hypothesis ranking) is directly applicable to deep-research's pipeline. Adding a "hypothesis composition" stage between retrieval and synthesis would map cleanly onto this benchmark.

---

### Methodology Breakthroughs in Evaluation (Nov 2025 – May 2026)

1. **Contamination-resistant benchmark families** — LiveCodeBench (continuously harvested), FrontierMath (research-level, expert-generated), MMLU-Pro, LiveBench, SWE-bench-Live, SWE-rebench (rolling refresh). Five known contamination-detection techniques: time-based partition (Codeforces cliff), Min-K% probability, Time Travel guided-completion attack, ConStat (performance gaps on rephrased samples), BIG-Bench canary GUID memorization.

2. **Agent-as-Judge / Multi-agent eval frameworks** — Survey paper Jan 2026 (arXiv 2601.05111). Multi-agent collaboration shows ~15.55% improvement over raw single-LLM judgments and ~8.37% over single-agent baseline. Rubric-based evaluation (Adnan Masood, Apr 2026) decomposes "good answer" into operational traits.

3. **Eval-as-CI-pipeline** — Evaluations now run on every PR; "every prompt change includes quality metrics in PR description, nothing ships without passing." Pre-production evals auto-convert into production guardrails.

4. **METR Time Horizons 1.1** (Jan 29, 2026) — task expansion (170→228), 8h+ task coverage doubled, Inspect framework (UK AISI), tighter CIs at longer horizons. Replaces fragile point estimates with logistic-curve duration estimates.

5. **Standardized agent harness scorings (Scale SEAL)** — Side-by-side standardized scaffold for SWE-Bench Pro that strips out vendor-specific harness variance. Shows ~30 pp difference vs vendor self-reported.

6. **SWE-ABS (Adversarial Benchmark Strengthening)** — exposes that 19.78% of top-30 leaderboard "solved" cases on SWE-Bench are semantically incorrect. Pattern of "passes tests for the wrong reason" formalized.

**Skill-Impact (Methodology):** Multi-agent judge frameworks are now standard for complex eval — the deep-research skill should pair its synthesis agent with a *judge agent* that scores synthesis on rubric dimensions (citation accuracy, persistence, hallucination rate) before final delivery.

---

### Saturation Status (what's basically solved Nov 2025 → May 2026)

| Benchmark | Status May 2026 | Why |
|---|---|---|
| **MMLU / MMLU-Pro** | Saturated | Top frontier 90%+, role demoted to "component weight in composite indices" |
| **GPQA Diamond** | Saturated | Top cluster 92–94%, PhD experts at 65% |
| **AIME 2025** | Saturated | GPT-5 perfect 100%; AIME 2026 next target |
| **SWE-Bench Verified** | Saturated (top-5 cluster within 8 pp; contamination suspected) | Migrated to SWE-Bench Pro & SWE-rebench |
| **ARC-AGI-2** | Effectively saturated (GPT-5.5 at 85%) | Replaced by ARC-AGI-3 |
| **Cybench** | Saturated (Claude Mythos 100%) | Replaced by BountyBench / CyberGym |
| **TAU-Bench (retail)** | Near-saturated | Top-3 within 3 pp |
| **FrontierMath** | Approaching saturation | Top-4 within 2.4 pp |
| **GAIA (single-model)** | Approaching plateau (~50–52% cluster) | Moved to system-level scoring on HAL/Steel boards |

**Open / unsaturated:**
- **ARC-AGI-3**: <1% best (humans 100%) — the new "AI failure" benchmark
- **HLE**: Top 64.7%, humans implicitly 100% — still ~35 pp gap
- **SWE-Bench Pro** (Scale SEAL standardized): top ~46%, lots of headroom
- **METR Time Horizons** beyond 16h: METR explicitly notes task suite can't reliably measure
- **Vending-Bench 2** / Long-coherence: highly variable; "meltdown loops" common
- **MLE-Bench**: top 34.2%, far below human Kaggle gold
- **WindowsAgentArena**: ~50% vs ~75% human
- **OSWorld**: at or near human (72.7% vs 72.4%) but verified-only narrow

---

### Reasoning Benchmarks Summary (single-row recap)

| Benchmark | May 2026 SOTA | Score | Nov 2025 SOTA | Status |
|---|---|---|---|---|
| GPQA Diamond | Gemini 3.1 Pro Preview / Claude Mythos | 94.1–94.6% | ~90–91% | Saturated |
| AIME 2025 | GPT-5 | 100% | ~94.6% | Saturated |
| AIME 2026 | Qwen3.5-plus | 91.3% | n/a | Active |
| MMLU-Pro | (composite-only) | — | — | Saturated |
| HLE | Claude Mythos Preview | 64.7% | ~41% (Gemini 3 DT no-tools) | Active, ~35 pp gap to ceiling |
| FrontierMath | GPT-5.5 Pro | 52.4% | ~40% (Gemini 3 DT) | Approaching saturation |

---

### Long-Horizon / Multi-Step Task Evals (newer 2026 entries)

- **LongCLI-Bench** — long-horizon agentic programming in CLI; failure analysis + human-agent collab insights
- **DeepPlanning** — multi-day travel planning, multi-product shopping; proactive info acquisition + global constraint optimization
- **HORIZON** — diagnostic with systematically increasing step requirements; structured horizon-failure analysis (arXiv 2604.11978)
- **OdysseyBench** — long-horizon complex office app workflows
- **Vending-Bench 2** — 1-year sim; Gemini 3 Pro and Claude Opus 4.5 are top with ~$5K profit from $500 start
- **METR HCAST / TH 1.1** — 228 tasks, primary long-horizon SWE evaluation infrastructure

Industry consensus per multiple sources: **"2026 is the year long-horizon agents go mainstream."**

---

### Cross-References

- For coding-agent **architecture / harnesses** (SWE-agent, OpenHands, Aider, Codex/Claude Code), see Researcher covering harnesses.
- For **MCP, A2A, agent protocols**, see protocols researcher.
- For **multi-agent orchestration / parallel execution**, see orchestrator researcher (relates to GAIA system-level entries).
- For **HRM/TRM hierarchical reasoning**, see HRM researcher (relates to ARC-AGI-3 capability gap).
- For **scientific discovery agents**, see discovery researcher (PaperBench, ScienceAgentBench, AutoResearchBench, ResearchBench).
- For **memory and checkpointing**, see memory researcher (relates to long-coherence Vending-Bench 2).
- For **verifiers and process-reward models**, see verifier researcher (relates to Agent-as-Judge methodology).

---

### Gaps & Open Questions

1. **Vendor-reported vs standardized scores**: SWE-Bench Pro shows ~30 pp gap between Anthropic-reported (77.8%) and Scale-standardized (45.9%). No consensus on which is the "real" number.
2. **METR Mythos 16h+ horizon**: Only 5/228 tasks reach this duration — METR explicitly says "measurements above 16 hrs are unreliable." We don't know real frontier capability above 16h.
3. **GAIA single-model vs system-level**: 52% vs 92% spread — no consensus on which to cite. Reflects whether agentic tooling counts as "the system."
4. **ARC-AGI-3 method gap**: Frontier <1% suggests current architectures lack *something* fundamental (in-context exploration / planning / continuous learning). Methodology unclear.
5. **Contamination quantification on Verified**: SWE-ABS suggests 19.78% of "solved" cases are semantically incorrect. True frontier coding skill is probably ~10-15 pp below reported scores.
6. **Discovery evals at scale**: PaperBench, AutoResearchBench, ResearchBench all exist but no centralized leaderboard or cross-comparison.
7. **Long-horizon benchmark saturation pace**: METR's 7-month doubling vs LessWrong's "10x/year" claim — unclear which is correct beyond mid-2026.

---

### Overall Skill-Impact Summary

The deep-research skill should:
1. **Adopt rubric-based + agent-as-judge evaluation** of its own synthesis output (15.55% quality lift documented).
2. **Add citation-grounding loop** (verify-before-cite re-fetch) to reduce hallucination, modeled on BrowseComp top-system practices.
3. **Add page-rank-traversal / 2-3 hop citation chains** beyond keyword search, since BrowseComp jumped from 51.5% to 90.1% on this capability.
4. **Add hypothesis-composition stage** between retrieval and synthesis (per ResearchBench pipeline).
5. **Run code-grounded sandbox verification** for any code/claim citations (SWE-Bench shows 19.78% of "solved" patches are semantically wrong).
6. **Treat individual model SOTA vs system-level SOTA as distinct dimensions** — GAIA spread (52% vs 92%) shows agentic system design now dominates raw model capability for research tasks.
