---
layout: page
title: Healthcare Operations Copilot
description: Production-style LLM agent for referral intake, payer policy retrieval, tool calling, guardrails, and human review.
img: assets/img/healthcare_ops_copilot_harness_loop.png
importance: 0
category: portfolio
---

Built a production-style healthcare operations copilot MVP that analyzes synthetic referral and intake cases, retrieves payer policy and clinic SOP evidence, calls operational tools, and returns a structured next-action recommendation with confidence, source citations, and human-review flags.

GitHub: [marcin-ogrodniczuk/healthcare-ai-agent](https://github.com/marcin-ogrodniczuk/healthcare-ai-agent)

The goal of this project is to demonstrate practical LLM production engineering: not just prompting a model, but building the surrounding harness, agent loop, memory layer, guardrails, evaluation checks, and observability path that make an AI system more reliable. The MVP intentionally avoids paid model calls: the LLM-ready reasoning node is deterministic today, with a clear production path to OpenAI or LiteLLM structured output.

**Core workflow.** A user submits a synthetic case packet with referral notes, insurance details, intake forms, and appointment rules. FastAPI validates the input as a `CaseRequest`, initializes LangGraph `AgentState`, and runs a LangGraph state machine through structured extraction, LangChain RAG, local operational tools, deterministic MVP reasoning, guardrails, and structured `AgentDecision` output.

**Production concepts demonstrated.**

- RAG pipeline with LangChain document chunking, metadata-aware retrieval, citations, and a planned pgvector store
- LangGraph StateGraph orchestration for the agent run loop
- Structured extraction with Pydantic schemas and JSON validation
- Tool calling for eligibility checks, appointment search, missing-document detection, and payer scripts
- LLM-ready reasoning node with deterministic MVP logic and a production swap-in path for OpenAI/LiteLLM
- Guardrails for no diagnosis, no unsupported medical advice, citation checks, and human review routing
- Agent memory model with procedural memory in code/rules, semantic memory in local policy/SOP references, and episodic memory in run trace JSON
- Evaluation harness with golden test cases for retrieval quality, schema validity, action selection, and hallucination checks
- LLMOps path for traces, latency, token cost, model versioning, retrieval quality, and CI/CD eval gates

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/healthcare_ops_copilot_harness_loop.png" title="Healthcare operations copilot harness, loop, and LLMOps architecture" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The architecture separates the FastAPI harness, LangGraph state machine, semantic and episodic memory, operational tools, guardrails, and external LLMOps evaluation path.
</div>

**Tech stack.** The no-cost MVP uses FastAPI, Pydantic, LangGraph, LangChain text splitters, local policy and SOP documents, local Python tools, deterministic decision logic, synthetic healthcare cases, pytest golden cases, and Docker Compose. The production roadmap adds OpenAI/LiteLLM structured output, Postgres + pgvector semantic memory, Redis-backed queues, a React review dashboard, LangSmith/Langfuse or OpenTelemetry traces, and GitHub Actions evaluation gates.

This project intentionally avoids real PHI. It uses synthetic patient/referral examples and public healthcare reference material so the demo can show production AI patterns without exposing sensitive clinical data.
