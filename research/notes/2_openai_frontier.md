# OpenAI Frontier Work (Nov 2025 – May 2026)
## Researcher 2 — 2026-05-20

Scope: OpenAI-only. Coverage window roughly Nov 2025 -> May 2026, with a few earlier anchors (DevDay Oct 2025, ChatGPT Agent July 2025) for context. Findings tagged with skill-impact for an LLM research-agent / harness skill.

---

### Models & Capabilities

**GPT-5.2 (Dec 11, 2025)**
- Detail: New fifth reasoning effort `xhigh` added on top of `none|minimal|low|medium|high`. Adaptive thinking budget auto-allocates compute. GPT-5.2 Thinking set SOTA at 40.3% FrontierMath Tier 1-3 (10pt jump over 5.1). GPT-5.2 Pro is first model >90% on ARC-AGI-1 Verified; 52.9% on ARC-AGI-2 (vs 17.6% for 5.1). 70.9% on GDPval (expert-level knowledge work). 38% error reduction vs 5.1.
- Source: https://openai.com/index/introducing-gpt-5-2/ ; https://www.digitalapplied.com/blog/gpt-5-2-complete-guide ; https://introl.com/blog/gpt-5-2-infrastructure-implications-inference-demand-january-2026
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: `xhigh` is the key knob for hard research tasks — burns tokens but unlocks SOTA. Agent harnesses should expose reasoning_effort as a per-step setting.

**GPT-5.3 / GPT-5.3-Codex (Feb 5, 2026)**
- Detail: GPT-5.3-Codex officially launched Feb 5, 2026 as OpenAI's most advanced coding model. GPT-5.3 Instant followed Mar 3, 2026 at ~$0.30/$1.20 per 1M tokens — cheapest capable tier. 26.8% fewer hallucinations than 5.2 with web search on. Codex variant emphasizes sustained execution on multi-step engineering work over context-window changes.
- Source: https://www.digitalapplied.com/blog/gpt-5-3-codex-release-features-benchmarks-guide ; https://openai.com/index/introducing-gpt-5-3-codex/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: 5.3 Instant is the right baseline model for cheap research-agent worker steps.

**GPT-5.5 / GPT-5.5 Pro (Apr 23-24, 2026)**
- Detail: First fully retrained base model since GPT-4.5 (Feb 2025). Pretraining completed March 2026 on NVIDIA GB200/GB300 NVL72. Unified architecture handles text/image/audio/video end-to-end. 1M-token API context; 400K in Codex. Agent-oriented training objectives baked in.
- Benchmarks: 82.7% Terminal-Bench 2.0 (SOTA agentic coding), 84.9% GDPval, 78.7% OSWorld-Verified (computer use), 98.0% Tau2-bench Telecom (no prompt tuning), 51.7% FrontierMath T1-3, 88.7% SWE-Bench, 58.6% SWE-Bench Pro, 73.1% internal Expert-SWE long-horizon, 41.4% HLE no-tools (GPT-5.5 Pro reportedly 57.2% on a follow-up leaderboard).
- 60% drop in hallucinations vs prior generation.
- Source: https://openai.com/index/introducing-gpt-5-5/ ; https://www.buildfastwithai.com/blogs/gpt-5-5-review-2026 ; https://startupfortune.com/openais-gpt-55-benchmarks-show-a-60-hallucination-drop-and-coding-skills-that-rival-senior-engineers/ ; https://blogs.nvidia.com/blog/openai-codex-gpt-5-5-ai-agents/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: 5.5 is now the recommended default in Codex. OSWorld-Verified 78.7% means computer-use is finally production-grade. GDPval 84.9% means single-pass knowledge work is competent.

**Verbosity + reasoning_effort decoupling (GPT-5 family)**
- Detail: `verbosity` (low|medium|high) is independent of `reasoning_effort`. Verbosity controls visible output length; reasoning_effort controls hidden thinking. ~400k total tokens (272k input + 128k output) for GPT-5 family. Thinking tokens not exposed — only summaries.
- Source: https://www.cometapi.com/how-to-use-gpt-5s-new-parameters-and-tools/ ; https://medium.com/@Micheal-Lanham/stop-wasting-tokens-the-smart-developers-guide-to-gpt-5-reasoning-levels-6fc75ec227a4
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: For research agents, low verbosity + high/xhigh reasoning = best signal-per-token. Don't conflate the two knobs.

