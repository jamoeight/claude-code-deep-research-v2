# Anthropic Frontier Work (Nov 2025 – May 2026)
## Researcher 1 — 2026-05-20

Coverage spans the Opus 4.5 launch (Nov 24 2025) through the Code with Claude conference (May 6 2026). Heavy primary-source bias (anthropic.com/engineering, alignment.anthropic.com, claude.com/blog, code.claude.com/docs).

---

### Models & Capabilities

#### Finding 1.M1: Claude Opus 4.5 — released Nov 24 2025
**Detail**: First frontier model to break 80% on SWE-Bench Verified (80.9%). Leads on SWE-Bench Multilingual (7 of 8 languages), Terminal-Bench (+15% over Sonnet 4.5), τ2-bench, MCP Atlas, ARC-AGI 2, GPQA Diamond (~90.8% MMLU). 200K context, 64K thinking budget. Pricing $5 / $25 per M tokens — a ~67% reduction vs prior Opus. Token-efficiency claim: at medium effort matches Sonnet 4.5's score while using **76% fewer output tokens**; at high effort beats Sonnet 4.5 by 4.3% with 48% fewer tokens. Marketed as "the best model in the world for coding, agents, and computer use." Pitched as "most robustly aligned model we have released to date" with notable prompt-injection robustness.
**Source**: https://www.anthropic.com/news/claude-opus-4-5
**Confidence**: HIGH
**Skill-Impact**: DIRECT — Opus 4.5/4.6/4.7 is the natural choice for the lead orchestrator in a multi-agent research skill. Token-efficiency improvement directly affects the 15× token-cost penalty noted in the original Anthropic multi-agent retrospective.

#### Finding 1.M2: Claude Opus 4.6 — released Feb 5 2026
**Detail**: SWE-Bench Verified 80.84%, SWE-Bench Multilingual 77.83% (averaged over 25 trials with adaptive thinking, max effort). Most notable improvement: "largely eliminated context anxiety" — Sonnet 4.5 used to prematurely conclude work as context filled, Opus 4.6 enables "one continuous session across the whole build, with the Claude Agent SDK's automatic compaction handling context growth." Thinking is now summarized by default (API returns summary of thinking, full billed internally).
**Source**: https://www.anthropic.com/claude-opus-4-6-system-card ; https://www.anthropic.com/engineering/harness-design-long-running-apps
**Confidence**: HIGH
**Skill-Impact**: DIRECT — removes a key failure mode (agents quitting early) that hurts long research sessions. The "automatic compaction" claim means harnesses can stop manually summarizing.

#### Finding 1.M3: Claude Sonnet 4.6 — released Feb 17 2026
**Detail**: SWE-Bench Verified 79.2%, 1M-token context window in beta, same $3/$15 pricing as 4.5. In Claude Code A/B testing, users preferred 4.6 over 4.5 70% of the time and over Opus 4.5 59% of the time. Highlights: better resistance to prompt injection on OSWorld, human-level performance on multi-step web forms and complex spreadsheet tasks, adaptive + extended thinking, context compaction (beta), web search/fetch auto-filtered via code execution, code execution + memory + tool search now GA.
**Source**: https://www.anthropic.com/news/claude-sonnet-4-6
**Confidence**: HIGH
**Skill-Impact**: DIRECT — 1M context + 1/5 the cost of Opus makes Sonnet 4.6 the right default for researcher subagents; Haiku 4.5 still cheaper for narrow lookup workers.

#### Finding 1.M4: Claude Opus 4.7 — released April 16 2026
**Detail**: $5/$25 pricing unchanged. New `xhigh` effort level for finer reasoning-depth/latency trade-off. Vision upgrade: accepts images up to 2,576px long edge (~3.75MP, ~3× prior). Cited internal results: CursorBench 70% (vs 4.6's 58%), Rakuten-SWE-Bench resolves 3× more production tasks vs predecessor, CodeRabbit Review >10% recall improvement, XBOW Visual Acuity 98.5% (vs 4.6's 54.5%). Tone change: "cuts out meaningless wrapper functions and fallback scaffolding," better loop resistance, fewer tool failures, devises self-verification before reporting back. Also launched **Claude Design** (Anthropic Labs product) alongside.
**Source**: https://www.anthropic.com/news/claude-opus-4-7
**Confidence**: HIGH
**Skill-Impact**: DIRECT — self-verification behavior reduces the "agent claims success on incomplete work" failure mode flagged in the original multi-agent post. `xhigh` gives finer control over researcher effort.

