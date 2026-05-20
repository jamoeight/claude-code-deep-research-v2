# Open-Source Agent Frameworks & Emerging Patterns (Nov 2025 – May 2026)
## Researcher 8 — 2026-05-20

Scope: tooling, frameworks, OSS implementations of agentic patterns, and which open patterns are gaining traction. Excludes pure lab products (Claude/GPT/Gemini), pure architecture papers, and pure context-engineering tricks.

---

### Coding-Agent Harnesses

**OpenHands (formerly OpenDevin) is the open SOTA harness.**
- Detail: OpenHands + CodeAct v3 hits ~68.4% on SWE-Bench Verified with Claude Opus 4.6; 77.6% with internal harness tuning. Now backed by $18.8M Series A, used by AMD/Apple/Google/Amazon/Netflix/NVIDIA. 74k+ GitHub stars. The November 2025 paper "The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents" (arxiv 2511.03690, MLSys 2026 Oral) is the definitive reference architecture.
- Source: https://www.openhands.dev/blog/sota-on-swe-bench-verified-with-inference-time-scaling-and-critic-model ; https://arxiv.org/abs/2511.03690
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Adopt OpenHands V1's **event-sourced state model with deterministic replay** + immutable agent config + typed tool system with MCP integration. Workspace abstraction lets the same agent run locally or remotely with minimal code changes — exactly the dual-mode pattern our skill needs.

**OpenHands' CodeAct loop + critic model is the canonical "agent + verifier" pattern.**
- Detail: CodeAct is an observe-think-act loop where actions are Python/shell snippets. Recent v3 adds a critic model (best-of-N sampling) that produces verification feedback rendered inline in the UI. The runtime separates the controller process (Python server, LiteLLM abstraction) from the sandbox (Docker container per task).
- Source: https://www.researchgate.net/figure/Overview-of-OpenHands-default-CodeAct-Browsing-agent-architecture-the-baseline-agent_fig2_387184139
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Use a separate critic/verifier model on subagent outputs before merging — even simple BoN-2 with a small model gives measurable lift.

**SWE-agent v1 (Princeton/Stanford) — the research reference.**
- Detail: Minimal, text-first, canonical reference for Agent-Computer Interfaces (ACI). Scores 43.2% on SWE-Bench Verified with Claude Sonnet 4.5. The lineage shows how a clean ACI design enables agent transferability across models.
- Source: https://www.codesota.com/agentic/openhands-vs-swe-agent
- Confidence: HIGH
- Skill-Impact: INDIRECT (architecture inspiration)
- Borrow: Keep tool surface minimal and text-first; complex UIs add failure modes.

**Cline / Roo Code / Continue dominate VS Code OSS agent extensions.**
- Detail: Cline (Apache 2.0, 61.2k stars, 5M+ installs, v3.81 in May 2026) runs as VS Code sidebar + JetBrains + CLI. Roo Code is a fork of Cline that added Modes (Architect/Act/Ask) and multi-agent workflows. Continue.dev complements them with fast inline completion. All three are now distributed as CLI assistants too.
- Source: https://github.com/cline/cline ; https://www.qodo.ai/blog/roo-code-vs-cline/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: The "Modes" pattern (Architect=plan, Act=execute, Ask=Q&A) is a clean separation that maps to our skill's plan/execute split.

**OpenCode (95k stars) is the breakout open Claude Code competitor.**
- Detail: Emerged as the default OSS alternative to Claude Code for users who want model flexibility (any model via OpenRouter, no Anthropic lock-in).
- Source: https://openalternative.co/alternatives/devin
- Confidence: MEDIUM
- Skill-Impact: NONE

**Aider remains the git-native pioneer.**
- Detail: 39k stars, 4.1M installs, processes 15B tokens/week. Strength: every edit is a commit, every session is a branch. Now used as a baseline in benchmarks rather than as SOTA.
- Source: https://www.morphllm.com/best-ai-coding-agents-2026
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: Auto-commit-per-edit gives free checkpoint/rollback — relevant for our checkpoint/resume work.

---

### General Multi-Agent Frameworks

**LangChain 1.0 + LangGraph 1.0 (October 22, 2025) is the de facto open default.**
- Detail: First stable major release in durable agent frameworks. Stability commitment: no breaking changes until 2.0. New `create_agent` entry point sits on LangGraph runtime; customization via **middleware array** instead of subclassing. Middleware hooks: `before_agent`, `before_model`, `wrap_model_call`, `wrap_tool_call`, `after_model`, `after_agent` — built-in middleware for HITL, summarization, PII redaction. Provider integrations moved out-of-tree into `@langchain/<provider>` packages.
- Source: https://blog.langchain.com/langchain-langgraph-1dot0/ ; https://changelog.langchain.com/announcements/langchain-1-0-now-generally-available
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: **Middleware-array pattern** is a powerful abstraction — hooks instead of subclassing lets you compose context-engineering tricks without rewriting the agent loop.

**LangGraph's durable execution is the standard.**
- Detail: Agent state persists automatically — survives server restart, picks up exactly where it left off. Workflows can be saved/resumed without custom DB logic. Adopted by Uber, LinkedIn, Klarna. Graph-based execution with typed state.
- Source: https://docs.langchain.com/oss/python/langgraph/overview
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Treat durable state as a first-class primitive, not bolted-on.

