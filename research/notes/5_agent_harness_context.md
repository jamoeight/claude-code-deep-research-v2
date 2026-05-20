# Agent Harness & Context Engineering (Nov 2025 – May 2026)
## Researcher 5 — 2026-05-20

This document captures findings on agent harness primitives and context-engineering techniques for long-running, context-bound agents — the techniques most relevant to building a deep-research multi-agent skill.

---

## Hierarchical Memory Systems

### Finding 1: MemGPT → Letta v1 — OS-inspired tiered memory has matured to production
- **Detail**: MemGPT's "context window as constrained RAM, archival as disk" model has been productized as Letta. Letta v1 (May 2026) deprecates the heartbeat/`send_message` tool plumbing because frontier models are now post-trained on agentic patterns natively. Letta uses three memory tiers: **core** (in-context blocks compiled into the system prompt every step), **archival** (external vector store, agent-queried with `archival_memory_search`), **recall** (conversation history, searchable on demand). Sonnet 4.5's memory tool primitives are first-class.
- **Source**: [Letta — Agent Memory](https://www.letta.com/blog/agent-memory) · [Letta v1 Agent Loop](https://www.letta.com/blog/letta-v1-agent) · [DeepWiki: Letta Memory System](https://deepwiki.com/letta-ai/letta/2.3-agent-memory-system)
- **Confidence**: High
- **Skill-Impact**: INDIRECT — informs how we should structure persistent state across research sessions.

### Finding 2: A-MEM (Agentic Memory, NeurIPS 2025) — Zettelkasten-style memory graph
- **Detail**: A-MEM auto-generates structured notes per memory (contextual descriptions, keywords, tags) and creates dynamic links between notes — a Zettelkasten knowledge net rather than a flat vector store. The system updates its own knowledge graph as memories are added, getting more cohesive over time.
- **Source**: [arXiv 2502.12110](https://arxiv.org/abs/2502.12110) · [agiresearch/A-mem](https://github.com/agiresearch/a-mem)
- **Confidence**: High (NeurIPS-accepted with code)
- **Skill-Impact**: INDIRECT — too heavyweight for a single research session, but the "linked notes" pattern is portable.

### Finding 3: Mem0 vs Zep benchmark fight ended with task-dependent winners
- **Detail**: On LongMemEval (GPT-4o), **Zep scores 63.8%** vs **Mem0 49.0%** — a 15-point gap attributed to Zep's temporal knowledge graph (Graphiti) storing fact-validity windows. On LoCoMo, Mem0's April 2026 algorithm leads with **92.5 / 94.4 on LongMemEval**, using ~6,900 tokens/query vs ~26K for full-context. Mem0 = fast simple retrieval (chatbots); Zep = temporally-correct "what was true when" (enterprise).
- **Source**: [Mem0 State of Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026) · [Atlan: Zep vs Mem0](https://atlan.com/know/zep-vs-mem0/) · [Vectorize: Zep vs Cognee](https://vectorize.io/articles/zep-vs-cognee)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

### Finding 4: BEAM benchmark — 1M and 10M token scales expose temporal-abstraction gap
- **Detail**: BEAM tests at 1M+ token scales. Performance drops ~25% moving 1M → 10M tokens. Open production gaps: temporal abstraction, cross-session identity, memory staleness, and domain-specific evaluation.
- **Source**: [Mem0 State of Agent Memory 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026)
- **Confidence**: Medium-High
- **Skill-Impact**: NONE for the skill itself, but warns us not to over-trust long contexts.

### Finding 5: Cognee — knowledge-graph-native memory (vs vector-only)
- **Detail**: Cognee's `.add()` / `.cognify()` / `.search()` API builds knowledge graphs as the primary retrieval surface (extracts entities + relationships from 38+ sources). Recommended for reasoning over large document corpora where entity relationships are first-class. Bayer + University of Wyoming production deployments.
- **Source**: [Cognee blog](https://www.cognee.ai/blog/fundamentals/how-cognee-builds-ai-memory) · [Memgraph: From RAG to Graphs](https://memgraph.com/blog/from-rag-to-graphs-cognee-ai-memory)
- **Confidence**: Medium
- **Skill-Impact**: INDIRECT.

### Finding 6: Anthropic Memory Tool — `/memories` filesystem, GA April 2026
- **Detail**: Anthropic's memory tool exposes `/memories` (a directory) to the model. Six file ops: `view`, `create`, `str_replace`, `insert`, `delete`, `rename`. Memory is **client-side-executed**: the agent emits memory tool calls, the application handles file I/O. On Managed Agents (public beta April 23, 2026), `/mnt/memory/` mounts inside the container so bash/code-exec can use it directly. One agent can share memory with sibling agents in the same workspace.
- **Source**: [Memory tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) · [Anthropic Managed Agents Memory](https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta) · [Anthropic Cookbook: Context Engineering](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- **Confidence**: High (official docs)
- **Skill-Impact**: **DIRECT** — Researcher agents could write findings to a shared `/memories/research_session_XX/` directory accessible to all subagents.
- **PROPOSED EDIT**: Add a "Shared memory" primitive to the orchestrator: before spawning researchers, create `files/research_session_<id>/memory/` and instruct each researcher to write/read structured notes there. The orchestrator reads the directory at synthesis time instead of relying solely on returned summaries.

---

## Context Compaction & Summarization

### Finding 7: Anthropic Compaction API (`compact_20260112`) — server-side, GA Jan 2026
- **Detail**: Production API: pass `context_management.edits=[{"type":"compact_20260112"}]` with beta header `compact-2026-01-12`. Default trigger 150K input tokens (minimum 50K). Generates a `compaction` block; subsequent requests automatically discard all messages prior to the block. Supports custom `instructions` (e.g., "Focus on preserving code snippets, variable names, and technical decisions"). Available across Claude API, Bedrock, Vertex, Foundry; ZDR-compatible. Compatible with prompt caching (ephemeral cache control on compaction blocks).
- **Source**: [Compaction — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/compaction) · [Claude Lab: Compaction API Guide](https://claudelab.net/en/articles/api-sdk/compaction-api-context-management)
- **Confidence**: High
- **Skill-Impact**: **DIRECT** for the orchestrator's long-running runs.
- **PROPOSED EDIT**: For the orchestrator (which holds the full multi-researcher transcript), enable compaction with `trigger=120_000` and custom `instructions` preserving "research questions assigned per researcher, key findings, source URLs, gap analysis." Researcher subagents typically finish well under 200K and do NOT need compaction enabled.

### Finding 8: Three-primitive context-engineering framework (Anthropic cookbook)
- **Detail**: Production agents combine three orthogonal context tools:
  - **Tool-result clearing** (`clear_tool_uses_20250919`): replaces old `tool_result` bodies with placeholders, keeps the `tool_use` record. Mechanical, zero-inference, surgical. Use for "context dominated by large re-callable tool outputs (file reads, API queries)." Triggered at e.g. 30K tokens, keeps last 4 tool uses.
  - **Compaction** (`compact_20260112`): summarizes whole transcript when long dialogue/reasoning accumulates.
  - **Memory tool**: cross-session persistence.
  - Example: a research agent went baseline 335K → 173K peak with clearing alone; combined with compaction at 150K, ran indefinitely.
- **Source**: [Anthropic Cookbook: Context Engineering](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools)
- **Confidence**: High (official cookbook with code)
- **Skill-Impact**: **DIRECT**
- **PROPOSED EDIT**: Add `clear_tool_uses_20250919` to the researcher subagent config with `trigger=30_000`, `keep=4`. Researcher subagents do many WebSearch + WebFetch calls; the verbatim WebFetch outputs are pure context bloat once the researcher has extracted findings. Excluding `memory` from clearing preserves cross-session notes.

### Finding 9: Anchored iterative summarization beats full-reconstruction (Factory 36K-msg study)
- **Detail**: Factory evaluated 36,000 real engineering session messages: **anchored iterative summarization** (merging new summaries into a persistent state across compactions) produces higher accuracy, completeness, and continuity scores than reconstructing summary from full history each time. The persistent-state pattern is the SOTA recommendation.
- **Source**: [Zylos: AI Agent Context Compression Strategies](https://zylos.ai/research/2026-02-28-ai-agent-context-compression-strategies) · [Medium: Long Context Compaction Part 1](https://medium.com/@revoir07/long-context-compaction-for-ai-agents-part-1-design-principles-2bf4a5748154)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

### Finding 10: Agentic Context Engineering (ACE) — evolving playbooks beat brevity bias
- **Detail**: Stanford/SambaNova/UC Berkeley 2025-2026 work proposes "ACE": treat context as an evolving playbook with three modules (generate, reflect, curate). Solves two failure modes: **brevity bias** (summaries drop domain insights) and **context collapse** (iterative rewriting erodes details). Empirical: +10.6% on agents, +8.6% on finance; matches the top AppWorld production agent using a smaller open-source model.
- **Source**: [arXiv 2510.04618](https://arxiv.org/abs/2510.04618) · [InfoQ writeup](https://www.infoq.com/news/2025/10/agentic-context-eng/)
- **Confidence**: High
- **Skill-Impact**: INDIRECT, but motivates structured (not free-text) memory blocks.

### Finding 11: "Pre-Rot Threshold" — compact before context degrades, not before limit
- **Detail**: Practitioners now distinguish the *technical* context limit (1M, 2M) from the *quality* limit (~256K for 1M-window models). Best practice: define a Pre-Rot Threshold (Cline uses `max(window - 40_000, window * 0.8)`) and compact preventively. Keeping working context at 40-60% utilization is the goal. Anti-pattern: panic-compacting at 80-100%.
- **Source**: [Morph: Context Engineering](https://www.morphllm.com/context-engineering) · [Cline: Context Window Explained](https://cline.bot/blog/clines-context-window-explained-maximize-performance-minimize-cost) · [Morph: Context Rot](https://www.morphllm.com/context-rot)
- **Confidence**: High (multiple converging sources)
- **Skill-Impact**: **DIRECT**.
- **PROPOSED EDIT**: Set the orchestrator's compaction trigger to **40% of model context window** (e.g., 80K for 200K-window models, 400K for 1M-window models), not 150K-blanket. Add a check at synthesis time: "if context_utilization > 60%, summarize researcher reports before passing to synthesis stage."

---

## Sub-Agent Isolation & Return-Channel Design

### Finding 12: Each subagent = isolated 200K context, parent gets only the summary
- **Detail**: Claude Code subagent pattern: parent spawns subagent with a specific prompt; subagent does its work (file reads, searches, tool calls) in its own context window; only the final output returns to the parent. "All intermediate noise stays inside the subagent's context and never touches the parent's conversation." This isolation prevents context rot from compounding over long sessions. Parent runs concurrently with multiple subagents.
- **Source**: [Claude Code Subagents — Tembo](https://www.tembo.io/blog/claude-code-subagents) · [Nimbalyst: Subagents Guide](https://nimbalyst.com/blog/claude-code-subagents-guide/) · [Builder.io: Subagents](https://www.builder.io/blog/subagents)
- **Confidence**: High
- **Skill-Impact**: **DIRECT** (this is core to the deep-research skill).

### Finding 13: Return-channel design — structured summary, not raw trace
- **Detail**: Known footgun: if subagents dump their full journey into the parent, you've traded one polluted context for N polluted contexts that merge at the end. **The pattern that works: force the subagent to synthesize a structured summary** — what changed, what was tested, what's risky, source URLs. Discard the raw trace. Microsoft Copilot Studio specifically suppresses cross-agent reference forwarding for safety, so citations must be explicitly carried in the summary structure.
- **Source**: [Builder.io: Subagents](https://www.builder.io/blog/subagents) · [Augment: Single vs Multi-Agent](https://www.augmentcode.com/guides/single-agent-vs-multi-agent-ai)
- **Confidence**: High
- **Skill-Impact**: **DIRECT**.
- **PROPOSED EDIT**: Each researcher must return a **fixed-format structured summary**: `{findings: [{detail, source_url, confidence, skill_impact}], gaps: [...], cross_refs: [...]}`. The current skill already does this in the markdown template — make it stricter (require JSON-ish parseable structure inside the markdown so the orchestrator's synthesizer can ingest deterministically). Explicitly forbid researchers from returning raw search transcripts.

### Finding 14: Anthropic's multi-agent research blueprint
- **Detail**: Lead Researcher (orchestrator) analyzes query → plans → saves plan to memory → spawns parallel subagents with isolated context windows → each subagent has its own tool access → Citation Agent verifies claims against sources. **Performance: Opus orchestrator + Sonnet subagents = +90.2% over single Opus.** Scaling rule: 1 agent / 3-10 tool calls for simple fact-checks; 10+ subagents with divided responsibilities for complex queries. Interleaved thinking is treated as "controllable scratchpad."
- **Source**: [ByteByteGo: How Anthropic Built Multi-Agent Research](https://blog.bytebytego.com/p/how-anthropic-built-a-multi-agent) · [Anthropic Multi-Agent Research](https://aiagentwire.com/ai-agent-posts/anthropic-multi-agent-research-system) · [ZenML LLMOps DB entry](https://www.zenml.io/llmops-database/building-a-multi-agent-research-system-for-complex-information-tasks)
- **Confidence**: High
- **Skill-Impact**: **DIRECT** (foundational pattern for the skill).
- **PROPOSED EDIT**: Codify the dedicated **Citation Agent** as an explicit primitive in the skill: after researchers finish but before final synthesis, spawn a citation-verifier subagent that visits a sample of cited URLs and flags any unverifiable claims. Reduces hallucinated sources.

### Finding 15: Lost-in-the-middle is a 30%+ accuracy hit; persists in 2026
- **Detail**: U-shaped attention curve from RoPE positional encoding biases. Information in the middle of long contexts is recalled 30%+ worse than at start/end. **As of 2026, no production model has fully eliminated position bias.** Mitigations: context compression (shrink the middle region), inference-time attention calibration ("Found in the Middle" — subtracts positional bias, recovers up to 15pp), and pause-tuning (insert separator tokens). Best practical mitigation: keep working context small.
- **Source**: [Morph: Lost in the Middle](https://www.morphllm.com/lost-in-the-middle-llm) · [arXiv 2511.13900](https://arxiv.org/html/2511.13900v1) · [Beancount: Found in the Middle](https://beancount.io/bean-labs/research-logs/2026/07/02/found-in-the-middle-calibrating-positional-attention-bias)
- **Confidence**: High
- **Skill-Impact**: INDIRECT — reinforces small-window discipline.

---

## Prompt-Caching for Multi-Agent

### Finding 16: Cache savings 41–80% across OpenAI / Anthropic / Gemini for agentic workloads
- **Detail**: "Don't Break the Cache" (arXiv 2601.06007, Jan 2026) evaluates caching on DeepResearch Bench (500+ sessions, 10K-token system prompts, 3-50 tool calls). Three strategies tested: full-context (naive), system-prompt-only, and excluding-dynamic-tool-results. Findings:
  - Naive full-context caching can *increase* latency (cache invalidations cascade).
  - Best strategy: place dynamic content at the *end* of the system prompt, exclude dynamic tool results from cache, avoid dynamic function definitions.
  - Cost savings 41-80%; TTFT improvements 13-31%.
- **Source**: [arXiv 2601.06007](https://arxiv.org/abs/2601.06007)
- **Confidence**: High (peer-reviewable empirical study)
- **Skill-Impact**: **DIRECT**.
- **PROPOSED EDIT**: When spawning researcher subagents, the orchestrator should keep their system prompts *byte-identical* across instances (same tool surface, same skill instructions). Differences should be confined to the user-message research assignment. This lets Anthropic's prompt cache hit at 0.1× input cost for the shared prefix.

### Finding 17: Sliding 4-breakpoint pattern for long agent runs
- **Detail**: Anthropic's `cache_control` breakpoint sees only 20 content blocks behind it. In long tool loops, breakpoints fall out of range and need replacement. Production pattern: **place breakpoints on (1) the system+tools prefix, (2) round boundaries, (3) most-recent-user-block (longest cacheable prefix), (4) one floating breakpoint that rolls forward.** Cuts 25-turn agentic investigation to ~20% of uncached input cost.
- **Source**: [mager.co: Claude prompt caching](https://www.mager.co/blog/2026-04-29-claude-prompt-caching/) · [Prompt caching — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (we're calling the API, not implementing it ourselves, but worth knowing).

### Finding 18: Cache invalidation pitfalls — tool list & description churn
- **Detail**: Tools are part of the cached prefix. If your tool list changes (e.g., conditional MCP servers), the entire downstream cache invalidates. Practitioners should keep agent harness tool surface stable. Anti-pattern: placing a cache breakpoint after content that changes every request (constant new hashes, dashboard "shows caching enabled but poor financial results").
- **Source**: [Anthropic Prompt Caching docs](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) · [AI Checker Hub: 2026 caching guide](https://aicheckerhub.com/anthropic-prompt-caching-2026-cost-latency-guide)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

---

## Skills / Dynamic Tool Loading / Deferred Tools

### Finding 19: Anthropic Skills — progressive disclosure (3 levels), open standard (Dec 2025)
- **Detail**: Skill = folder containing `SKILL.md`. Three levels of context cost:
  1. **Metadata** (`name`, `description` in YAML frontmatter) — always preloaded into system prompt at session start; ~50 tokens/skill.
  2. **Core body** — loads only when Claude judges the skill applies to the current request.
  3. **Nested resources** (additional files in the skill dir) — load only when the body references them.
  Skills live in `~/.claude/skills/` (personal) or `.claude/skills/` (project). Spec released as open standard Dec 18, 2025 (`agentskills.io`); v1.0 H2 2026. Adopted by Codex CLI, Gemini CLI, Cursor, Aider, Cline, Windsurf, etc. (12+ tools).
- **Source**: [Anthropic Skills engineering blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · [Anthropic Skills docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) · [Claude Code Skills docs](https://code.claude.com/docs/en/skills) · [SwirlAI: Skills as System Design Pattern](https://www.newsletter.swirlai.com/p/agent-skills-progressive-disclosure) · [arXiv 2602.12430](https://arxiv.org/abs/2602.12430)
- **Confidence**: High
- **Skill-Impact**: **DIRECT** (the skill itself uses this).
- **PROPOSED EDIT**: Refactor the deep-research skill to split into nested files: `SKILL.md` (router), `research_strategy.md` (when to spawn N researchers), `synthesis.md` (final-report format), `templates/researcher_prompt.md`. Body of SKILL.md references these only when needed. Saves 80%+ of skill tokens for invocations that hit early-exit conditions.

### Finding 20: Tool Search Tool — `defer_loading: true` for 10,000-tool catalogs
- **Detail**: Two variants released Nov 2025: `tool_search_tool_regex_20251119` (Claude builds regex) and `tool_search_tool_bm25_20251119` (natural language). Tools marked `defer_loading: true` are excluded from the prefix; only the search tool + non-deferred tools appear initially. When the model needs more, it searches; the API returns 3-5 `tool_reference` blocks that auto-expand into full definitions inline. **Prompt cache preserved** because the prefix is untouched. Tool selection accuracy degrades past 30-50 tools without search; search keeps it high across 10K+. ~85% token reduction on multi-MCP setups. Limit: max 10K tools, max 200-char pattern.
- **Source**: [Tool Search Tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Speakeasy: 100x MCP reduction](https://www.speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2)
- **Confidence**: High (official docs)
- **Skill-Impact**: **DIRECT** (we observed it in this very session).
- **PROPOSED EDIT**: Researchers should be spawned with `defer_loading: true` on tools they don't need (e.g., a "scientific paper search" researcher doesn't need `mcp__claude_ai_Gmail__*`). The orchestrator should pass a *curated* tool whitelist as non-deferred per researcher role.

### Finding 21: Claude Code v2.1.69 — built-in tools deferred behind ToolSearch
- **Detail**: As of Claude Code v2.1.69, ALL built-in system tools (Bash, Read, Edit, Write, Glob, Grep, Agent, etc.) are deferred behind ToolSearch. Reduces "System tools" context from ~14-16K → ~968 tokens. Cost: 1 extra ToolSearch call (~200 tokens) when needed. Net positive unless searching for new tools every turn. GitHub issues track edge cases (PreToolUse hooks can hang, "Tool loaded" output leaking as user prompt, custom agents undiscoverable when Agent tool deferred).
- **Source**: [GitHub issue 31002: Built-in tools deferred](https://github.com/anthropics/claude-code/issues/31002) · [Finisky Garden: Deferred Tool Loading](https://finisky.github.io/en/claude-code-deferred-tools/)
- **Confidence**: High
- **Skill-Impact**: **DIRECT** (already affects this session).

### Finding 22: SkillSearch — proposed but not yet shipped
- **Detail**: Active feature request (GitHub issue 29711 / 42650): Skills currently load all `description` fields into every session's system prompt. With 50+ skills, this overhead is non-trivial. A SkillSearch mechanism — analogous to ToolSearch — would return matching skill names + descriptions on demand. **Not yet shipped** as of May 2026. Workaround: keep top-level skills lean; nest specialized variants as sub-files.
- **Source**: [GitHub issue 29711](https://github.com/anthropics/claude-code/issues/29711) · [GitHub issue 42650](https://github.com/anthropics/claude-code/issues/42650)
- **Confidence**: High (issues are open)
- **Skill-Impact**: INDIRECT (future-proofing).

### Finding 23: Code Mode — MCP via code execution, 98%+ token reduction
- **Detail**: Cloudflare + Anthropic pattern: instead of exposing MCP tools directly, expose them as a TypeScript/Python filesystem (`./servers/google-drive/getDocument.ts`). Model writes a short orchestration script; gateway executes in sandbox. **Anthropic Drive-to-Salesforce demo: 150K → 2K tokens (98.7% reduction).** Cloudflare 2,500-endpoint API: 1.17M → <1K tokens (99.9%). 30-40% latency improvement (skips agent loop round-trips). Key benefit: intermediate results never enter model context — only filtered/transformed final values do.
- **Source**: [Anthropic: Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) · [Speakeasy: 100x reduction](https://www.speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2) · [StackOne: MCP Code Mode](https://www.stackone.com/blog/mcp-code-mode-agent-context-architecture/)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (we're not gateway-implementing MCP, but this is the SOTA for large tool surfaces).

### Finding 24: Skills vs MCP — Armin Ronacher recommends agent-maintained Skills
- **Detail**: Armin's argument: Skills teach agents *how to use existing tools more effectively* (no new tool defs, minimal token cost, agent-controlled). MCP adds tool defs (~8K tokens upfront for typical multi-server setup, harder to maintain, cache-fragile). Recommendation: "ask the agent to write its own tools as a skill." Avoids MCP server description churn that invalidates caches.
- **Source**: [Armin Ronacher: Skills vs MCP](https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/)
- **Confidence**: Medium (opinion piece, but well-argued)
- **Skill-Impact**: INDIRECT.

---

## File-Based Scratchpads & Artifact Pattern

### Finding 25: Filesystem-as-memory is the dominant 2026 production pattern
- **Detail**: Microsoft SRE agent shifted from 100+ bespoke tools to a filesystem-based context engineering system: `read_file`, `grep`, `find`, shell — outperformed specialized tooling. Anthropic: "models understand files natively." Claude Code uses Markdown to maintain project structure summaries (`AGENTS.md`, `CLAUDE.md`); reads them first on session start to orient.
- **Source**: [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Agent Harness Engineering — Medium](https://medium.com/@adnanmasood/agent-harness-engineering-the-rise-of-the-ai-control-plane-938ead884b1d) · [DEV: Markdown Files Are All You Need](https://dev.to/imaginex/ai-agent-memory-management-when-markdown-files-are-all-you-need-5ekk)
- **Confidence**: High
- **Skill-Impact**: **DIRECT**.
- **PROPOSED EDIT**: Researchers already write `research_notes/N_topic.md` files. Make this stricter: orchestrator should *only* communicate with researchers via the file system after kickoff (write `task.md`, read `result.md`), so the orchestrator's context never receives the raw researcher trace.

### Finding 26: `plan.md` / `notes.md` / `todo.md` triad (Boris Tane / Cloudflare)
- **Detail**: Three-phase coding-agent workflow: **research** (deep code reading produces `research.md`), **planning** (produces approved `plan.md`), **implementation** (writes code, updates `todo.md` continually re-injecting goal). Rule: "don't let the agent write a single line of code until you've reviewed and approved a detailed written plan." `todo.md` solves the "forgot what I was doing" problem by re-injecting goals at end of context every turn.
- **Source**: [LogRocket: Context Engineering for IDEs](https://blog.logrocket.com/context-engineering-for-ides-agents-md-agent-skills/) · [Nyosegawa: Survey of Coding Agent Workflows](https://nyosegawa.com/en/posts/coding-agent-workflow-2026/) · [Advanced Context Engineering for Coding Agents](https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (we're not writing code, but the structure is portable).

### Finding 27: Ralph Loop — naive persistence via filesystem
- **Detail**: Ralph Loop (named after the Simpsons character) repeatedly feeds the *same prompt* to a fresh agent. Progress lives in files + git, not in the LLM context. Each iteration starts with a fresh window; agent re-orients by reading files. **Trades token efficiency for context-rot immunity.** Officially packaged as a Cursor plugin in 2026; Codex `/goal` is OpenAI's built-in equivalent. Useful for multi-hour autonomous runs.
- **Source**: [Ralph Wiggum AI Agents — Leanware](https://www.leanware.co/insights/ralph-wiggum-ai-coding) · [Knightli: What Ralph Is](https://www.knightli.com/en/2026/04/27/ralph-autonomous-agent-loop-claude-code-amp/) · [DEV: Year of the Ralph Loop](https://dev.to/alexandergekov/2026-the-year-of-the-ralph-loop-agent-1gkj)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

### Finding 28: Deep Agents (LangChain) — three compression techniques
- **Detail**: LangChain's Deep Agents:
  1. **Offload large tool results**: at 20K-token tool response, write to disk; substitute a file path + 10-line preview.
  2. **Offload large tool inputs**: at 85% context, truncate older file write/edit args (content is on disk anyway, replace with pointers).
  3. **Summarization** (last resort): LLM generates structured summary (`session intent`, `artifacts created`, `next steps`), replaces full history; originals preserved on disk for retrieval.
- **Source**: [LangChain: Context Management for Deep Agents](https://www.langchain.com/blog/context-management-for-deepagents) · [LangChain Docs: Deep Agents Context Engineering](https://docs.langchain.com/oss/python/deepagents/context-engineering)
- **Confidence**: High
- **Skill-Impact**: **DIRECT**.
- **PROPOSED EDIT**: Wrap WebFetch in a researcher-internal helper that writes the full fetched page to `files/research_session_<id>/raw/<urlhash>.md` and returns to the model only the top 10 lines + a token-budget-aware extract. Reduces researcher context bloat dramatically on long sessions.

---

## Worktrees / Sandboxes / Hooks

### Finding 29: Claude Code worktrees — parallel agent execution without conflict
- **Detail**: Sub-agents can run in their own git worktrees via `isolation: "worktree"` frontmatter. Each worktree is a real copy of the repo; edits in one don't touch another. Combined with `run_in_background: true`, agents can run tests/builds for hours without blocking. Production scale: 4-8 concurrent worktrees per developer. Known bug: agentId-prefix collisions can reuse stale branches (issue 51596).
- **Source**: [Claude Code Worktrees docs](https://code.claude.com/docs/en/worktrees) · [Claude Directory: Worktrees Guide](https://www.claudedirectory.org/blog/claude-code-worktrees-guide) · [GitHub issue 51596](https://github.com/anthropics/claude-code/issues/51596)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (we're file-based, not git-based, but the pattern of "isolated working dir per researcher" applies).

### Finding 30: Sandboxing — gVisor / Kata / microVM, not raw Docker
- **Detail**: Standard Docker containers share the host kernel and are not a strong enough boundary for AI agent sandboxes. 2026 production stacks use gVisor or Kata Containers (or microVMs via Firecracker). Each agent gets an isolated VPC, per-session resource limits, no cross-session leakage. Northflank, Modal, e2b are typical providers.
- **Source**: [Northflank: Sandbox AI Agents](https://northflank.com/blog/how-to-sandbox-ai-agents) · [Penligent: Sandboxes for Coding Agents](https://www.penligent.ai/hackinglabs/sandboxes-for-coding-agents/) · [Coding Agent Sandboxes 2026-05](https://gist.github.com/wincent/2752d8d97727577050c043e4ff9e386e)
- **Confidence**: High
- **Skill-Impact**: NONE (this skill runs in user's local shell — out of scope).

### Finding 31: Claude Code Hooks — 32+ events, 5 handler types (Feb 2026 HTTP added)
- **Detail**: Hooks intercept the agent loop at 32+ events: per-session (`SessionStart`, `SessionEnd`), per-turn (`UserPromptSubmit`, `Stop`, `StopFailure`), per-tool (`PreToolUse`, `PostToolUse`). Five handler types: command (shell), HTTP (POST, Feb 2026), MCP, LLM prompt, agent-spawn. PreToolUse can `allow` / `deny` / `ask` / `defer` and can mutate tool input before exec. PostToolUse can feedback but cannot undo. Communication: exit code 2 = stop; richer control via `hookSpecificOutput` JSON.
- **Source**: [Claude Code Hooks docs](https://code.claude.com/docs/en/hooks) · [Hooks Complete 2026 Reference](https://thepromptshelf.dev/blog/claude-code-hooks-complete-reference-2026/) · [Hooks: Policy as Code](https://ranjankumar.in/hooks-policy-as-code-agent-enforcement)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (skill-level; user-configurable).
- **PROPOSED EDIT (optional)**: The skill could *suggest* (not mandate) a `PostToolUse` hook on `WebFetch` that auto-archives the fetched content to `files/research_session_<id>/raw/` for citation verification.

### Finding 32: Hooks ⇄ Deferred Tools interaction bug
- **Detail**: PreToolUse hooks can cause agent hang after ToolSearch deferred tool loading (issue 33073). Implication: if our skill ships with custom hooks, they need to be tested against deferred-tool sessions. Generally, hook authors should expect ToolSearch is in the loop.
- **Source**: [GitHub issue 33073](https://github.com/anthropics/claude-code/issues/33073)
- **Confidence**: High (open bug)
- **Skill-Impact**: INDIRECT (caution).

---

## Checkpoint / Resume / Durable Execution

### Finding 33: LangGraph 1.2 (May 11, 2026) — durable graph execution
- **Detail**: Treats agent run as durable graph rather than Python function. Every node transition checkpointed via pluggable saver (Memory/SQLite/Postgres). Pause/resume, time-travel debugging, multi-instance horizontal scaling are first-class. Klarna uses it for stateful customer-service across millions of concurrent sessions; LinkedIn for multi-agent hiring flows.
- **Source**: [LangGraph Tutorial 2026](https://tech-insider.org/langgraph-tutorial-python-stateful-agent-13-steps-2026/) · [LangGraph vs Temporal 2026](https://agentmarketcap.ai/blog/2026/04/08/langgraph-vs-temporal-long-running-agent-workflows-2026)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

### Finding 34: Temporal — durable execution as table stakes
- **Detail**: Temporal raised $300M at $5B valuation (Feb 2026), 380% YoY revenue, 9.1T lifetime workflow actions. Every step automatically checkpointed; crashed workers resume exactly where they left off. **March 2026 GA: OpenAI Agents SDK ↔ Temporal Python SDK integration** — workflows spanning days/weeks with state checkpointed at every transition. Restate is the lighter-footprint alternative for edge/serverless.
- **Source**: [Temporal Replay 2026](https://thenewstack.io/temporal-replay-2026-news/) · [Durable Agent Execution 2026](https://agentmarketcap.ai/blog/2026/04/10/durable-agent-execution-production-temporal-modal-event-sourced) · [Diagrid: Checkpoints ≠ Durable Execution](https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows)
- **Confidence**: High
- **Skill-Impact**: NONE (skill runs in-session, not multi-day).

### Finding 35: Confucius Code Agent (CCA) — Meta/Harvard production scaffold, Jan 2026
- **Detail**: Open-sourced agent for industrial-scale repos and long sessions. SWE-Bench-Pro Resolve@1 = 59% (beats prior research + commercial). Three core mechanisms: **unified orchestrator with hierarchical working memory** (RAM-like tiers in code-aware structure), **persistent note-taking** (cross-session learning), **modular extension interface for tools**. Designed around three axes: Agent Experience, User Experience, Developer Experience.
- **Source**: [MarkTechPost: Confucius Code Agent](https://www.marktechpost.com/2026/01/09/meta-and-harvard-researchers-introduce-the-confucius-code-agent-cca-a-software-engineering-agent-that-can-operate-at-large-scale-codebases/) · [arXiv 2512.10398](https://arxiv.org/pdf/2512.10398)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

---

## Token-Efficient Tool Use

### Finding 36: Claude 4.x — token-efficient tool use ON by default
- **Detail**: All Claude 4 models support token-efficient tool use by default. Average -14% output tokens, up to -70%. Reduces latency too. No per-request config needed.
- **Source**: [Token-efficient tool use — Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/token-efficient-tool-use)
- **Confidence**: High
- **Skill-Impact**: NONE (handled by API).

### Finding 37: Dynamic toolsets — 96%+ input token reduction
- **Detail**: Dynamic toolset approaches reduce input tokens by ~96.7% (simple tasks) and ~91.2% (complex). Even with increased output tokens, total drops ~96% / ~90%. Mechanism: dramatically pruned tool surface per turn, surfacing only what's needed.
- **Source**: [Speakeasy: Reducing MCP token usage by 100x](https://www.speakeasy.com/blog/how-we-reduced-token-usage-by-100x-dynamic-toolsets-v2)
- **Confidence**: High
- **Skill-Impact**: INDIRECT (we already use ToolSearch).

### Finding 38: Cline 3 (May 2026) — rebuilt harness as standalone SDK
- **Detail**: On May 13, 2026, Cline released `@cline/sdk` — a ground-up rewrite of the agent runtime, separated from IDE lock-in. New: simplified loop, tightened context management, rewritten prompts, improved feedback loops/error handling, rethought tool surfacing. Context formula: `maxAllowedSize = max(window - 40_000, window * 0.8)`. New `new_task` tool: agent ends session, preloads next with structured context (summaries, file states, next steps) — basically scripted Ralph Loop.
- **Source**: [Cline: Rebuilt Harness](https://www.essamamdani.com/blog/cline-rebuilt-harness-why-it-matters) · [Cline SDK announcement](https://cline.ghost.io/introducing-cline-sdk-the-upgraded-agent-runtime/) · [Cline: Auto Compact](https://docs.cline.bot/features/auto-compact)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

---

## Attention-Sink / KV-Cache Management

### Finding 39: StreamingLLM + H2O patterns mainstream; DeepSeek MLA = endgame
- **Detail**: StreamingLLM retains "sink tokens" (first few tokens that absorb attention) + recent tokens, bounded KV cache. H2O uses heavy-hitter eviction by cumulative attention. Modern alternative: **DeepSeek's MLA (Multi-head Latent Attention)** compresses KV cache 7-14× via low-rank projection — described as "the architectural endgame for KV efficiency in 2026." Inference-stack concern, not directly user-controllable.
- **Source**: [MarkTechPost: Top 10 KV Cache Techniques 2026](https://www.marktechpost.com/2026/04/29/top-10-kv-cache-compression-techniques-for-llm-inference-reducing-memory-overhead-across-eviction-quantization-and-low-rank-methods/) · [DigitalApplied: KV Cache Optimization 2026](https://www.digitalapplied.com/blog/kv-cache-optimization-techniques-2026-engineering-guide)
- **Confidence**: High
- **Skill-Impact**: NONE.

### Finding 40: SideQuest — KV cache management for long-horizon agent reasoning
- **Detail**: 2026 paper (arXiv 2602.22603) addresses KV cache specifically for agent workloads with long reasoning chains. Model-driven (not static heuristic) eviction. Result quality at lower KV memory budgets than StreamingLLM/H2O for agentic loops.
- **Source**: [arXiv 2602.22603](https://arxiv.org/html/2602.22603v1)
- **Confidence**: Medium (preprint)
- **Skill-Impact**: NONE.

---

## HRM / TRM / Hierarchical Reasoning Architectures

### Finding 41: HRM (June 2025) — 27M param model beats SOTA on hard reasoning
- **Detail**: Hierarchical Reasoning Model (Guan Wang et al, June 2025): 27M params, two recurrent modules (high-level slow abstract planner, low-level fast detailed computer). Beats Claude 3.7 Sonnet, o3, DeepSeek-R1 on ARC-AGI, Sudoku-Extreme, Maze-Hard. Executes sequential reasoning in a *single forward pass* without explicit CoT supervision.
- **Source**: [arXiv 2506.21734](https://arxiv.org/abs/2506.21734) · [IBM: HRM explainer](https://www.ibm.com/think/topics/hierarchical-reasoning-model)
- **Confidence**: High
- **Skill-Impact**: NONE for *this* skill (we're not training; we orchestrate an LLM).

### Finding 42: TRM (Tiny Recursive Model, Oct 2025) — 7M params, 45% ARC-AGI-1
- **Detail**: 7M-param 2-layer single-network recursive reasoner. 45% ARC-AGI-1, 8% ARC-AGI-2 — beats most LLMs (DeepSeek R1, o3-mini, Gemini 2.5 Pro) with <0.01% of their params. Simpler than HRM, generalizes better.
- **Source**: [arXiv 2510.04871](https://arxiv.org/abs/2510.04871)
- **Confidence**: High
- **Skill-Impact**: NONE.

### Finding 43: HRM-Agent (late 2025) — HRM extended to RL navigation in dynamic mazes
- **Detail**: HRM trained via RL alone to navigate goals in dynamic uncertain environments. Demonstrates that hierarchical recurrent reasoning generalizes beyond static puzzles.
- **Source**: [arXiv 2510.22832](https://arxiv.org/html/2510.22832)
- **Confidence**: High
- **Skill-Impact**: NONE.

---

## Hooks, Streaming, & Misc

### Finding 44: Codex Hooks (OpenAI) — parity with Claude Code hooks
- **Detail**: OpenAI shipped equivalent hooks for Codex CLI. "Make the harness real" — same lifecycle interception model. Same shell exit-code semantics. Signals industry-wide convergence on the hook abstraction.
- **Source**: [Codex Hooks Make the Harness Real](https://blakecrosley.com/blog/codex-hooks-make-the-harness-real)
- **Confidence**: High
- **Skill-Impact**: INDIRECT.

### Finding 45: Staircase Streaming — 93% TTFT reduction for multi-agent
- **Detail**: arXiv 2510.05059: instead of waiting for complete intermediate outputs from prior agents, use partial outputs to begin generating final responses. TTFT reduced up to 93% while maintaining response quality. Useful for streaming research findings before all subagents finish.
- **Source**: [arXiv 2510.05059](https://arxiv.org/pdf/2510.05059)
- **Confidence**: Medium-High
- **Skill-Impact**: INDIRECT.

### Finding 46: Agent Skills v2 (Q1 2026) — workflow packages with executable scripts
- **Detail**: "Skills 2.0" upgrade: skills can now bundle executable scripts (not just docs). The runner exec's scripts deterministically without consuming context. Examples: PDF skill bundles a Python parser; spreadsheet skill bundles formula engine.
- **Source**: [Beginners in AI: Anthropic Skills Library 2026](https://beginnersinai.org/anthropic-skills-library/) · [ClaudeWorld: Anthropic Official Skills](https://claude-world.com/articles/anthropic-official-skills-complete-guide/)
- **Confidence**: Medium-High
- **Skill-Impact**: INDIRECT (could bundle helper scripts for citation verification, source dedup).

### Finding 47: AGENTS.md — sibling spec to SKILL.md for repo-level instructions
- **Detail**: AGENTS.md is the open-format file placed at project root telling AI assistants project conventions/constraints. Sibling to SKILL.md (which teaches new capabilities). Supported by Codex, Cursor, Windsurf, Kilo. The pair pattern: AGENTS.md for "where you are," SKILL.md for "what you can do."
- **Source**: [AGENTS.md spec](https://agents.md/) · [agensi: SKILL.md Spec](https://www.agensi.io/learn/skill-md-specification-open-standard) · [AGENTS.md and SKILL.md](https://chrisreddington.com/blog/building-your-agent-toolbox/)
- **Confidence**: High
- **Skill-Impact**: NONE for this skill.

---

## Cross-References

- **Compaction (Finding 7-9) + Pre-Rot Threshold (Finding 11) + Lost-in-the-Middle (Finding 15)**: Three converging arguments to compact at 40-60% utilization, not 80-100%. Affects orchestrator config directly.
- **Subagent isolation (Finding 12) + Return-channel design (Finding 13) + Filesystem-as-memory (Finding 25)**: The Anthropic blueprint (Finding 14) ties them together — communicate via files; only return structured summaries.
- **Skills progressive disclosure (Finding 19) + ToolSearch (Finding 20) + SkillSearch absent (Finding 22)**: All point at "load on demand" as the universal answer to context bloat. Skills handle docs; ToolSearch handles tool schemas; SkillSearch is the missing rung.
- **Prompt caching (Findings 16-18) + Stable tool surface (Finding 18)**: Multi-researcher cost optimization depends on byte-identical prefixes across spawned researchers.
- **Memory tool (Finding 6) + Shared memory across siblings (Finding 6 fine-print)**: One agent in a workspace can share memories with siblings — exact match for an orchestrator + N researchers needing a common scratchpad.
- **Anthropic deep research blueprint (Finding 14) is the canonical reference**: every architectural decision in our skill should be benchmarked against it.

---

## Skill Edits — Summary List

Concrete, prioritized changes to propose for the deep-research skill (all derived from DIRECT-impact findings above):

| # | Edit | Source Finding |
|---|------|----------------|
| 1 | Use `clear_tool_uses_20250919` on researcher subagents (`trigger=30_000`, `keep=4`, exclude `memory`) to drop WebFetch bodies once findings are extracted | F8 |
| 2 | Use `compact_20260112` on the orchestrator (`trigger=120_000` or 40% of window, custom instructions preserving research questions + findings + URLs) | F7, F11 |
| 3 | Enforce shared-memory directory `files/research_session_<id>/memory/` for orchestrator + researchers, writable by all siblings | F6 |
| 4 | Refactor `SKILL.md` into nested files (`research_strategy.md`, `synthesis.md`, `templates/researcher_prompt.md`) so non-active subskills don't load | F19 |
| 5 | Pass curated tool whitelist per researcher (`defer_loading: true` on tools the researcher doesn't need) | F20 |
| 6 | Force researchers to return strict structured summary JSON (`{findings:[{detail, source_url, confidence, skill_impact}], gaps:[...]}`), forbid raw trace | F13 |
| 7 | Add a dedicated Citation Agent stage after researchers, before synthesis — visits a sample of cited URLs to verify | F14 |
| 8 | Keep researcher system prompts byte-identical across instances so cache hits at 0.1× | F16 |
| 9 | Communicate orchestrator ↔ researcher *only via files* after kickoff (`task.md`, `result.md`) so orchestrator context stays clean | F25 |
| 10 | Wrap WebFetch in researcher-internal helper: write full page to `raw/<urlhash>.md`, return 10-line preview to model | F28 |

---

## Gaps & Open Questions

1. **SkillSearch shipping date**: SkillSearch (deferred Skill loading) is requested but unshipped. If/when it ships, our nested-file refactor (Edit #4) should re-evaluate. Track [issue 29711](https://github.com/anthropics/claude-code/issues/29711).
2. **Memory tool sharing semantics across siblings**: Cookbook says one agent can share memory with siblings in the same workspace, but the exact concurrency/locking model on Managed Agents isn't documented. Could subagents stomp each other's memory.md edits? Need to test or pin a write-lock convention (e.g., per-researcher subdirectories).
3. **PreToolUse hooks + ToolSearch interaction**: Open bug (issue 33073). If we ship hook recommendations, must validate they don't hang against deferred loading.
4. **Long-context degradation thresholds for current frontier models**: Sources cite ~256K as "rot zone" for 1M-window models, but no recent (May 2026) needle-in-haystack benchmark was found that's specific to Opus 4.7 / Sonnet 4.7. The 40% rule of thumb may be conservative or aggressive depending on the model.
5. **Cost of structured-summary discipline**: Forcing researchers to emit strict JSON-in-markdown costs them tokens (they have to write template scaffolding). Net savings vs. raw-trace dump are intuitive but not measured. Worth A/B testing.
6. **Citation Agent design**: Anthropic uses one; we don't yet have a sketch of its prompt + tool surface. Open question: should it WebFetch each URL or only a sample? What's the false-positive rate?
7. **ACE / agentic context engineering**: ACE's "evolving playbook" approach (F10) might be a natural fit for the orchestrator's planning prompt — i.e., let the orchestrator self-edit a `strategy.md` as it learns from each researcher's results. Out of scope for this pass but worth follow-up.
8. **TOON / structured-data formats**: A note in F25 mentions a 9,649-experiment study finding format choice (YAML/Markdown/JSON/TOON) matters for SQL/structured-data agents. Whether the same finding applies to research findings (lots of free-text + URLs) is unknown.