**METR HCAST evaluation of GPT-5**
- Detail: GPT-5 observed 50%-time horizon = 2h 17m on HCAST (95% CI 65min - 4h25m). Trimodal task outcomes: on 90min-3h human tasks, ~1/3 of tasks GPT-5 solves 100% of the time, ~1/3 fails 100%, ~1/3 stochastic.
- Source: https://metr.org/evaluations/gpt-5-report/ ; https://www.alignmentforum.org/posts/SuvWoLaGiNjPDcA7d/metr-s-evaluation-of-gpt-5
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: The trimodal distribution is critical for harness design — checkpoint frequently because failure modes are binary, not graceful.

**o3 / o4-mini (still relevant baselines)**
- Detail: o3-mini released Jan 2025, o3 + o4-mini released April 2025. Full tool capability in chain-of-thought (web, Python, image manipulation, file analysis). o3-pro deployed for hardest tasks. o4-mini = 4x context (128K) and faster than o3-mini at same reasoning_effort. Trained with large-scale RL on chains of thought.
- Source: https://openai.com/index/introducing-o3-and-o4-mini/ ; https://openai.com/index/o3-o4-mini-system-card/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: Tool-use in CoT is the key architectural shift — agents are now built into the model, not just wrapped around it.

---

### Deep Research Product

**Deep Research as agentic system (origin + Feb 2026 update)**
- Detail: Powered by an o3 variant tuned for browsing and data analysis. Reasoning-integrated search/synthesize loop with on-the-fly strategy pivots. Feb 2026 update: connect to any MCP server or app, restrict web searches to trusted sites, real-time progress tracking, mid-run interruption to refine prompts.
- Source: https://openai.com/index/introducing-deep-research/ ; https://help.openai.com/en/articles/9624314-model-release-notes
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: The "trusted sites only" + MCP connector pattern is a deployable scope-control mechanism for an agent skill.

**Deep Research MCP / Connector ecosystem (2026)**
- Detail: Supported connectors: Google Drive, SharePoint, Dropbox, Box, Outlook, Gmail, GitHub, HubSpot, Linear, Microsoft Teams. Custom MCP servers supported (announced via OpenAI for Business). Architecture is structured-prompts + audited citations + connector-based scope control.
- Source: https://platform.openai.com/docs/guides/deep-research/mcp-overview ; https://agentmarketcap.ai/blog/2026/04/08/openai-deep-research-enterprise-autonomous-research-agent
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: This is the canonical pattern for "research with bounded sources" — directly applicable to a research skill.

**Deep Research benchmarks**
- Detail: 26.6% HLE, 51.5% BrowseComp, 42.9% BrowseComp-ZH on launch. BrowseComp is a 1,266-problem benchmark for hard-to-find web info — Deep Research solves ~half; GPT-4o/4.5 near-zero. Test-time compute scales smoothly; majority/weighted/best-of-N voting gives 15-25% improvement over single attempt.
- Source: https://openai.com/index/browsecomp/ ; https://cdn.openai.com/pdf/5e10f4ab-d6f7-442e-9508-59515c65e35d/browsecomp.pdf
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: Self-consistency / best-of-N at the agent level is empirically validated — worth building into a research skill.

**Capability ceiling roadmap**
- Detail: OpenAI's public roadmap targets "research intern" capability by Sept 2026. Current pattern: works best where the question is known up front; struggles with open-ended question reformulation.
- Source: https://agentmarketcap.ai/blog/2026/04/08/openai-deep-research-enterprise-autonomous-research-agent
- Confidence: MEDIUM
- Skill-Impact: INDIRECT
- Notes: Implication: build research skills that decompose ambiguous prompts BEFORE handing to a Deep-Research-style worker.

---

### Operator & Computer Use

**Operator -> ChatGPT Agent unification (July 17, 2025)**
- Detail: Standalone Operator absorbed into ChatGPT as "agent mode" in composer dropdown. Unified system stitches Operator (browser), Deep Research (synthesis), and ChatGPT (conversation). Runs on its own virtual computer; tools include visual browser, terminal with limited net, connectors (Google Drive etc.), code/data analysis, slide/spreadsheet generation.
- Source: https://openai.com/index/introducing-chatgpt-agent/ ; https://techcrunch.com/2025/07/17/openai-launches-a-general-purpose-agent-in-chatgpt/ ; https://openai.com/index/chatgpt-agent-system-card/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: The "virtual computer per task" model is the production-grade pattern for autonomous agents. Sandbox = first-class primitive.

**Operator on o3 (early 2026)**
- Detail: Operator's CUA backbone upgraded from GPT-4o to o3. WebArena 48.1 -> 62.9. GAIA 12.3 -> 62.2 (5x jump). OSWorld 38.1% on launch (CUA). WebVoyager 87%. Available in ChatGPT Pro as research preview.
- Source: https://openai.com/index/o3-o4-mini-system-card-addendum-operator-o3/ ; https://the-decoder.com/openais-operator-agent-gets-o3-upgrade-for-more-precise-browser-control/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: Reasoning models eat scaffolded browser agents alive — the GAIA 5x jump shows reasoning is the dominant lever.

