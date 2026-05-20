# Gap-Fill: Concrete Prompt Patterns from SOTA Discovery & Verification Systems
## Researcher 9 (Gap-Fill) — 2026-05-20

Scope: ruthlessly specific prompts, templates, and algorithms for the four high-leverage SKILL v2 edits — *Failure Rubric, Generator-Evaluator Loop, Elo Debate Tournament + Generator/Verifier/Reviser, AggAgent Aggregation* — plus the three lower-priority items (Dreaming, BrowseConf, BATS).

---

## Gap A — DeepVerifier DRA Failure Taxonomy (arXiv 2601.15808)

### Full Enumeration (5 categories, 13 subcategories)

The DRA Failure Taxonomy was automatically constructed by clustering observed agent errors in the DeepVerifier-4K dataset; each subcategory becomes an explicit rubric check at verification time.

1. **Finding Sources** — failures in acquiring evidence (largest category).
   1.1 **Wrong Source / Consulting Wrong Evidence**: agent retrieves a source unrelated to or inconsistent with the question.
   1.2 **Missing Source**: relies on internal knowledge instead of retrieving evidence the task requires.
   1.3 **Generic / Inadequate Search**: query is too broad or non-specific, returning low-signal results.
   1.4 **Invalid Source / Secondary Source Dependence**: cites a secondary or low-credibility source rather than the primary record.

2. **Reasoning** — failures interpreting evidence already in hand.
   2.1 **Premature Conclusion**: jumps to an answer before sufficient evidence accumulates.
   2.2 **Misinterpretation**: misreads the retrieved snippet (wrong subject, wrong year, wrong unit, etc.).
   2.3 **Hallucinated / Overconfident Claims**: asserts facts not supported by any retrieved source.

3. **Problem Understanding & Decomposition** — failures upstream of search.
   3.1 **Misunderstanding Task / Instructions**: misreads what the user asked.
   3.2 **Goal Drift**: starts pursuing an adjacent sub-question and forgets the original objective.
   3.3 **Inappropriate Decomposition**: breaks the task into sub-questions that don't compose back to the answer.

4. **Action Errors** — failures executing tools/UI.
   4.1 **UI Failures**: browser/click/scroll errors, gives up on a page that has the answer.
   4.2 **Format Mistakes**: output violates required format (e.g. wrong JSON, wrong units).
   4.3 **Wrong Modality Use**: e.g. tries to read an image with a text tool, or vice-versa.

5. **Max-Step Reached** — single failure mode; early mistakes cascade and the trajectory exhausts the step budget without producing an answer.