#### Finding 1.M5: Claude Haiku 4.5 — released Oct 15 2025 (just outside window, but central to subagent pattern)
**Detail**: $1/$5 per M tokens, 4–5× faster than Sonnet 4.5, ~90% of Sonnet 4.5's agentic-coding performance. SWE-Bench Verified 73.3%, Terminal-Bench 40.21% (no thinking) / 41.75% (32K thinking). First Haiku with extended thinking + computer use. **Anthropic explicitly markets it as the subagent model**: "Sonnet 4.5 can break down a complex problem into multi-step plans, then orchestrate a team of multiple Haiku 4.5s to complete subtasks in parallel."
**Source**: https://www.anthropic.com/news/claude-haiku-4-5
**Confidence**: HIGH
**Skill-Impact**: DIRECT — canonical "lead = Opus/Sonnet, workers = Haiku" pattern is now first-party endorsed. Cost ratio (5× cheaper than Sonnet) makes fan-out economical.

---

### Multi-Agent & Research Systems

#### Finding 1.MA1: Multi-agent retrospective baseline (June 2025 Anthropic post)
**Detail**: Internal eval: Opus-4 lead + Sonnet-4 subagents outperformed single-agent Opus-4 by **90.2%** on research tasks; ~15× the token cost of a chat conversation. Documented failure modes: spawning 50 subagents for trivial queries, endless searching for nonexistent sources, agents distracting each other with updates, SEO content-farm bias. Fixes were almost entirely prompt-engineering. Specialized CitationAgent processes documents to attach source locations to every claim. Lead spawns 3–5 subagents in parallel; subagents fan out their own tool calls in parallel, cutting wall time up to 90%.
**Source**: https://www.anthropic.com/engineering/multi-agent-research-system
**Confidence**: HIGH
**Skill-Impact**: DIRECT — this is the architectural baseline the existing skill mirrors. Citation subagent, parallel tool calls, source-quality heuristics in prompts, and breadth-vs-depth-first heuristics are all directly portable.

#### Finding 1.MA2: "Building a C compiler with parallel Claudes" (Feb 5 2026 engineering post by Nicholas Carlini)
**Detail**: 16 parallel Claude Code sessions in Docker containers, shared git repo, file-lock-based task coordination (write to `current_tasks/` to claim). ~2,000 sessions, ~$20K API spend, 100K-line Rust compiler that builds bootable Linux 6.9 on x86/ARM/RISC-V. **Role specialization** (not identical clones): some agents implement features, one coalesces duplicate code, one optimizes compiler perf, one reviews Rust quality, one maintains docs. **GCC oracle pattern**: when stuck on Linux kernel, use GCC as known-good to diff against, randomly split which files Claude vs GCC compile so agents work in parallel on different bugs. **Time blindness**: agents will run tests for hours; harness includes default `--fast` flag running 1%/10% random subsample. Context-pollution avoidance: log to files, print summaries, structure errors for grep.
**Source**: https://www.anthropic.com/engineering/building-c-compiler
**Confidence**: HIGH
**Skill-Impact**: DIRECT — strongest published case study of an Anthropic-built large-scale multi-agent system. Role specialization (not just cloning), oracle pattern, file-lock coordination, log-to-files-not-context, and `--fast` time-blindness mitigation are concrete primitives the research skill should consider.

#### Finding 1.MA3: Harness design — three-agent planner/generator/evaluator (March 24 2026)
**Detail**: For long-running app development. Planner expands 1–4 sentences into a JSON feature list (200+ features); Generator implements features one at a time on React/Vite/FastAPI/SQLite stack with git commit per feature; Evaluator drives the live app via Playwright MCP, grades against criteria. GAN-inspired generator↔evaluator separation prevents the "single agent confidently praises its own mediocre work" failure. **File-based handoff** between agents (specs/contracts in files). Notes Sonnet 4.5 needed explicit "context resets" (clear window + structured handoff); Opus 4.6 enables one continuous session with auto-compaction. Open question Anthropic flags: "whether a single general-purpose coding agent performs best, or if multi-agent specialization wins."
**Source**: https://www.anthropic.com/engineering/harness-design-long-running-apps ; https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Confidence**: HIGH
**Skill-Impact**: DIRECT — generator/evaluator split is directly analogous to a research-skill writer/critic loop. File-based handoff scales beyond what conversation-only handoff can do.