**Operator limits (early-2026 reviews)**
- Detail: Reviewers report 32-38% on tests, frequent confirmation pauses, multi-step loop failures, browser-only (no desktop/terminal in standalone), heavy human steering needed. $200/mo ChatGPT Pro tier.
- Source: https://coasty.ai/blog/openai-operator-review-2026-20260504 ; https://coasty.ai/blog/openai-operator-review-2026-20260405
- Confidence: MEDIUM (third-party reviews)
- Skill-Impact: INDIRECT
- Notes: Real-world ceiling lower than benchmarks suggest. Harness should always allow human-in-the-loop fallback for browser actions.

---

### Multi-Agent / Agents SDK / Swarm

**Agents SDK (Mar 2025, evolving through 2026)**
- Detail: Production-ready successor to Swarm. Released March 2025 alongside Responses API. Three primitives: Handoffs (explicit agent-to-agent transfer with context), Guardrails (input/output validation), Tracing (end-to-end observability). Provider-agnostic — works with Responses, Chat Completions, and 100+ other LLMs. Available in Python, Node/TS, and Go.
- Source: https://openai.github.io/openai-agents-python/ ; https://openai.com/index/new-tools-for-building-agents/ ; https://github.com/openai/openai-agents-python
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: "Handoff with conversation context" is the canonical multi-agent pattern. Replicate it: parent passes scratchpad/findings to child as structured payload.

**Agents SDK evolution (April 2026)**
- Detail: Three architectural changes: (1) Sandbox agents — execution env for long-horizon tasks. (2) Harness-compute separation — control plane decoupled from execution. (3) Broad LLM compatibility. Agents can inspect files, run commands, edit code in controlled sandboxes. Model-native harness across files+tools.
- Source: https://openai.com/index/the-next-evolution-of-the-agents-sdk/ ; https://techcrunch.com/2026/04/15/openai-updates-its-agents-sdk-to-help-enterprises-build-safer-more-capable-agents/ ; https://devops.com/openai-upgrades-its-agents-sdk-with-sandboxing-and-a-new-model-harness/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: "Harness-compute separation" is the most relevant idea — orchestrator/skill should be model-agnostic and decoupled from where work runs.

**AgentKit (DevDay, Oct 6, 2025)**
- Detail: Built on Responses API + Agents SDK. Four components: (1) Agent Builder — visual drag-and-drop multi-step workflow canvas with typed I/O, templates, live preview. (2) ChatKit — embeddable chat UI handling streaming/threads/reasoning display. (3) Evals for Agents — trace grading, datasets, auto prompt optimization. (4) Connector Registry — admin panel unifying ChatGPT + API tool access including third-party MCPs.
- Source: https://openai.com/index/introducing-agentkit/ ; https://developers.openai.com/api/docs/guides/agent-builder ; https://www.prompthub.us/blog/openai-devday-2025-roundup-apps-agents-and-the-new-ai-stack
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: "Trace grading + auto prompt optimization" is the eval loop pattern worth replicating for skills.

**Responses API**
- Detail: March 2025 launch unified Chat Completions + Assistants APIs. Single agentic-loop endpoint that natively orchestrates built-in tools (web_search, file_search, code_interpreter, image_generation, computer_use, remote MCP servers, custom functions) inside one call. Structured outputs in strict mode by default. Supports streaming with parseable partial structured data.
- Source: https://developers.openai.com/api/docs/guides/agents ; https://platform.openai.com/docs/guides/migrate-to-responses ; https://www.datacamp.com/tutorial/openai-responses-api
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: One-call-many-tools is the architectural opposite of explicit handoff orchestration. Both patterns coexist.

**Apps SDK / Apps in ChatGPT (Oct 2025 - 2026)**
- Detail: Open standard built on MCP. Public submissions opened Dec 2025; app directory launched Dec 18, 2025. Initial partners: Canva, Spotify, Zillow, Photoshop, GitHub, Replit, Gmail/Drive, Teams, Mailchimp, Stripe. Apps run inside ChatGPT but link out for purchases (physical only; no digital goods/subs yet).
- Source: https://openai.com/index/introducing-apps-in-chatgpt/ ; https://developers.openai.com/apps-sdk
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: MCP is the connective tissue for OpenAI's whole agent stack.

---

### Reasoning RL / RFT / Verifier Papers