**LangChain `deepagents` library (and Deep Agents v0.5) — the "batteries-included" harness pattern.**
- Detail: Open-source harness for long-running tasks. Provides: planning (`write_todos`), virtual filesystem, sub-agent spawning (`task`), context compression, **skill loading**. Sub-agents get isolated context windows / tools / configs. Skill-loading explicitly inspired by Claude Skills.
- Source: https://github.com/langchain-ai/deepagents ; https://blog.langchain.com/deep-agents-v0-5/
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: This is the closest OSS analog to our skill. Steal: `write_todos` as planning primitive, virtual FS for cross-subagent comms, `task` tool for sub-agent spawning.

**CrewAI v1.14.5 (May 18, 2026) — role-based orchestration.**
- Detail: Two primitives: **Crews** (autonomy + collaborative intelligence) and **Flows** (granular event-driven control, single LLM calls). Recent adds: checkpoint forking with lineage tracking, reasoning-token + cache-creation token tracking, Daytona sandbox tools, security patches.
- Source: https://docs.crewai.com/en/changelog ; https://releasebot.io/updates/crewai
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: **Checkpoint forking with lineage tracking** is the right mental model for parallel hypothesis exploration.

**AutoGen → Microsoft Agent Framework 1.0 (April 3, 2026) — major consolidation.**
- Detail: AutoGen (now v0.7.x maintenance) folded into MAF along with Semantic Kernel. MAF 1.0 ships .NET + Python with session state, type safety, middleware, telemetry, **graph-based workflows**, and multi-agent orchestration patterns (sequential, concurrent, **handoff**, **group chat**, **Magentic-One**). Magentic-One: lead Orchestrator plans/tracks/replans, delegates to specialized agents.
- Source: https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/ ; https://visualstudiomagazine.com/articles/2026/04/06/microsoft-ships-production-ready-agent-framework-1-0-for-net-and-python.aspx
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: The named patterns library (handoff/group-chat/Magentic-One) is worth cataloging in our skill docs.

**MetaGPT 1.0 + MGX (Feb 2026) — Foundation Agent.**
- Detail: Released MGX (MetaGPT X), "the world's first AI agent development team". Version 1.0 incorporates Foundation Agent tech; the OG SOPs-for-software-company framing remains.
- Source: https://www.xpay.sh/resources/agentic-frameworks/metagpt/
- Confidence: MEDIUM
- Skill-Impact: NONE

**Smolagents (HuggingFace, 26k+ stars) — code-first minimalist.**
- Detail: ~1000 LOC core, 207 contributors. CodeAgent writes actions as Python; ToolCallingAgent uses tool-calling APIs. Multi-agent hierarchies, vision support. Sandbox backends: **Blaxel, E2B, Modal, Docker, or Pyodide+Deno WASM**. CodeAgent + GPT-4o scored 44.2% on GAIA without fine-tuning, beating prior multi-agent best at the time.
- Source: https://github.com/huggingface/smolagents ; https://huggingface.co/blog/smolagents
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: "Code as actions" outperforms JSON tool calls on GAIA — worth considering for orchestrator agents.

**Agno (formerly Phidata) — 39k stars, agent-swarm focus.**
- Detail: Stateless scaling via AgentOS runtime. User/session memory + RAG knowledge bases stored in your DB (data ownership). Positioned for high-throughput swarms.
- Source: https://www.xpay.sh/resources/agentic-frameworks/compare/phidata-vs-pydantic-ai/
- Confidence: MEDIUM
- Skill-Impact: NONE

**Pydantic AI (16.5k stars) — type-safe Python-native.**
- Detail: Schema validation + automatic self-correction when LLM outputs don't match expected structure (re-prompts the model with the validation error).
- Source: https://github.com/pydantic/pydantic-ai
- Confidence: MEDIUM
- Skill-Impact: INDIRECT
- Borrow: Auto-retry-with-validation-error is a free reliability win for structured outputs.

**DSPy (Stanford, ~23k stars) — prompts as compiled artifacts.**
- Detail: Signatures + modules; DSPy learns the prompts that make them work. Built-in ReAct + agent loops. Increasingly production-viable.
- Source: https://diamantai.substack.com/p/how-to-choose-your-ai-agent-framework
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

**AgentScope (Alibaba, OSS) — explicit message passing + drag-and-drop UI.**
- Detail: Zero-code drag-and-drop UI, built-in tool + MCP support, distributed execution, monitoring, automatic prompt tuning, fault tolerance. Added DB support + memory compression in the memory module (Jan 2026).
- Source: https://github.com/agentscope-ai/agentscope
- Confidence: MEDIUM
- Skill-Impact: NONE

**OpenAgents (Python) — first framework with native MCP + A2A.**
- Detail: As of 2026, the only framework with native support for both MCP and A2A protocols. Purpose-built for interoperable agent networks.
- Source: https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared
- Confidence: MEDIUM
- Skill-Impact: NONE