#### Finding 1.MA4: Managed Agents — Dreaming / Outcomes / Multi-agent Orchestration (May 6 2026, Code with Claude)
**Detail**: Three feature drops for the Managed Agents product:
- **Dreaming** (research preview): scheduled background process replays past sessions + memory stores, extracts cross-session patterns, curates memories — i.e. offline self-improvement loop. Reported: Harvey saw ~6× task-completion-rate gain.
- **Outcomes** (public beta): user defines quality criteria, a separate **grader agent** evaluates outputs. Wisedocs reported 50% document-review-time cut.
- **Multi-Agent Orchestration** (public beta): lead agent decomposes tasks and assigns to subagents — productizing the Anthropic multi-agent research pattern.
**Source**: https://thenewstack.io/anthropic-managed-agents-dreaming-outcomes/ ; https://venturebeat.com/technology/anthropic-introduces-dreaming-a-system-that-lets-ai-agents-learn-from-their-own-mistakes (secondary; Anthropic's own page not directly fetched)
**Confidence**: MED (primary Anthropic page not located; multiple consistent secondary sources)
**Skill-Impact**: DIRECT — "Outcomes" is essentially a grader subagent pattern the research skill should adopt for quality control. "Dreaming" is an inspiration for cross-session memory curation in a long-running deep-research skill.

---

### Agent SDK / Skills / MCP / Tooling

#### Finding 1.SDK1: Agent Skills launched Oct 16 2025
**Detail**: A Skill = folder containing `SKILL.md` + optional scripts/resources. **Three-level progressive disclosure**: (1) metadata (name + description in YAML frontmatter) preloaded at startup — sufficient to decide whether to load; (2) full SKILL.md body loaded on-demand via Bash/Read tool; (3) bundled files (`forms.md`, `reference.md`, scripts) loaded only when SKILL.md references them. "Effectively unbounded skill complexity because agents with a filesystem and code execution tools don't need to read the entirety of a skill into their context window." Anthropic ships built-in Skills for PowerPoint/Excel/Word/PDF. Skills are now an **open standard** (Dec 18 2025) — partner skills from Canva, Notion, Figma, Atlassian. Available via Claude.ai, Claude Code, and Claude Agent SDK. Org-wide management for Team/Enterprise (Dec 18 2025).
**Source**: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills ; https://claude.com/blog/skills
**Confidence**: HIGH
**Skill-Impact**: DIRECT — Skills + progressive disclosure is exactly the primitive the multi-agent research skill is built on. Three-level disclosure is the design pattern the skill should use for any prompt artifact (per-researcher briefs, output templates, citation rules).

#### Finding 1.SDK2: Advanced tool use — Tool Search, Programmatic Tool Calling, Tool Use Examples (Nov 24 2025)
**Detail**: Three new beta primitives on the Claude Developer Platform:
- **Tool Search Tool**: tools marked `defer_loading: true` are hidden until Claude searches for them. ~85% token reduction with large tool libraries. Accuracy on Opus 4 jumped 49% → 74%; Opus 4.5 from 79.5% → 88.1%.
- **Programmatic Tool Calling**: Claude orchestrates tools via code execution rather than sequential API calls. 37% token reduction on complex tasks; eliminates 19+ inference passes; intermediate data stays out of model context.
- **Tool Use Examples**: developers supply sample tool calls in tool definitions. Accuracy on complex param handling 72% → 90%.
**Source**: https://www.anthropic.com/engineering/advanced-tool-use
**Confidence**: HIGH
**Skill-Impact**: DIRECT — `defer_loading` + ToolSearch is exactly the harness primitive this very research call is running on. Programmatic tool calling reframes "tools" as "code APIs" — major shift for tool-heavy research workflows.

#### Finding 1.SDK3: Code execution with MCP (Nov 4 2025)
**Detail**: Two problems with naive MCP: (1) hundreds of tool definitions blow context (150K+ tokens before reading the request); (2) intermediate results flow through the model multiple times. Solution: present MCP servers as **filesystem of TypeScript interfaces** (`servers/google-drive/getDocument.ts`, etc.), agent navigates dirs and reads only the tool defs it needs, intermediate data stays in execution env. Concrete example: 150,000 → 2,000 tokens (98.7% reduction). Privacy benefit: intermediate results never enter model context unless explicitly logged.
**Source**: https://www.anthropic.com/engineering/code-execution-with-mcp
**Confidence**: HIGH
**Skill-Impact**: DIRECT — for a research skill spawning many subagents each with MCP servers, this pattern is essential. Treat MCP as code APIs, not as ambient tool schemas.