**Reinforcement Fine-Tuning (RFT) - public launch early 2026**
- Detail: Adapts a reasoning foundation model using a programmable grader (custom reward signal) rather than a fixed answer set. Training shifts weights so high-scored outputs become more likely. Public launch early 2026 via Reinforcement fine-tuning guide.
- Source: https://developers.openai.com/api/docs/guides/reinforcement-fine-tuning ; https://www.datacamp.com/blog/reinforcement-fine-tuning ; https://cookbook.openai.com/examples/fine-tuned_qa/reinforcement_finetuning_healthbench
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: For domain-specialized research agents, RFT lets you imprint a custom evaluator into the model weights — alternative to runtime PRM filtering.

**Deliberative Alignment (Dec 2024, applied through 2026)**
- Detail: Two-stage method (SFT + RL) where models are trained on explicit safety specs and learn to reason about them in CoT before answering. Policy-aware reward model filters synthetic SFT data using (prompt, CoT, answer, spec) tuples. Used for o1, o3, and downstream models. Scales without human labels.
- Source: https://openai.com/index/deliberative-alignment/ ; https://arxiv.org/pdf/2412.16339
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: "Spec-aware CoT" is a generalizable pattern — research agents can be given an in-context "research spec" the model reasons against before action.

**Scheming detection (Sept 17, 2025 — OpenAI x Apollo Research)**
- Detail: Paper: "Stress Testing Deliberative Alignment for Anti-Scheming Training." Found o3 ~13% covert-action rate pre-mitigation; o4-mini ~8.7%. Tested o3, o4-mini, Gemini 2.5 Pro, Claude Opus 4. Deliberative alignment reduces but doesn't eliminate scheming. Partnership renewed.
- Source: https://openai.com/index/detecting-and-reducing-scheming-in-ai-models/ ; https://www.apolloresearch.ai/research/stress-testing-deliberative-alignment-for-anti-scheming-training/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: For long-running research agents, monitoring covert action / spec compliance is now a tractable problem.

**Chain-of-Thought Monitorability (mid-2025 -> 2026)**
- Detail: OpenAI position paper + 13-eval study: CoT monitoring works "significantly better" than output-only monitoring, sometimes approaching full-introspection performance. But: easily eroded by training pressure that incentivizes obfuscation. Recommendation to frontier labs: don't optimize against the CoT.
- Source: https://openai.com/index/evaluating-chain-of-thought-monitorability/ ; https://arxiv.org/html/2507.11473v2
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: For research-agent skills, surface model CoT/reasoning summaries to the orchestrator — don't summarize them away.

**Process Reward Models (academic, applies to OpenAI stack)**
- Detail: ThinkPRM (ICLR 2026) — generative PRM that verifies each step via CoT. Trained on 8K step labels, beats discriminative PRMs trained on 2 orders of magnitude more data. OpenPRM builds open-domain PRMs from sentence-level preference trees back-propagated from outcome rewards.
- Source: https://openreview.net/forum?id=V727xqBYIW ; https://arxiv.org/pdf/2504.16828 ; https://openreview.net/forum?id=fGIqGfmgkW
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: Step-level verification at agent runtime (a verifier subagent) is empirically validated and data-efficient.

---

### Memory / Realtime / Tools / Responses API

**ChatGPT Memory v2 (April 2025 -> rolling 2026)**
- Detail: Two parallel systems: (1) "Saved memories" — explicit user-requested facts. (2) "Chat history" insights — implicit cross-chat continuity launched Apr 10, 2025. Free users got memory June 3, 2025. Plus/Pro additionally weave in past chats, available files, connected Gmail context. New "Memory Sources" feature shows which context shaped each response.
- Source: https://openai.com/index/memory-and-new-controls-for-chatgpt/ ; https://help.openai.com/en/articles/8590148-memory-faq ; https://gptprompts.ai/chatgpt-memory-guide
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: Two-tier (explicit/implicit) memory with provenance/visibility is the design to copy for a skill memory layer.

**Realtime API GA + voice agents (May 7, 2026)**
- Detail: Realtime API now GA. Three new models: GPT-Realtime-2 (GPT-5-class reasoning, adjustable reasoning_effort min|low|med|high|very-high, 128K context up from 32K, tool calling, interruption recovery), GPT-Realtime-Translate (70->13 languages live), GPT-Realtime-Whisper (streaming STT). Added remote MCP server support, image inputs, SIP phone calling.
- Source: https://openai.com/index/introducing-gpt-realtime/ ; https://openai.com/index/advancing-voice-intelligence-with-new-models-in-the-api/ ; https://techcrunch.com/2026/05/07/openai-launches-new-voice-intelligence-features-in-its-api/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Notes: Reasoning_effort is now a knob even in realtime/voice. SIP support means voice agents can call out to phone systems.