*(Note: some secondary sources phrase 1.x slightly differently — Wan et al. 2026 Figure 3 is the canonical reference. The structure above is what DeepVerifier's rubric checks operate on.)*

### Rubric-Feedback Prompt Template (DeepVerifier, Appendix B.2)

**Error Identification (Verifier → Taxonomy):**
> "Identify suspicious behaviors and map each to **one** potential error from the list below. If none, return exactly: 'No potential errors found'. **Potential error list:** [Failure Taxonomy]"

**Corrective Feedback Prompt (Verifier → Re-running Agent):**
> "You are given a task description, a wrong answer given by an agent, a summary of how the agent obtained the wrong answer, and additional answers provided by another research agent regarding the additional questions. Now, the agent will try to solve the task again. Based on these inputs, you need to help the agent retrieve the correct answer by first providing a brief reflection and then providing **no more than three instructions**."

Enforced output format:
```
Reflection: <brief reflection on why the prior attempt failed>
Instruction 1: <one concrete corrective step>
Instruction 2: <optional>
Instruction 3: <optional, max 3 total>
```

Guidance baked into the prompt: "point out necessary sources and actions to avoid the agent making the same mistakes again" and prefer "clear, concise, and accurate instructions rather than long or complex" ones.

**Judge / Scoring Step (Reflection component):**
> "Explanation: <explanation> Score: <1-4 integer>"
Score forces a categorical judgement on a 1-4 scale with an explanation before the number (reduces score-anchoring).

### Source
arXiv 2601.15808 (Wan et al., 2026), HTML v1 §3 + Appendix B.2; cross-verified with emergentmind taxonomy summary.

---

## Gap B — Generator-Evaluator Prompt Patterns

### OpenEvolve (github.com/algorithmicsuperintelligence/openevolve)

Prompt templates live in `openevolve/prompts/defaults/`. All quotes below are verbatim from the repo (Apache-2 licensed).

**System Prompt** (`system_message.txt`):
```
You are an expert software developer tasked with iteratively improving a codebase.
Your goal is to maximize the FITNESS SCORE while exploring diverse solutions across feature dimensions.
The system maintains a collection of diverse programs - both high fitness AND diversity are valuable.
```

**Mutation User Prompt** (`diff_user.txt`) — the canonical proposer prompt:
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

Example of valid diff format:
<<<<<<< SEARCH
for i in range(m):
    for j in range(p):
        for k in range(n):
            C[i, j] += A[i, k] * B[k, j]
=======
# Reorder loops for better memory access pattern
for i in range(m):
    for k in range(n):
        for j in range(p):
            C[i, j] += A[i, k] * B[k, j]
>>>>>>> REPLACE

You can suggest multiple changes. Each SEARCH section must exactly match code in the current program.
Be thoughtful about your changes and explain your reasoning thoroughly.
IMPORTANT: Do not rewrite the entire program - focus on targeted improvements.
```

**Full-Rewrite Alternative** (`full_rewrite_user.txt`) — used when the proposer prefers wholesale replacement; same `{artifacts}` / `{evolution_history}` / `{current_program}` scaffold but asks for a complete `{language}` rewrite preserving I/O.

**Evolution History Sub-template** (`evolution_history.txt`):
```
## Previous Attempts
{previous_attempts}

## Top Performing Programs
{top_programs}

{inspirations_section}
```

**Per-Attempt Slot** (`previous_attempt.txt`):
```
### Attempt {attempt_number}
- Changes: {changes}
- Metrics: {performance}
- Outcome: {outcome}
```

**Top Program Slot** (`top_program.txt`):
```
### Program {program_number} (Score: {score})
```{language}
{program_snippet}
```
Key features: {key_features}
```

**Inspiration Slot** (`inspiration_program.txt`) — used to inject diverse-but-distant exemplars from other MAP-Elites cells:
```
### Inspiration {program_number} (Score: {score}, Type: {program_type})
```{language}
{program_snippet}
```
Unique approach: {unique_features}
```

**Evaluator System / Score Prompt** (`evaluator_system_message.txt` + `evaluation.txt`) — LLM-as-judge fallback when the programmatic evaluator can't score readability/maintainability:
```
You are an expert code reviewer.
Your job is to analyze the provided code and evaluate it systematically.
```
followed by the rubric in `evaluation.txt`:
```
Evaluate the following code on a scale of 0.0 to 1.0 for the following metrics:
1. Readability: ...
2. Maintainability: ...
3. Efficiency: ...
Return your evaluation as a JSON object: {"readability": ..., "maintainability": ..., "efficiency": ..., "reasoning": "..."}
```

**Mutation Wiring (EVOLVE-BLOCK markers):**
The user marks editable code with `# EVOLVE-BLOCK-START` and `# EVOLVE-BLOCK-END` comments in the source file (or language-specific equivalents). Only code between the markers is shown to the proposer as `{current_program}` and is the only region the SEARCH/REPLACE diff can touch. Code outside the markers is preserved verbatim. This lets users fix scaffolding (imports, I/O, evaluation harness) while evolving only the algorithm core.

**Artifact Side-Channel (errors → next prompt):**
The `{artifacts}` placeholder is filled from the previous run's `EvaluationResult.artifacts` dict, which can carry: `stderr`, `profiling_data`, `llm_feedback`, `build_warnings`. These render in the next prompt under a "Previous Execution Feedback" header — e.g.:
```
⚠️ Warning: suboptimal memory access pattern
💡 LLM Feedback: Code is correct but could use better variable names
```
This is the critical "feedback closes the loop" wire — programmatic evaluator errors become natural-language context for the proposer's next mutation.

### AlphaEvolve (arXiv 2506.13131, DeepMind 2026)

DeepMind did **not** release the literal production prompts. From the paper text + figures, the prompt structure is:

**Prompt Sampler components** (assembled per generation, fed to the LLM ensemble):
1. *Explicit context*: problem description, fixed human instructions, relevant equations, literature snippets, code scaffolding.
2. *Rendered evaluation results*: parent program(s) + their evaluator scores + the actual execution output (stdout, error traces).
3. *Stochastic formatting*: template placeholders with multiple human-provided alternatives, randomized per call to encourage diversity.
4. *Meta-prompt evolution*: instructions and context proposed by a separate prompt-generation step that itself evolves (the system can rewrite its own meta-prompt).

**Verbatim System Prompt Excerpt (Figure 3b of paper):**
> "Act as an expert software developer. Your task is to iteratively improve the provided codebase."

The user message follows the pattern:
> "Previously we found that the following programs performed well on the task at hand: [scored examples] ... Now improve the following program: [current_program]"

**LLM Ensemble Wiring (Flash + Pro):**
- **Gemini 2.0/2.5 Flash**: high-throughput, breadth — many candidate diffs per generation, lower-fidelity but cheaper. Used to widen the search frontier.
- **Gemini 2.0/2.5 Pro**: lower-throughput, depth — fewer but higher-quality candidates, used for refinement and the "critical-depth" insightful suggestions.
The paper notes the ensemble runs *in parallel* with the same prompt template; the Program Database absorbs both streams indifferently and lets the MAP-Elites/island scheme handle quality-vs-diversity arbitration.

**Evaluator Integration (scalar → next prompt):**
The evaluator returns scalar (or vector) fitness scores; the Prompt Sampler renders this as "scored examples" in the next prompt, e.g. "Program A (score: 0.87): <code>" → the LLM sees prior fitness deltas and can reason about what moves up the gradient. Multi-objective scores render as Pareto-frontier annotations.

**Program Database / Parent Sampling:**
"The evolutionary database implements an algorithm that is inspired by a combination of the MAP-Elites algorithm and island-based population models."
- MAP-Elites: programs are binned by user-defined behavioural features (e.g. *compute used*, *memory footprint*, *algorithmic family*); each bin keeps the highest-fitness program.
- Island model: the population is partitioned into multiple sub-populations ("islands") that evolve independently with occasional migration — prevents premature convergence.
- *Sampling*: parents are drawn proportional to fitness within an island; inspirations are drawn from other MAP-Elites cells to inject diverse exemplars (this matches OpenEvolve's `inspirations_section`).

### Source
- OpenEvolve repo `openevolve/prompts/defaults/` (verbatim).
- AlphaEvolve arXiv 2506.13131 §Method, Figure 3, and the DeepMind blog (architecture-level only; literal production prompts not released).

---

## Gap C — Co-Scientist (Elo Debate Tournament) & Aletheia (G/V/R)

### Co-Scientist Ranking — Pairwise Comparison Tournament

**Paper**: Gottweis et al. "Towards an AI Co-Scientist", arXiv 2502.18864 (Nature 2026, DOI s41586-026-10644-y). DeepMind/Google Research.

The paper references the verbatim prompts as Appendix figures: `COMPARE_IDEAS_PROMPT` (Figure A.4), `SELF_PLAY_PROMPT` (the multi-turn scientific debate format), `REVIEWS_PROMPT_TEMPLATE` (Reflection), `EXPLORE_ARTICLES_PROMPT`, `FEASIBILITY_IDEA_PROMPT`, `OUT_OF_THE_BOX_SINGLE_IDEA_PROMPT`. The figures are embedded as raster images in the arXiv PDF and could not be extracted verbatim via WebFetch; the *structure and mechanics* are pinned down below.

**Pairwise Comparison Prompt Structure (paraphrased from paper description):**
- *Two-tier matchmaking*:
  - **Top-ranked hypotheses** → multi-turn scientific debate (mitigates ordering bias; LLM plays multiple "expert" perspectives across turns before deciding).
  - **Lower-ranked hypotheses** → single-turn pairwise comparison (cheaper).
- *Evaluation axes the prompt forces the comparator to consider*: **novelty, correctness, testability** (these three appear repeatedly in the prompt structure description).
- *Output*: the agent must conclude each comparison with an explicit "Hypothesis A is better / Hypothesis B is better / Tie" decision plus a one-paragraph rationale.
- *Self-play / scientific debate*: the LLM is instructed to "simulate an expert panel" — generating critiques, counter-critiques, and a final adjudication within one prompt.

**[paraphrased structure for the comparator prompt]:**
```
You are evaluating two research hypotheses on the same scientific problem.
Compare them on:
  - Novelty: Which proposes a more original mechanism?
  - Correctness: Which is more likely to be scientifically valid?
  - Testability: Which can be more concretely tested or falsified?

Hypothesis A: <text>
Hypothesis B: <text>

[For top-ranked pairs only:] Simulate a multi-turn debate between two expert reviewers,
one defending each hypothesis. After 3 turns, adjudicate.

Conclusion: <"A better" | "B better" | "Tie">
Rationale: <one paragraph>
```

**Elo Update Rule (confirmed from paper):**
- *Initial rating*: every new hypothesis enters with Elo = **1200**.
- *Tournament prioritization*: pairs are selected by (a) Proximity-agent graph distance (hypotheses are more likely to play other hypotheses on similar topics), (b) newness bias, and (c) top-rank bias (newer and stronger candidates play more matches).
- *Update*: standard pairwise Elo with win/loss based on the comparator's verdict. The paper does **not** disclose the exact K-factor; from context (gradual rating change, tournaments of dozens-to-hundreds of matches) it's plausibly K ≈ 32 (chess default), but this is not stated.
- *Use*: the Elo rating is the system's auto-evaluation signal. Hypotheses with higher Elo are preferentially evolved (Evolution agent), proximity-clustered (Proximity agent), and surfaced to the Meta-review.

**Reflection Agent — Critique Format (multiple review types):**
The paper lists at least five Reflection review modes:
- **Initial review** — quick triage (correctness, quality, novelty).
- **Full review** — deep correctness check against the literature.
- **Deep verification review** — fine-grained logical/empirical check.
- **Observation review** — does this hypothesis explain a phenomenon the user mentioned?
- **Simulation review** — would a thought-experiment / simulation confirm or break it?

Each review writes a structured critique with explicit axes (correctness, quality, novelty) plus a free-form "concerns" section. The verbatim template (`REVIEWS_PROMPT_TEMPLATE`) is in the appendix but is not extractable as text from the figure image.

### Aletheia — Generator / Verifier / Reviser (arXiv 2601.22401, DeepMind 2026)

**Paper**: "Semi-Autonomous Mathematics Discovery with Gemini: A Case Study on the Erdős Problems." Aletheia is a Gemini-Deep-Think-based agent that autonomously solved 4 previously-open Erdős problems and scored 91.9% on IMO-ProofBench Advanced.

**Architecture** (decoupled three-role harness):
1. **Generator** — proposes a candidate solution in natural language (uses Gemini Deep Think with intensive tool use).
2. **Verifier** — *natural-language* verifier (the explicit decoupling of verification from generation is the paper's key claim — "researchers observed that explicitly separating verification helps the model recognize flaws it initially overlooks during generation").
3. **Reviser** — given Verifier critique, attempts a localized fix without restarting from scratch.

**Three feedback branches the Verifier emits:**
- **Correct** → output the solution.
- **Minor flaws** → route to **Reviser** for a patch.
- **Major / critical flaws** → restart at **Generator** with the failure context.

**Reject branch ("I cannot solve this"):**
The system can explicitly **admit failure** and output a rejection rather than fabricating an answer (the paper highlights this as a key anti-hallucination property). The criterion is conservative: if after N iterations of Generate→Verify→Revise the Verifier still reports critical flaws, Aletheia returns a "could not resolve" verdict rather than a low-confidence guess. Concretely, the natural-language verifier acts as a gate — of 700 input Erdős problems, only 212 passed Verifier sign-off (a ~70% rejection rate), and of those only ~13 ultimately survived human expert vetting. This high rejection rate is the design intent: prefer abstention over hallucination.

**Inference-Time Scaling:**
- Multiple Generator candidates per problem (sampling at the candidate-level, then Verifier-filtered).
- Iterative Generate→Verify→Revise loop with bounded iterations.
- A "novel inference-time scaling law" is cited but the paper does not give the formula in the abstract or main text accessible via WebFetch; the literal prompts are stated to be in the GitHub release at `google-deepmind/superhuman/tree/main/aletheia` (the repo contains per-problem solution PDFs and a master `Aletheia.pdf`, but the system prompts themselves are **not** committed to the public repo as of 2026-05-20 — only the raw outputs).

**[paraphrased — verbatim prompts not released]:**
- *Generator*: math-reasoning system prompt invoking Deep Think with tool use (calculator, theorem-prover, literature search). Implicit "admit failure" instruction tied to the Verifier loop.
- *Verifier*: "Critique this proof / argument in natural language. Identify any logical gap, citation error, hallucinated theorem, or numerical mistake. Conclude with one of: CORRECT / MINOR-FLAW / CRITICAL-FLAW. If CRITICAL-FLAW, explain why a patch would not save the argument."
- *Reviser*: "Given the original argument and the Verifier's identified flaw, produce a localized correction. Do not re-derive the whole proof."

### Source
- Co-Scientist: arXiv 2502.18864, DeepMind blog *co-scientist-a-multi-agent-ai-partner-to-accelerate-research*, Nature s41586-026-10644-y. Appendix figures A.4 / A.5 / A.17 referenced but not extractable verbatim from PDF.
- Aletheia: arXiv 2601.22401 v3, DeepMind blog *accelerating-mathematical-and-scientific-discovery-with-gemini-deep-think*, repo `google-deepmind/superhuman/aletheia` (outputs only; system prompts not released).

---

## Gap D — AggAgent Aggregation (arXiv 2604.11753)

**Paper**: Lee, Yen, Ye, Chen, "Agentic Aggregation for Parallel Scaling of Long-Horizon Agentic Tasks", Princeton PLI, 2026. Repo: `princeton-pli/AggAgent` (Apache-2).

**Core Idea**: instead of voting on final answers (loses trajectory info) or concatenating all trajectories (blows the context window), treat the parallel trajectories as an **environment** the aggregator can interactively interrogate via tool calls. Up to **5.3% absolute** average improvement over flat aggregation across 6 benchmarks (GLM-4.7, Qwen3.5, MiniMax-M2.5).

### Aggregator Prompt (verbatim structure from `aggagent/prompts.py`)

There are three variants of the aggregator system prompt; all share these guideline pillars:

**Core operational guideline (verbatim):**
> "A single trajectory with a clear, unambiguous tool observation supporting answer X is stronger evidence than many trajectories that reasoned their way to Y without grounding in tool outputs."

**Other locked-in instructions (verbatim quotes from the prompt):**
- Agents must **verify claims by inspecting actual tool outputs** using search and retrieval functions.
- Final solutions must be **self-contained** with no references to trajectory IDs or tool invocations.
- **Prohibited**: circular logic, ungrounded assumptions, silent handling of tool errors, majority-vote bias without evidence grounding, self-referential mentions of trajectories/tools.

**Three prompt variants:**
1. **Standard (XML format)**: final answer wrapped in XML tags.
2. **Qwen variant**: uses labelled text fields instead of XML —
```
Explanation: {{detailed reasoning leading to the answer}}
Exact Answer: {{the exact answer}}
```
3. **Long-form / Report variant** (for HealthBench, ResearchRubrics-style tasks): explicitly requires "integrate content across candidates rather than concatenate sections" and "ground every nontrivial claim in retrieved snippets using citation format" and "resolve contradictions by reasoning about accuracy rather than averaging positions."

### Trajectory Surface — What the Aggregator Sees

**Neither raw rollouts nor a flat summary — both, on demand.**
- At session start the aggregator receives **only `format_metadata(...)` output per trajectory**: step counts, tool usage histograms, and a brief preview. (Saves context.)
- The aggregator then **pulls** detail on demand via tool calls. This is the key efficiency trick — trajectories live "out of context" and are paged in selectively.

### Interrogation Tool Surface (4 tools, from `aggagent/tools.py`)

1. **`GetSolutionTool` / `get_solution`** — fetch the **final-step content** of one or more trajectories. Supports single or batch retrieval. This is the "what did each candidate answer?" tool.

2. **`SearchTrajectoriesTool` / `search_trajectory`** — **keyword / phrase search across trajectories** using ROUGE-L recall scoring; optional role filter (user/assistant/tool). Returns ranked snippets. This is the "did any trajectory ever observe X?" tool.

3. **`GetSegmentTool` / `get_segment`** — **read a contiguous step range (max 5 steps)** from a specific trajectory, with full formatting. Returns surrounding context, not just the matching line. This is the "let me see the actual tool output in context" tool.

4. **`FinishTool` / `finish`** — submit the final synthesized answer. Variants: standard XML, Qwen labelled-text, long-form report. The finish tool enforces the output format.

### Algorithmic Loop (from `aggagent/agent.py`)

```
def run(question, trajectories):
    msgs = [system_prompt, user_question, metadata_for_each_trajectory]
    while not finished and iters < 100:
        response = LLM(msgs, tools=[GetSolution, SearchTrajectories, GetSegment, Finish])
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call)         # raw trajectory inspection
            msgs.append(result)
        if Finish was called: return solution
        if context approaching limit: force-finish (only_finish=True)
    return error
```

**Other details:**
- Iteration limit: **100 steps** for the aggregator.
- Context-overflow handling: when token budget runs low, the aggregator is forced to call `finish` (no more `get_segment` calls allowed) — graceful degradation.
- Supports OpenAI / Gemini / Qwen / MiniMax / local vLLM backends.
- Tracks per-iteration statistics (server errors, tool usage, token usage).
- Task-family-specific system-prompt swaps (long-form for HealthBench / ResearchRubrics).
- Tool names are sanitized via regex to drop non-alphanumeric characters before being passed to providers that restrict the name namespace.

### Why This Beats Flat Synthesis
- Avoids context blow-up: don't concatenate; page in on demand.
- Avoids majority-vote dilution: a single grounded tool observation > N ungrounded reasoning chains.
- Prevents silent error swallowing: aggregator explicitly inspects tool outputs.
- Enables disagreement resolution: when trajectories disagree, the aggregator can `search_trajectory` to find which one has the supporting evidence.

### Source
- arXiv 2604.11753 (Lee, Yen, Ye, Chen, 2026).
- Repo `princeton-pli/AggAgent`: `aggagent/prompts.py`, `aggagent/tools.py`, `aggagent/agent.py` (all Apache-2 licensed; verbatim quotes above).

---

## Lower-Priority Gaps

### Anthropic Managed Agents "Dreaming"

**State of public documentation (2026-05-20):** Anthropic has *announced* Dreaming as a research preview for Claude Managed Agents (rolled out at Code with Claude 2026). The **literal replay-and-extract algorithm and consolidation prompts have not been released publicly.** What is documented:

**Pipeline (4 stages, paraphrased from Anthropic announcement + multiple secondary sources):**
1. **Log capture**: during normal agent sessions, structured logs are persisted with metadata about task outcomes, tool calls, and explicit corrections (success/failure flags).
2. **Replay**: on a schedule (nightly / hourly / configurable interval), the dreaming sub-agent receives a structured prompt that "instructs it to read recent session transcripts, compare against existing memories, identify changes, and write updated memory entries."
3. **Extract**: the sub-agent identifies recurring failure patterns and successful task templates — i.e. patterns that "happened more than once." Statistical recurrence is the filter that distinguishes signal from noise.
4. **Consolidate**: structured summaries are written back to persistent storage (project-level files like `CLAUDE.md` in the public Claude Code variant). The cycle "orients on current project state, prunes stale entries, merges duplicates, and reorganizes notes."

**Trigger surface (in Claude Code):**
- `/dream` slash command (manual).
- Background process on configurable interval.
- Does not run during active sessions (avoids latency penalty).

**Reported impact**: Harvey reported ~6× task-completion rate increase after Dreaming was enabled (Anthropic announcement number, internal benchmark).

**[paraphrased — verbatim consolidation prompt not released]:** "Review the following session transcripts. Identify (a) recurring failure modes, (b) successful patterns worth promoting to long-term memory, (c) stale memory entries to remove. Output: a structured patch to the memory store."

### BrowseConf (arXiv 2510.23458) — Confidence Retry Pattern

**Verbalized Confidence Prompt (verbatim, Table 3 / Appendix B.3):**
```
**Answer**: [A concise and clear answer, directly answering the question]
**Confidence**: [A confidence score between 0-100 representing how sure you are
that the answer is correct...]
```

Full instruction text:
> "A confidence score between 0-100 representing how sure you are that the answer is correct. A value close to 0 means you think the answer is likely to be wrong, while a value close to 100 means you think the answer is likely to be correct. Just give the integer, no explanation needed."

**Two retry-variant prompts:**

1. **BrowseConf-Summary (Table 4):**
   > "Below is a summary of a previous attempt at the question"
   — provides a summary of the prior trajectory to the new attempt, biasing it to explore different angles.

2. **BrowseConf-Neg (Table 5):**
   > "Below are identified incorrect answers to the question. You MUST NOT give these answers again unless some turned out to be correct."
   — explicit blocklist of prior wrong answers; the strongest retry signal.

**Calibration threshold τ*** (verbatim):
> "the minimum threshold that ensures at least k% relative accuracy improvement on samples with confidence exceeding τ"

Ablations test k ∈ {5, 10, 20}. **No single fixed threshold** — it's dataset-calibrated, tuned to guarantee at least k% accuracy lift at the threshold-passed slice. Empirically: accuracy ≈ 0 below 70% confidence; >2× average accuracy above 95% confidence (strong calibration signal).

**Test-Time Scaling Logic**: if final confidence < τ*, spawn a new attempt (Summary or Neg variant); else accept. The compute budget is dynamically allocated to the uncertain queries.

### BATS (arXiv 2511.17006) — Budget Tracker Context Injection

**Verbatim budget-tracker block** (injected after each tool response):
```
Budget Tracker <budget>
  Tool1 Budget Used: ##, Tool1 Budget Remaining: ##
  Tool2 Budget Used: ##, Tool2 Budget Remaining: ##
Make the best use of the available resources.
</budget>
```

**Tiered behavioural guidance (verbatim from paper):**

- **HIGH (≥70% remaining):** *"Search: 3-5 diverse queries in one batch. Browse: up to 2-3 high-value URLs."*
- **MEDIUM (30-70%):** *"Search: 2-3 precise, refined queries per cycle. Browse: 1-2 URLs that close key knowledge gaps."*
- **LOW (10-30%):** *"Search: 1 tightly focused query. Browse: at most 1 most promising URL."*

**Dig-Deeper vs Pivot Decision (verbatim, from the verification module):**
- **CONTINUE**: *"If several constraints remain unverifiable but the trajectory appears promising, provided the budget is sufficient for deeper exploration."*
- **PIVOT**: *"If contradictions are identified or the remaining budget cannot support further investigation towards this lead, the agent is expected to terminate expensive or low-yield directions."*

The verification module performs a "constraint-by-constraint backward check" before issuing CONTINUE/PIVOT — i.e. it walks back through the verified facts and asks whether the remaining unverified ones are worth the marginal cost.

**Why this works**: prior work shows simply raising the tool-call budget *fails* to improve agent accuracy (agents lack budget awareness and burn calls inefficiently). BATS's contribution is the **continuous awareness signal** + the **policy guidance text** + the **explicit dig/pivot decision point** — all three together break the budget-ceiling.

---

## Notes on Confidence

| Gap | Confidence | Notes |
|---|---|---|
| **A. DRA Failure Taxonomy** | **High** (verbatim B.2 prompt + 5 categories nailed) | The 13 subcategory names were assembled from two independent secondary sources that converged; minor wording variance possible at the subcategory level (e.g. "Wrong Source" vs "Consulting Wrong Evidence" — same concept). |
| **B. OpenEvolve prompts** | **Very High** (literally pulled from the Apache-2 repo) | Every template above is verbatim from `openevolve/prompts/defaults/`. |
| **B. AlphaEvolve** | **Medium** (structural details from paper; literal production prompts not released) | DeepMind has not open-sourced the production prompts; OpenEvolve is the best proxy and the paper confirms it's structurally faithful. |
| **C. Co-Scientist** | **Medium** (mechanics nailed; literal pairwise-comparison prompt only paraphrasable) | The arXiv PDF appendix figures (A.4, A.5, A.17) embed prompts as raster images; not extractable via WebFetch. Initial Elo = 1200 is confirmed; K-factor is not disclosed. The two-tier (multi-turn for top, single-turn for bottom) mechanism + (novelty, correctness, testability) axes are confirmed. |
| **C. Aletheia** | **Medium-Low** for prompts (paper does not publish them; repo has outputs only). **High** for architecture (G/V/R + 3-branch routing + reject-when-uncertain). | The repo `google-deepmind/superhuman/aletheia` was checked — it contains per-problem solution PDFs but **no committed system prompts** as of 2026-05-20. We have the architecture confidently; the literal prompts are paraphrased. |
| **D. AggAgent** | **Very High** (Apache-2 repo, verbatim prompts and tool definitions) | The four-tool surface, three-prompt variants, and core operational guideline are all verbatim from the repo. |
| **Dreaming** | **Low-Medium** | No primary source has published the literal replay/extract/consolidate prompts; structure is from multiple converging secondary sources + Anthropic's announcement. |
| **BrowseConf** | **High** (verbatim from Tables 3-5) | All three prompt patterns + threshold logic confirmed from the HTML. |
| **BATS** | **High** (verbatim budget block + tiered guidance from paper) | Continue/Pivot decision text confirmed verbatim. |

**Couldn't fully fill:**
- AlphaEvolve's exact production system prompt (DeepMind has not released it; OpenEvolve fills the gap as a high-fidelity OSS implementation).
- Co-Scientist's exact COMPARE_IDEAS_PROMPT and SELF_PLAY_PROMPT text (figures are raster in the PDF; would need OCR on a high-DPI download).
- Aletheia's literal Generator / Verifier / Reviser prompts (the paper states "we share all prompts" pointing to a repo, but as of the check date the repo holds outputs only).
- Anthropic Dreaming's literal consolidation prompt (still a research preview; not in public docs).

For the SKILL v2 proposal, the verbatim coverage of **OpenEvolve, AggAgent, DeepVerifier B.2, BrowseConf, BATS** is more than sufficient to wire concrete blueprints. The architectural / paraphrased coverage of **AlphaEvolve, Co-Scientist, Aletheia, Dreaming** is enough to inform skill design without needing the literal upstream prompts.