**ChatDev 2.0 (DevAll, Jan 7 2026) — zero-code multi-agent platform.**
- Detail: Companion paper "Multi-Agent Collaboration via Evolving Orchestration" at NeurIPS 2025; "puppeteer branch" carries the new orchestration approach.
- Source: https://github.com/OpenBMB/ChatDev
- Confidence: MEDIUM
- Skill-Impact: NONE

**Claude Agent SDK** (renamed from Claude Code SDK, Anthropic) — Python + TypeScript.
- Detail: Same harness powering Claude Code, exposed as a programmable SDK. Xcode 26.3 ships native integration. From June 15, 2026, Agent SDK + `claude -p` usage on subscription plans draws from a separate monthly credit pool (Pro $20, Max5x $100, Max20x $200). OpenClaw / 3rd-party harnesses re-enabled with this credit model.
- Source: https://code.claude.com/docs/en/agent-sdk/overview ; https://github.com/anthropics/claude-agent-sdk-python
- Confidence: HIGH
- Skill-Impact: DIRECT (it powers Claude Code, which our skill targets)

---

### Open Multi-Agent Research / Deep-Research Clones

**LangChain `open_deep_research` — supervisor-researcher reference impl.**
- Detail: Open-source deep research agent across many model providers, search tools, MCP servers. Ranks #6 on Deep Research Bench (RACE 0.4943 with GPT-5). Structured workflow: research → summarization → compression → report generation. Includes legacy plan-and-execute (HITL) and multi-agent supervisor-researcher variants.
- Source: https://github.com/langchain-ai/open_deep_research ; https://docs.langchain.com/oss/python/deepagents/deep-research
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: The **supervisor-researcher architecture separates parallel info gathering from coherent report synthesis** — exact pattern Anthropic's multi-agent research system uses. Mirror this split in our skill.

**HuggingFace `open_deep_research` (smolagents example) — code-acting researcher.**
- Detail: Smolagents-based implementation, used as a benchmark baseline. CodeAgent variant runs ~55% on GAIA, was leapfrogged by OWL.
- Source: https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research
- Confidence: HIGH
- Skill-Impact: INDIRECT

**OWL (CAMEL-AI) — #1 OSS on GAIA at 69.09%.**
- Detail: "Optimized Workforce Learning". Hierarchical multi-agent: domain-agnostic **Planner** for decomposition → **Coordinator** for subtask mgmt → specialized **Workers** with domain-specific tools. Cross-domain transferability via training methodology (not just prompting). WORKFORCE variant: 69.70% open SOTA, beats OpenAI Deep Research by 2.34%.
- Source: https://github.com/camel-ai/owl ; https://arxiv.org/pdf/2505.23885
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Planner / Coordinator / Worker is a clean three-tier hierarchy. Workforce *training* (vs pure prompting) suggests fine-tuning specialized worker models is worth the cost.

**Cognitive Kernel-Pro (Tencent AI Lab, arXiv 2508.00414).**
- Detail: Multi-module hierarchical: main agent for decomposition + integration; sub-agents for web/file/code/general reasoning. An 8B-parameter open model surpasses WebDancer and WebSailor. Open code at github.com/Tencent/CognitiveKernel-Pro.
- Source: https://arxiv.org/pdf/2508.00414 ; https://huggingface.co/papers/2508.00414
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: The four-domain query/trajectory/verifiable-answer split (web/file/code/reasoning) is a clean taxonomy for trajectory data — useful if we ever fine-tune our own orchestrator.

**GPT-Researcher (Assaf Elovic).**
- Detail: Pioneer of the planner → parallel search → synthesize report pattern. May 2026 updates: LangSmith tracing, auto-generated Gemini illustrations, a `.claude/skills/` directory with a 1,500+ line SKILL.md teaching Claude Code to extend it, **Deep Research recursive workflow** (tree-like exploration, depth + breadth).
- Source: https://github.com/assafelovic/gpt-researcher
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: GPT-Researcher's "include a SKILL.md teaching Claude Code to extend the project" is itself a pattern we should replicate.

**AutoAgent / Auto-Deep-Research (HKUDS).**
- Detail: AutoAgent is fully-automated agent construction from natural language alone, no manual coding. Auto-Deep-Research is an open Deep Research alternative built on it ($200/month commercial → BYO API keys). Matches Deep Research using Claude 3.5 rather than o3.
- Source: https://github.com/HKUDS/AutoAgent ; https://github.com/HKUDS/Auto-Deep-Research
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

**STORM (Stanford) — Wikipedia-style synthesis via simulated expert panels.**
- Detail: Simulates a panel of expert interviewers asking from different perspectives, synthesizes into structured article. Still the canonical academic reference for multi-perspective questioning.
- Source: https://awesomeagents.ai/tools/best-ai-deep-research-tools-2026/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: Multi-perspective questioning (simulate different expert viewpoints before synthesis) is an under-used pattern in our skill.

**OpenManus / OpenManus-RL — clone of Manus AI.**
- Detail: MetaGPT team's invitation-free replica of Monica's Manus. Modular, multi-model, browser+code+file tooling.
- Source: https://github.com/henryalps/OpenManus
- Confidence: MEDIUM
- Skill-Impact: NONE