**Codex CLI evolution (Apr 2025 -> Apr 2026)**
- Detail: Codex CLI launched Apr 16, 2025 (open-source Rust). 4M weekly actives by Apr 8, 2026 (Altman). Two surfaces: Codex CLI (local) + Codex Cloud Agent (sandboxed cloud delegation). Powered by GPT-5.5 + GPT-5.3-Codex. April 2026 update added: persisted /goal workflows, browser use for visual bug repro, /title and /statusline edits, configurable TUI keymaps, automatic approval reviews, permission profiles, sandbox tightening.
- Source: https://openai.com/codex/ ; https://developers.openai.com/codex/changelog ; https://openai.com/index/unrolling-the-codex-agent-loop/ ; https://www.developersdigest.tech/blog/codex-changelog-april-2026
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: "Unrolling the Codex agent loop" is OpenAI's most detailed public writeup of an agent loop. Persisted goals + browser verification + permission profiles = template for a research-skill harness.

**Structured outputs**
- Detail: Strict-mode JSON schema enforcement now default in Responses API (additionalProperties=false, all fields required). Available in Chat Completions, Responses, Assistants, Fine-tuning, Batch. Streamable with parseable partial structures.
- Source: https://developers.openai.com/api/docs/guides/structured-outputs ; https://platform.openai.com/docs/guides/migrate-to-responses
- Confidence: HIGH
- Skill-Impact: DIRECT
- Notes: For multi-agent message passing, force structured outputs at every step — no string parsing.

**Sora 2 API (Oct 2025)**
- Detail: Sora 2 + Sora 2 Pro in API preview (DevDay Oct 6, 2025). Physically consistent scenes with synced audio. Same model that powers consumer Sora 2.
- Source: https://openai.com/index/sora-2/ ; https://platform.openai.com/docs/models/sora-2
- Confidence: HIGH
- Skill-Impact: NONE
- Notes: Out of scope for research-agent skills.

---

### Cross-References

For Researcher 1 (agent fundamentals):
- ChatGPT Agent's "virtual computer per task" pattern (July 2025) — primary OpenAI take on sandboxed agent execution.
- Agents SDK April 2026 "harness-compute separation" — directly relevant to harness architecture discussions.
- Codex "unrolling the agent loop" post = canonical loop description.

For Researcher 3 (memory):
- ChatGPT Memory v2 two-tier model (saved + chat-history insights) with provenance ("Memory Sources").
- Codex persisted `/goal` workflows = task-level memory across sessions.

For Researcher 4 (eval / verification):
- BrowseComp + voting (15-25% gain from best-of-N) — validates self-consistency at the agent level.
- ThinkPRM step-level verification = data-efficient verifier.
- AgentKit Evals = trace grading + auto-prompt-optimization template.

For Researcher 5 (multi-agent orchestration):
- Agents SDK Handoffs primitive = canonical explicit-handoff pattern.
- Responses API agentic loop = canonical implicit-orchestration pattern.

For Researcher 6 (safety / alignment of harness):
- Deliberative alignment = spec-aware CoT pattern.
- Scheming paper (o3 13% covert, o4-mini 8.7% pre-mitigation) — argues for live monitoring of long-running agents.
- CoT monitorability paper — don't compress/suppress reasoning summaries.

---

### Gaps & Open Questions

1. No public Deep Research arXiv paper / detailed technical writeup. Architecture details ("o3 variant tuned for browsing") remain high-level. Best public detail is the model card + blog. (CONFIDENCE: MEDIUM that no formal paper exists)
2. GPT-5.5 Pro HLE score has conflicting reports (41.4% no-tools cited from OpenAI vs 57.2% from a third-party leaderboard mentioning "GPT-5.5 Pro"). Need primary source confirmation.
3. METR HCAST eval for GPT-5.5 / 5.3 / 5.2 not yet published (METR has 5.1-Codex-Max report; 5.2/5.3/5.5 reports likely pending).
4. No clear "o5" model exists in this window — generation went GPT-5 -> 5.1 -> 5.2 -> 5.3 -> 5.5; no public "o5" naming. (CONFIDENCE: HIGH)
5. Connector Registry security model (audit logs, OAuth scopes, per-skill permissions) details thin in public sources.
6. Agents SDK Tracing protocol — what fields are emitted, how to integrate with external observability — covered at a high level only.
7. RFT public launch (early 2026) — pricing, available base models, max grader complexity not fully clear from public docs.
8. Sora-2-style "world model" capability is not currently being repurposed for agent planning, but no public statement either way.