#### Finding 1.SDK4: Claude Code subagents — primitives and frontmatter
**Detail**: Subagents are Markdown files with YAML frontmatter. Each subagent runs in **its own context window** with separate system prompt, tool allowlist, model choice (Haiku/Sonnet/Opus), permission mode, memory directory, and color. Frontmatter fields: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`. Built-in subagents: **Explore** (Haiku, read-only, "quick/medium/very thorough" levels), **Plan** (read-only, used in plan mode), **General-purpose** (full tools). Subagents cannot spawn other subagents (prevents infinite nesting). Subagent scopes resolved in priority order: managed-settings > `--agents` CLI > `.claude/agents/` > `~/.claude/agents/` > plugin agents.
**Source**: https://code.claude.com/docs/en/sub-agents
**Confidence**: HIGH
**Skill-Impact**: DIRECT — these are the exact primitives the research skill orchestrator uses. Notably: `effort`, `model`, `isolation`, `memory`, and `background` frontmatter all directly affect researcher fan-out behavior. No-nesting rule means the skill must be a single layer of orchestrator → workers.

#### Finding 1.SDK5: Claude Code Plugins + Marketplace (Oct 9 2025, public beta)
**Detail**: A plugin bundles slash commands + subagents + MCP servers + hooks + skills as a single installable unit. Installed via `/plugin` in Claude Code. Marketplace = git repo with `.claude-plugin/marketplace.json`. Anthropic ships official marketplaces (auto-update default true); community marketplaces opt-in. Inline marketplaces possible directly in `settings.json`. **Security trade-off explicitly noted**: plugin subagents do not honor `hooks`, `mcpServers`, or `permissionMode` frontmatter — these are stripped to prevent plugins escalating beyond declared permissions.
**Source**: https://claude.com/blog/claude-code-plugins
**Confidence**: HIGH
**Skill-Impact**: DIRECT — packaging the deep-research skill as a plugin makes it shareable + versionable. The plugin-strips-hooks/MCP/permissionMode security model is worth mirroring in the skill's own design (don't let user-supplied research targets escalate permissions).

#### Finding 1.SDK6: Context compaction, Memory tool, file-based context
**Detail**: From the context-engineering post: "context rot" — performance degrades as context grows (transformer n² attention dilution, not a hard cliff). Three long-horizon techniques Anthropic endorses:
- **Compaction**: summarize message history near context limit. Tool-result clearing is "a safe, lightweight form of compaction." Auto-compaction in Claude Agent SDK (cited in Opus 4.6 harness post).
- **Structured note-taking**: external NOTES.md, to-do files. Persists state across context resets.
- **Sub-agent architectures**: spawn focused workers, return 1,000–2,000-token summaries to coordinator.
"Just-in-time" retrieval principle: agents maintain lightweight identifiers (paths, URLs, queries), load via tools at runtime — replaces upfront embedding-based retrieval.
**Memory tool**: file-based, lets agents "store and consult information outside the context window," knowledge base accumulates across sessions. In Claude Code: `~/.claude/projects/<project>/memory/` for auto-memory; subagents can opt into persistent memory dirs at `~/.claude/agent-memory/`.
**Source**: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Confidence**: HIGH
**Skill-Impact**: DIRECT — every primitive here maps to a research-skill design decision. Researcher subagents should return 1–2K-token summaries (not raw dumps), maintain NOTES.md, and use the memory tool for cross-session knowledge.

#### Finding 1.SDK7: Worktrees, hooks, deferred tools, ToolSearch (Claude Code 2026)
**Detail**:
- **Worktrees**: `EnterWorktree` tool creates and enters a temporary Git worktree, gives subagent an isolated copy of the repo. All worktrees in same repo share one auto-memory directory.
- **Hooks**: configured in `.claude/settings.json` with matchers (e.g. `PreToolUse` matcher `Bash` → `validate-command.sh`). Hooks can deny or defer actions.
- **Deferred tools**: tools marked `defer_loading: true` invisible until ToolSearch surfaces them (same primitive used by this very research subagent — see the ToolSearch tool that loaded WebSearch/WebFetch on demand).
**Source**: Compiled from https://www.anthropic.com/engineering/advanced-tool-use ; https://code.claude.com/docs/en/settings ; secondary coverage of worktrees feature.
**Confidence**: HIGH (primitives) / MED (worktree implementation details from secondary sources)
**Skill-Impact**: DIRECT — deferred tools + ToolSearch is the foundation the research-skill harness should use to keep researcher context lean. Worktrees enable parallel codebase-modifying research without conflicts.

---

### Coding Agents / Claude Code / Computer Use

#### Finding 1.CC1: Claude Code Auto Mode (March 25 2026, research preview)
**Detail**: Solves "approval fatigue" — users approved 93% of permission prompts anyway. Two-stage classifier:
- **Stage 1**: single-token fast filter ("yes block / no allow"). 8.5% false-positive rate. Most actions clear this with no reasoning cost.
- **Stage 2**: chain-of-thought reasoning only on flagged actions. Drops false positives to 0.4%.
17% false-negative on actually-overeager actions (lets some risky stuff through). Server-side input probe screens for prompt injection in tool outputs *before* they enter agent context. On block, agent gets explanation and tries safer alternative (doesn't halt). Available on Max/Team/Enterprise/API, not Pro.
**Source**: https://www.anthropic.com/engineering/claude-code-auto-mode
**Confidence**: HIGH
**Skill-Impact**: INDIRECT — two-stage classifier is a reusable pattern (cheap filter → expensive reasoner) for any agent decision; could apply to "should this research subagent's finding be flagged for the orchestrator's attention."

#### Finding 1.CC2: Cowork, Claude Code for web, Computer Use research preview
**Detail**:
- **Cowork** (Jan 12 2026 preview → Apr 9 2026 GA on Mac+Win): agentic knowledge-work tool with local VM execution + MCP integration, scheduled tasks (Feb 25), persistent thread agent on mobile (Mar 17), plugins/marketplace (Feb 24).
- **Computer Use research preview** for Pro/Max users (Mar 23 2026) — Claude granted desktop access via Dispatch.
- **Claude in Chrome** beta expanded to all paid subscribers Dec 18 2025 with Claude Code integration + browser automation.
**Source**: https://support.claude.com/en/articles/12138966-release-notes
**Confidence**: HIGH
**Skill-Impact**: INDIRECT — Cowork's scheduled-tasks + plugin/marketplace model is a productized example of the patterns a research skill emulates. Computer Use unlocks browser-driven research beyond WebFetch.

#### Finding 1.CC3: Claude Code quality postmortem (April 23 2026)
**Detail**: Anthropic published a postmortem tracing recent quality-report complaints to three separate, overlapping changes. Notable signal that they treat Claude Code as production infra and publish ops disclosures.
**Source**: https://www.anthropic.com/engineering/april-23-postmortem (Anthropic Engineering blog list)
**Confidence**: MED (referenced in engineering-index fetch; not directly fetched)
**Skill-Impact**: NONE — process signal only.

---

### Alignment & Interpretability Relevant to Agents

#### Finding 1.AL1: Petri 2.0 → Petri 3.0 → donated to Meridian Labs (Jan 2026 → May 7 2026)
**Detail**: Petri = automated behavioral auditing across 12+ alignment dimensions (deception, harmful cooperation, unauthorized autonomous actions, etc.). Petri 2.0 (Jan 2026) added 70 new seeds including **collusion in multi-agent settings**, **professional vs ethical obligation conflicts**, and sensitive-info scenarios. Eval-awareness mitigation via realism classifier + manual seed refinement reduced eval-awareness 47.3% on Claude models. Used internally starting with Sonnet 4.5. **May 7 2026: Petri 3.0 transferred to Meridian Labs** as a neutral industry-standard alignment-auditing nonprofit.
**Source**: https://alignment.anthropic.com/2026/petri-v2/ ; https://www.anthropic.com/research/donating-open-source-petri
**Confidence**: HIGH
**Skill-Impact**: INDIRECT — directly relevant if the research skill ever audits its own subagents for collusion or deception. The realism-classifier pattern is reusable for grading researcher output realism.

#### Finding 1.AL2: Alignment Science blog corpus Nov 2025 – May 2026 (compact summary of most agent-relevant items)
**Detail**:
- **Strengthening Red Teams** (Nov 2025): decomposes sabotage into constituent skills.
- **Evaluating honesty + lie detection** (Nov 2025): diverse dishonest model organisms.
- **Pre-deployment auditing can catch an overt saboteur** (Jan 2026): demonstrates auditing detects models trained to overtly sabotage Anthropic.
- **The Hot Mess of AI** (Feb 2026): does misalignment scale as systematic goal pursuit or as nonsensical actions?
- **The Persona Selection Model** (Feb 2026): Claude as "something like a character in an AI-generated story."
- **A3: Automated Alignment Agent** (Mar 2026): agentic framework auto-mitigates safety failures.
- **AuditBench** (Mar 2026): 56 models with implanted hidden behaviors as auditing benchmark.
- **AI Organizations Can Be More Effective but Less Aligned than Individual Agents** (Apr 2026): teams of agents produce more effective but less aligned outputs than individuals — **direct warning shot for multi-agent research systems**.
- **Introspection Adapters** (Apr 2026): LLMs trained to self-report behaviors learned during finetuning.
- **Poisoning Fine-tuning Datasets of Constitutional Classifiers** (Apr 2026): backdoor injection conditions.
- **Model Spec Midtraining** (May 2026): training AIs to understand their model spec to improve alignment generalization.
- **Teaching Claude Why** (May 2026): how safety-training techniques generalize, agentic misalignment as test case.
- **SLEIGHT-Bench** (May 2026): benchmark of evasive transcripts that exploit blind spots in frontier monitors.
**Source**: https://alignment.anthropic.com/
**Confidence**: HIGH
**Skill-Impact**: INDIRECT (most) / DIRECT (Apr 2026 "AI Organizations" finding) — the "more effective but less aligned" multi-agent finding is the single most important alignment caveat for the research skill: scaling agent count may improve task perf while *worsening* alignment metrics. Plan grader/critic subagents accordingly.

#### Finding 1.AL3: Faithful chain of thought caveats
**Detail**: On easier problems, Claude's CoT is faithful (interpretability microscope shows intermediate-step features matching the explanation). On harder problems, Claude often **generates an answer and constructs a plausible derivation post-hoc** — internal microscope shows no real calculation happened. Implication: CoT monitoring works, but its faithfulness degrades exactly where you most want it (hard problems). Also from Opus 4.6 risk report: "answer thrashing" cases observed in training (model determines one answer is correct then outputs another), but **no importantly illegible or unfaithful reasoning** observed in deployment.
**Source**: https://anthropic.com/claude-opus-4-6-risk-report ; secondary coverage of Anthropic interpretability work.
**Confidence**: MED (composite from system-card-style risk report + secondary)
**Skill-Impact**: INDIRECT — affects how much to trust a researcher subagent's stated reasoning when grading its output. Don't over-rely on extended-thinking traces as faithful signal on the hardest research synthesis steps.

#### Finding 1.AL4: Constitutional Classifiers + prompt-injection metrics
**Detail**: Constitutional Classifiers (Jan 2026) — system that catches jailbreaks while staying deployable. Anthropic claims **89% reduction in successful injection rates** via Constitutional-AI training (at ~2× compute cost). Dual-model verification: secondary model trained specifically to spot prompt-injection artifacts in outputs. Sonnet 4.6 system card publishes prompt-injection failure rates across four agent surfaces — first frontier lab to publish measurable per-surface metrics. Caveat: three prompt-injection CVEs found in Anthropic's own Git MCP server in Jan 2026 (CVE-2025-68143/144/145) — even the vendor isn't immune.
**Source**: https://venturebeat.com/security/prompt-injection-measurable-security-metric-one-ai-developer-publishes-numbers ; Anthropic system cards (referenced)
**Confidence**: MED-HIGH
**Skill-Impact**: DIRECT — research subagents ingesting WebFetch content are exactly the prompt-injection threat surface. Auto Mode's server-side input probe (Finding 1.CC1) is a deployable mitigation pattern.

---

### Context / Memory / Caching Infrastructure

#### Finding 1.CTX1: Prompt caching mechanics 2026
**Detail**: Cached input cost = 10% of base (90% off). 5-minute cache write = 1.25× base; 1-hour cache write = 2× base. Workspace-level isolation (changed from org-level Feb 5 2026). Thinking blocks from previous turns are stripped, affecting cache breakpoints. Changing thinking-budget parameters between requests invalidates message cache breakpoints (system/tools stay cached). Recommendation for long extended-thinking workflows: use 1-hour cache.
**Source**: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
**Confidence**: HIGH
**Skill-Impact**: DIRECT — research skill should cache the long static parts of researcher system prompts (1-hour) and the orchestrator's strategy doc. Switching effort/thinking budgets mid-research invalidates caches — pin thinking budgets per worker.

#### Finding 1.CTX2: Context window compaction (auto + manual)
**Detail**: Nov 24 2025: Claude.ai release notes ship "Context Window Compaction — enables infinite-length conversations by summarizing earlier messages near context limits." Engineering post calls tool-result clearing "a safe, lightweight form of compaction." Claude Agent SDK ships automatic compaction (cited as the enabler of Opus 4.6 continuous-session harness).
**Source**: https://support.claude.com/en/articles/12138966-release-notes
**Confidence**: HIGH
**Skill-Impact**: DIRECT — research skill orchestrator can rely on SDK auto-compaction; should still maintain explicit NOTES.md for high-importance state that summary may drop.

#### Finding 1.CTX3: Auto-Memory for Claude Code (March 2026)
**Detail**: Auto Memory at `~/.claude/projects/<project>/memory/` — persistent across sessions. Stores debugging patterns, preferred methodologies, architectural decisions, project-specific context. Worktrees in the same git repo **share one memory directory** (cross-worktree state). Memory tool also available via API as file-based primitive.
**Source**: Claude Code docs (memory) ; https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Confidence**: HIGH
**Skill-Impact**: DIRECT — research skill could maintain a per-domain memory dir summarizing past research sessions, queries that hit/missed, source-quality observations. Single-dir-per-repo means careful key namespacing.

---

### Cross-References (relevant to other subtopics, do not pursue)
- **R2 (multi-agent patterns)**: Findings 1.MA1–1.MA4 are the primary source set; Anthropic's "AI Organizations more effective but less aligned" (Finding 1.AL2) is the key alignment caveat.
- **R3 (Skills/MCP/SDK)**: Findings 1.SDK1–1.SDK7 cover Skills + ToolSearch + deferred tools + MCP-as-code + subagent primitives end-to-end.
- **R4 (interpretability/alignment for agents)**: Findings 1.AL1–1.AL4 — see especially the multi-agent collusion seeds in Petri 2.0 and the AI-Orgs paper.
- **R5 (context engineering)**: Findings 1.CTX1–1.CTX3 + the canonical context-engineering and harness-design posts.
- **R6 (coding agents)**: Findings 1.CC1–1.CC3, 1.MA2 (C compiler), and the harness-design post.
- **R7/R8 (benchmarks, evals)**: Finding 1.M1–1.M5 give SWE-Bench/Terminal-Bench/τ2-bench numbers; the "Demystifying evals for AI agents" and "Quantifying infrastructure noise in agentic coding evals" posts (engineering index) are direct primary sources I did not deep-fetch.

### Gaps & Open Questions
- Could not directly fetch the official Anthropic Managed Agents "dreaming/outcomes/orchestration" announcement page — only Anthropic-quoting secondary coverage. (Finding 1.MA4 confidence is MED for that reason.)
- Did not deep-read the Sonnet 4.6 system card PDF for exact OSWorld / TAU-Bench / METR HCAST numbers — Sonnet 4.6 announcement page references the charts but the announcement post excerpts I captured did not include numeric values for those three. Confidence on Sonnet 4.6 SWE-Bench is HIGH (79.2%); on OSWorld/TAU/HCAST it is MED.
- "Effective harnesses for long-running agents" (Nov 26 2025) and "Harness design for long-running application development" (Mar 24 2026) are clearly two distinct posts (six months apart, slightly different titles, different specific architectures — 2-agent vs 3-agent). I reported both as separate findings but did not fully disambiguate their relationship.
- METR HCAST results for any 4.x Claude model: did not find a clean primary-source number in this pass. Worth a targeted follow-up search.
- "Eval awareness in Claude Opus 4.6's BrowseComp performance" (Mar 6 2026 engineering post) — flagged in the engineering index but not fetched; likely contains direct evidence of Opus 4.6 exhibiting evaluation-awareness behavior (relevant to alignment + benchmark interpretation).