**DeepAgent (RUC-NLPIR, WWW '26 Oral).**
- Detail: End-to-end deep reasoning agent with **brain-inspired memory folding mechanism**. Autonomously discovers + uses 16,000+ RapidAPIs.
- Source: https://github.com/RUC-NLPIR/DeepAgent
- Confidence: MEDIUM
- Skill-Impact: INDIRECT
- Borrow: "Memory folding" is a memory-compression pattern worth investigating for long-running agents.

**Letta (formerly MemGPT, UC Berkeley) — stateful agent runtime.**
- Detail: Implements MemGPT's OS-inspired core/archival/recall memory hierarchy. Agents run *inside* Letta. Letta Code app launched April 6, 2026 for personalized agents that learn over time. Better default than Mem0 for full stateful runtime; Mem0 is just memory.
- Source: https://www.letta.com/blog/letta-v1-agent ; https://www.letta.com/blog/agent-memory
- Confidence: HIGH
- Skill-Impact: DIRECT (cross-ref R1 hierarchical memory)
- Borrow: "Stateless LLM + stateful runtime" architecture cleanly separates the model from the memory system.

---

### Novel Architectures (neurosymbolic, agent-foundation models)

**Cognitive Kernel-Pro (Tencent) trains an Agent Foundation Model.**
- Detail: First open framework to systematically curate Queries × Trajectories × Verifiable Answers across web/file/code/reasoning. 8B AFM beats prior leading open systems on GAIA. Suggests training a model specifically for orchestration roles is feasible at small scale.
- Source: https://arxiv.org/pdf/2508.00414
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: When fine-tuning is possible, this is the recipe; until then, treat sub-agent training data collection as a first-class artifact.

**Sakana AI Fugu — Multi-Agent Orchestrator as Foundation Model.**
- Detail: Two ICLR 2026 papers from Sakana: "Learning to Orchestrate Agents in Natural Language with the Conductor" and "TRINITY: An Evolved LLM Coordinator". Fugu models are the result. The orchestrator itself is trained, not just prompted.
- Source: https://sakana.ai/fugu-beta/
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: Conceptually validates "orchestrator-as-trained-model" — orchestration may eventually be a fine-tuned specialty.

**Voyager-style self-extending skill libraries (continuous lifelong learning).**
- Detail: Original Voyager: automatic curriculum + ever-growing skill library (JS functions indexed by embedding of NL description) + iterative prompting with execution-error feedback. Top-5 most-relevant skills retrieved per task. 2026 follow-ups: "Agent Skills for Large Language Models" survey (arxiv 2602.12430) maps the taxonomy of skill acquisition methods.
- Source: https://github.com/MineDojo/Voyager ; https://arxiv.org/html/2602.12430v3
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: This is the conceptual ancestor of Claude Skills. Index skills by NL-description embedding; retrieve top-K per task; store winning code on success.

**Neurosymbolic agents — Z3/SMT solvers + LLM ensembles.**
- Detail: 2026 highlights: **FregeLogic (Amazon, SemEval 2026)** uses 5 LLM classifiers (Llama 4 Maverick/Scout, Qwen3-32B) + Z3 SMT solver as a formal tiebreaker. **Novelty Adaptation (arxiv 2603.11351)** combines symbolic planner + RL + LLM. **Ontology-Constrained Neural Reasoning (arxiv 2604.00555)** uses 3-layer ontologies (Role/Domain/Interaction) to ground enterprise agents. **VERUS-LM** is a versatile framework for combining LLMs with symbolic reasoning.
- Source: https://www.amazon.science/publications/fregelogic-at-semeval-2026-task-11 ; https://arxiv.org/abs/2603.11351 ; https://arxiv.org/pdf/2604.00555
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: Formal verifiers as tiebreakers between LLM ensembles is a cheap reliability boost when correctness is checkable.

**ALMA — Meta-learning Agentic Memory Designs.**
- Detail: Meta Agent searches over memory designs **as executable code** (self-improving memory). Code: github.com/zksha/alma.
- Source: https://arxiv.org/pdf/2602.07755
- Confidence: MEDIUM
- Skill-Impact: INDIRECT
- Borrow: "Memory architecture as a program the agent can edit" is a powerful frame for our memory work.

**MAS-Orchestra + ORCH — RL-trained orchestrators.**
- Detail: MAS-Orchestra formulates multi-agent orchestration as **function-calling RL with holistic system-level reasoning**; introduces MASBench. ORCH (Feb 2026) is a deterministic multi-agent orchestrator with EMA-guided routing for discrete-choice reasoning.
- Source: https://arxiv.org/pdf/2602.01797
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

**ARTIST — Agentic Reasoning and Tool Integration in Self-Improving Transformers.**
- Detail: Microsoft framework. LLMs learn optimal strategies for tools + complex environments via RL.
- Source: https://www.microsoft.com/en-us/research/wp-content/uploads/2025/04/AgenticReasoning.pdf
- Confidence: MEDIUM
- Skill-Impact: NONE

**QwQ-32B (Qwen) + DeepSeek-R1 — open reasoning agents.**
- Detail: QwQ-32B (RL-trained, agent capabilities baked in: tool use + reasoning + environmental feedback) matches DeepSeek-R1-671B on many benchmarks. DeepSeek-R1-Zero showed pure RL (no SFT) yields emergent reasoning. R1-distilled into 7B/14B/32B Qwen + 8B/70B Llama — DeepSeek-R1-Qwen-14B outperformed standalone QwQ-32B.
- Source: https://qwenlm.github.io/blog/qwq-32b/ ; https://arxiv.org/html/2501.12948v1
- Confidence: HIGH
- Skill-Impact: INDIRECT
- Borrow: Reasoning + agentic tool use can be co-trained; relevant if we ever consider distilling our orchestrator.

---

### Standards & Protocols (MCP, A2A, etc.)

**MCP at 97M monthly downloads (4,750% growth in 16 months from launch).**
- Detail: From ~2M/month at Nov 2024 launch to 97M by March 2026. 10,000+ public MCP servers across registries; ~1,200 on npm. Now governed by **Linux Foundation**; embraced by OpenAI, Microsoft, Google, AWS, Salesforce, IBM, Cisco, MongoDB, Cohere, LangChain.
- Source: https://thenewstack.io/model-context-protocol-roadmap-2026/ ; https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
- Confidence: HIGH
- Skill-Impact: DIRECT

**MCP 2026 roadmap priorities (official, last updated 2026-03-05).**
- Detail:
  1. **Transport evolution**: stateless Streamable HTTP across multiple server instances; behave correctly behind LBs/proxies. **MCP Server Cards** via `.well-known` URL for static capability discovery without connecting.
  2. **Agent Communication**: lifecycle gaps in Tasks primitive (SEP-1686) — retry semantics, expiry policies.
  3. **Governance**: Contributor Ladder SEP, WG delegation model, charter templates.
  4. **Enterprise Readiness**: audit trails, SSO-integrated auth (Cross-App Access), gateway/proxy patterns, configuration portability.
  - On the horizon: triggers/webhooks, streamed + reference-based result types, security/authz (DPoP SEP-1932, Workload Identity Federation SEP-1933), **a Skills primitive for composed capabilities**.
- Source: https://modelcontextprotocol.io/development/roadmap
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: A "Skills primitive" being on MCP's roadmap means our skill design should anticipate MCP-Skills interop.

**MCP Streamable HTTP transport (March 2025 spec).**
- Detail: Replaced HTTP+SSE. Single-endpoint, stateless-capable, works behind load balancers + proxies + across org boundaries. Solved the localhost problem.
- Source: https://modelcontextprotocol.io/specification/2025-03-26/basic/transports
- Confidence: HIGH
- Skill-Impact: INDIRECT

**A2A Protocol — Linux Foundation, 150+ orgs in production.**
- Detail: HTTP + JSON-RPC 2.0. Defines how agents discover capabilities, negotiate task delegation, exchange structured data, maintain context. Seven task states: submitted, working, input-required, completed, failed, canceled, rejected. Supporters: Google, Microsoft, AWS, Salesforce, SAP, ServiceNow, Workday, IBM, Cisco, PayPal, LangChain, MongoDB, Cohere.
- Source: https://galileo.ai/blog/google-agent2agent-a2a-protocol-guide ; https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade
- Confidence: HIGH
- Skill-Impact: INDIRECT

**ACP (Agent Communication Protocol) — IBM, merged with A2A under LF AI & Data.**
- Detail: Lightweight HTTP-native peer-to-peer agent comms. Primary impl: BeeAI Framework (Python + TS). ACP joined A2A under Linux Foundation governance in Aug 2025.
- Source: https://research.ibm.com/blog/agent-communication-protocol-ai ; https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/
- Confidence: HIGH
- Skill-Impact: NONE

**AGNTCY (Cisco-led, Linux Foundation) — agent identity + directory.**
- Detail: Open Internet of Agents. Components: **Identity** (W3C DIDs, verifiable credentials, bring-your-own from Okta/A2A Agent Cards), **Directory** (registration, search, resolution), **OASF** (OCI-based extensible schema describing A2A agents + MCP servers). Forming members: Cisco, Dell, Google Cloud, Oracle, Red Hat. 75+ companies on board by July 2025.
- Source: https://docs.agntcy.org/ ; https://github.com/agntcy/identity
- Confidence: HIGH
- Skill-Impact: NONE

**OpenAI Apps SDK — built on MCP.**
- Detail: Apps SDK released as open standard built on MCP. Extends MCP so devs can design both logic and UI of apps. Open source, runs anywhere that adopts the standard. OpenAI Agents SDK 2026 update: configurable memory, sandbox-aware orchestration, Codex-like filesystem tools.
- Source: https://openai.com/index/introducing-apps-in-chatgpt/ ; https://techcrunch.com/2026/04/15/openai-updates-its-agents-sdk-to-help-enterprises-build-safer-more-capable-agents/
- Confidence: HIGH
- Skill-Impact: INDIRECT

**LlamaIndex + Agent Client Protocol (ACP) integration (Jan 2026).**
- Detail: LlamaIndex Workflows + ACP integration with filesystem tools, MCP servers, persistent memory. Pre-built document agent templates via `llamactl`. llama-index-workflows v1.0+ is the event-driven, async-first composition primitive.
- Source: https://www.llamaindex.ai/blog/llamaindex-newsletter-2026-01-06 ; https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems
- Confidence: HIGH
- Skill-Impact: INDIRECT

---

### Sandboxing & Safe Execution

**The Big Four sandbox platforms (E2B / Modal / Daytona / Vercel Sandbox), plus Northflank/Blaxel.**
- Detail:
  - **E2B**: Firecracker microVMs, hardware-level isolation per session. Best for "untrusted code from LLMs". Largest catalog of community-built templates. Cold start ~90-150ms.
  - **Daytona**: Docker containers, shared kernel. Fastest provisioning (27-90ms). Persistent dev workspace orientation. Better for "agent builds up state over time".
  - **Modal**: gVisor-based isolation. **Only platform where a sandbox can hold a GPU.** Required if agent needs to run inference/fine-tune/process images inside the sandbox.
  - **Vercel Sandbox**: newer entrant, headless browser automation CLI for AI agents (12.1k stars).
  - **Blaxel**: 25ms cold start (industry-leading).
- Source: https://northflank.com/blog/daytona-vs-e2b-ai-code-execution-sandboxes ; https://www.superagent.sh/blog/ai-code-sandbox-benchmark-2026 ; https://modal.com/resources/best-code-execution-sandboxes-coding-agents
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: For LLM-generated code, use Firecracker microVMs (E2B) or Kata Containers — hardware boundary blocks kernel-based attacks. For GPU sub-tasks, Modal is currently the only option.

**Sandbox isolation hierarchy (2026 standard).**
- Detail: Layer 1: virtualization tech (AWS Firecracker microVMs, gVisor user-space kernel, Cloud Hypervisor, Microsoft LiteBox library OS). gVisor adds 10-30% I/O overhead, minimal compute overhead. Firecracker: 125ms boot, <5MiB overhead, 150 microVMs/sec/host.
- Source: https://northflank.com/blog/how-to-sandbox-ai-agents ; https://emirb.github.io/blog/microvm-2026/
- Confidence: HIGH
- Skill-Impact: INDIRECT

**Browser-Use (89.1% on WebVoyager) leads OSS browser agents.**
- Detail: Top OSS browser-automation harness. UI-TARS (Alibaba) has the most reliable Windows desktop support thanks to a custom vision model trained on Windows UI screenshots. BrowserOS / Browser Operator are privacy-focused alternatives. Steel is the OSS browser-API-for-agents service.
- Source: https://www.firecrawl.dev/blog/best-browser-agents ; https://aimultiple.com/open-source-web-agents
- Confidence: HIGH
- Skill-Impact: INDIRECT

---

### Cost / Efficiency Patterns

**Three-tier model routing (Opus/Sonnet/Haiku style) saves ~51%.**
- Detail: Frontier for coordination, mid for high-volume implementation, fast/small for file ops. Three-tier Claude routing saves 51% vs uniform Opus deployment. Multi-model routing commonly delivers 30-60% cost reduction. IDC forecasts 60% of enterprise apps will include multi-agent AI by 2026.
- Source: https://www.augmentcode.com/guides/ai-model-routing-guide ; https://www.swfte.com/blog/intelligent-llm-routing-multi-model-ai
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Explicitly route sub-tasks by complexity tier — our skill should call out which sub-agent uses which model tier.

**Cascade failure modes — under-discussed risk.**
- Detail: In tree-like multi-agent regimes, a single agent failure cascades exponentially. In dense cyclic regimes, the same failure self-limits within one hop. Schedulers typically optimize load + fitness but carry no failure-propagation model.
- Source: https://arxiv.org/html/2603.17112v1
- Confidence: MEDIUM
- Skill-Impact: DIRECT
- Borrow: For high-reliability flows, prefer dense-cyclic communication over pure trees — limits cascade blast radius.

**Sub-goal distillation + small-model agents.**
- Detail: Hierarchical agents distill LLM-generated sub-goals into smaller models. Neither module needs real-time LLM access at inference, reducing total cost to a fixed cost. 40% of enterprise apps to integrate task-specific AI agents by 2026.
- Source: https://arxiv.org/pdf/2405.02749
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

**SpecRouter / SpecForge — speculative decoding as adaptive routing.**
- Detail: Multi-level speculative decoding reimagined as an adaptive routing problem. SpecForge is an OSS training framework for speculative decoders. Note: coding workloads benefit, creative tasks can slow down.
- Source: https://arxiv.org/abs/2505.07680 ; https://arxiv.org/pdf/2603.18567
- Confidence: MEDIUM
- Skill-Impact: NONE

**Qwen 3 Coder / Qwen 3.6 Plus — best self-hostable open-weight coders.**
- Detail: Qwen 3.6 Plus = top open-weight for demanding agentic coding (1M context, frontier-competitive). Qwen 3 Coder handles routine coding at a fraction of frontier cost. 32B dense + 235B MoE variants self-hostable on consumer/prosumer hardware.
- Source: https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

---

### Open Verifiers & Process Reward Models

**ThinkPRM (mukhal/thinkprm) — generative long-CoT PRM.**
- Detail: Repurposes open-weight reasoning models as generative PRMs via lightweight training on synthetic data (as few as **8K step labels** vs PRM800K's ~700K). Released sizes: 1.5B + 14B (R1-Distill-Qwen base), 7B (Deepseek-R1-Distill-Qwen-7B base, May 2025). Outperforms LLM-as-Judge + discriminative PRMs in/out of domain. Can scale verifier compute in parallel or by thinking longer.
- Source: https://github.com/mukhal/thinkprm ; https://arxiv.org/pdf/2504.16828
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Generative PRMs (CoT-style verification) outperform discriminative PRMs and need ~100x fewer labels. Use one as our skill's verifier of sub-agent outputs.

**OpenPRM, VersaPRM, GenPRM — multi-domain process verifiers.**
- Detail: **OpenPRM** unifies ORMs + PRMs under pairwise ranking — open-domain scalability. **VersaPRM** fine-tunes a math PRM on synthetic multi-domain data — generalizes beyond math. **GenPRM** scales test-time compute via generative reasoning.
- Source: https://github.com/RyanLiu112/Awesome-Process-Reward-Models ; https://arxiv.org/pdf/2502.06737 ; https://arxiv.org/pdf/2504.00891
- Confidence: HIGH
- Skill-Impact: INDIRECT

**Multi-Agent Verification (MAV) — verifiers as a third scaling axis.**
- Detail: Beyond more generators and longer thinking, **scaling the number of verifiers** is a new test-time compute paradigm. Performance improves with verifier count across domains + LLMs.
- Source: https://arxiv.org/pdf/2502.20379
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Run multiple cheap verifiers in parallel rather than one big one — diversity beats size.

**Inference-Aware Fine-Tuning for BoN (BoN-RL-V).**
- Detail: Training a generator with the same verifier used at test-time is critical. BoN-RL-V shows substantial improvements over baselines.
- Source: https://arxiv.org/pdf/2412.15287
- Confidence: MEDIUM
- Skill-Impact: NONE

---

### Discovery-Oriented Open-Source

**OpenEvolve (algorithmicsuperintelligence/openevolve) — best AlphaEvolve clone.**
- Detail: MAP-Elites + LLM evolutionary pipeline. Three components: **Generator** (LLM ensemble with weighted combinations + fallback), **Evaluator** (cascade eval, artifact feedback, multi-stage testing), **Database** (MAP-Elites grid, island-based parallel evolution). **Artifact side-channel**: execution errors/warnings feed back into subsequent generation prompts. Results: 2-3x real hardware speedups, SOTA circle packing (n=26), 2.8x faster GPU kernels on M1 Pro, +23% on HotpotQA via prompt evolution. Domains: GPU kernel opt (Metal/CUDA), algorithm discovery, scientific computing, multi-language (Python/Rust/R/Metal shaders), prompt optimization.
- Source: https://github.com/algorithmicsuperintelligence/openevolve
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Artifact side-channel (errors → next-gen prompts), island architecture, double-selection (different programs for performance vs inspiration), MAP-Elites quality-diversity grid. All directly transferable to our discovery-style skills.

**CodeEvolve (arxiv 2510.14150) — fully open evolutionary coding agent.**
- Detail: Operationalizes LLM-driven search in a transparent fully-open framework. Open-weight models often match or exceed closed-source baselines at a fraction of compute cost.
- Source: https://arxiv.org/html/2510.14150v4
- Confidence: HIGH
- Skill-Impact: INDIRECT

**OpenAlpha_Evolve / jamesahou-openevolve / ryanrudes-openevolve — multiple parallel clones.**
- Detail: Confirms strong community interest in OSS AlphaEvolve. All share core ideas: iterative writes-tests-improves with LLMs via LiteLLM, evolutionary selection.
- Source: https://github.com/shyamsaktawat/OpenAlpha_Evolve ; https://github.com/jamesahou/openevolve
- Confidence: HIGH
- Skill-Impact: NONE

**The AI Scientist v2 (Sakana, OSS) — workshop-level automated discovery.**
- Detail: Removes the dependency on human-coded templates from v1. Employs **agentic tree search** to generate + refine code implementations. OSS at github.com/SakanaAI/AI-Scientist-v2.
- Source: https://github.com/SakanaAI/AI-Scientist (v1) ; https://pub.sakana.ai/ai-scientist-v2/paper/paper.pdf
- Confidence: HIGH
- Skill-Impact: DIRECT
- Borrow: Agentic tree search beats template-based scaffolding. Use a search-tree over hypotheses rather than fixed prompt templates.

**EvoScientist (arxiv 2603.08127) — multi-agent evolving AI scientists.**
- Detail: Continuously improves research strategies via persistent memory + self-evolution. End-to-end scientific discovery.
- Source: https://arxiv.org/pdf/2603.08127
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

**Deep Researcher Agent (arxiv 2604.05854) — 24/7 deep-learning experimentation.**
- Detail: Handles full ML experiment lifecycle: hypothesis → code → training execution → analysis → iteration. Distinct from paper-writing focused systems.
- Source: https://arxiv.org/pdf/2604.05854
- Confidence: MEDIUM
- Skill-Impact: INDIRECT

---

### Benchmark Landscape (which harnesses are winning)

- **SWE-Bench Verified**: OpenHands + CodeAct v3 = 68.4% on Opus 4.6 (open SOTA). SWE-agent v1 = 43.2% on Sonnet 4.5. Caveat: OpenAI found 59.4% of hardest cases had flawed test cases; SWE-bench Pro is the recommended replacement.
- **SWE-Bench Pro (1,865 multi-language tasks)**: Claude Mythos Preview 77.8% (May 19, 2026); Claude Opus 4.7 (Adaptive) 64.3%; GPT-5.5 58.6%.
- **Terminal-Bench 2.0 (89 realistic terminal tasks, Jan 2026)**: Codex CLI + GPT-5.2 = 63%; Terminus 2 + Claude Opus 4.5 = 58%.
- **GAIA** (Princeton HAL leaderboard, April 2026): Claude Sonnet 4.5 = 74.6%. Anthropic models sweep top 6. **OWL** = 69.09% (#1 OSS).
- **Tau2-bench**: Claude Opus 4.6 = 99.3% telecom, 91.9% retail (highest recorded).
- **Deep Research Bench (RACE score)**: Gemini-2.5-Pro Deep Research = 48.88 (lead). LangChain `open_deep_research` = 49.43 with GPT-5 (ranked #6).
- **Key meta-finding**: Same model showed up to **6x performance variation** by harness alone (GPT-5.5 jumped 61.5% → 87.2% on one benchmark just by switching harness). "The harness is now the product."
- Source: https://benchmarkingagents.com/agent-benchmarks/ ; https://www.mindstudio.ai/blog/agent-harnesses-beat-model-upgrades-5-benchmarks ; https://www.morphllm.com/swe-bench-pro

**Inspect AI (UK AISI, OSS) — emerging evaluation standard.**
- Detail: UK AI Security Institute's framework. Primitives: dataset → Task → Solver → Scorer. Multi-turn/agent workflows with tools, sandboxed exec (Docker built-in, optional K8s/Proxmox), VS Code log viewer, web Inspect View. 200+ pre-built evals via Inspect Evals (collab with Arcadia Impact, Vector Institute). Includes OWASP Top 10 for Agentic Applications (2026) evals.
- Source: https://github.com/UKGovernmentBEIS/inspect_ai ; https://github.com/UKGovernmentBEIS/inspect_evals
- Confidence: HIGH
- Skill-Impact: INDIRECT

---

### Cross-References

- **R1 / R2 / R3 (lab products)**: This research mentions Claude/GPT/Gemini only as the *model* powering OSS harnesses. The Claude Agent SDK is included because it's the OSS-distributed SDK form (not the product).
- **R1 hierarchical memory**: Letta/MemGPT core/archival/recall hierarchy + DeepAgent's "memory folding" + ALMA's meta-learned memory designs are all relevant memory-system primitives.
- **R4 architecture papers**: OWL's Workforce training, Cognitive Kernel-Pro's AFM training data recipe, MAS-Orchestra's RL-trained orchestrators, ARTIST — these blur into R4's "training paradigms for agents" but are covered here because they ship as OSS frameworks/codebases.
- **R5 context engineering**: LangChain 1.0 middleware hooks, deepagents virtual filesystem, OpenHands event-sourced state, and CrewAI checkpoint forking are *infrastructure* for the context tricks R5 catalogs. Borrow primitives from here; borrow techniques from R5.

---

### Gaps & Open Questions

1. **No clear winner among "research agent" OSS frameworks for our use case.** OWL leads benchmarks but is heavyweight; `deepagents` is more aligned with our skill; `open_deep_research` is the cleanest reference architecture. Recommend: study `deepagents` source closely, treat it as the closest analog.
2. **MCP-Skills primitive** is on the roadmap but undefined. We should anticipate but not depend on it.
3. **OSS verifier integration into agent frameworks is shallow.** ThinkPRM, OpenPRM exist as models but few frameworks integrate them as first-class. Opportunity.
4. **Voyager-style continual skill libraries**: 2026 follow-ups are mostly surveys, not new working systems. The original idea is robust but under-implemented for non-Minecraft domains.
5. **Cost-routing remains ad-hoc**: routing libraries (RouteLLM, LiteLLM router) exist but multi-agent frameworks rarely wire routing into orchestrator decisions automatically. Manual tier mapping is still the norm.
6. **Cascade-failure-aware orchestration is unstudied in practice**: theory in arxiv 2603.17112, no OSS implementation maps to it yet.
7. **Discovery-oriented OSS converges on MAP-Elites + LLM + artifact feedback.** OpenEvolve's design appears stable across ~4 independent clones — this is the de facto open AlphaEvolve pattern.
8. **Agent foundation models are emerging but tiny (8B is SOTA open).** Cognitive Kernel-Pro and Sakana Fugu suggest the next wave but no community-trained orchestrator-specialty model is widely available yet.
9. **Identity layer underutilized**: AGNTCY exists and is Linux-Foundation backed, but no major framework uses verifiable agent IDs yet in practice.
10. **Browser-Use sits separately** from coding agents — bridging browser + code in one harness (OpenHands does this) is still rare and gives a big GAIA lift.
