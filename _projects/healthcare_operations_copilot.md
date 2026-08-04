---
layout: page
title: Healthcare Operations Copilot
description: Production-style LLM agent for referral intake, payer policy retrieval, tool calling, guardrails, and human review.
img: assets/img/healthcare_ops_copilot_harness_loop.png
importance: 0
category: portfolio
---

Built a production-style healthcare operations copilot that analyzes synthetic referral and intake cases, retrieves payer policy and clinic SOP evidence, calls operational tools, and returns a structured next-action recommendation with confidence, source citations, and human-review flags.

GitHub: [marcin-ogrodniczuk/healthcare-ai-agent](https://github.com/marcin-ogrodniczuk/healthcare-ai-agent)

The goal of this project is to demonstrate practical LLM production engineering: not just prompting a model, but building the surrounding harness, agent loop, memory layer, guardrails, evaluation checks, and observability path that make an AI system more reliable.

**Core workflow.** A user submits synthetic referral notes, insurance details, intake forms, and appointment rules. The system extracts structured fields such as patient need, payer, diagnosis context, urgency, and missing documents. Retrieval then searches policy and SOP knowledge with citations before the agent recommends one of four operational actions: schedule, request missing information, escalate to human review, or draft a payer call script.

**Production concepts demonstrated.**

- RAG pipeline with LangChain document chunking, metadata-aware retrieval, citations, and a planned pgvector store
- LangGraph StateGraph orchestration for the agent run loop
- Structured extraction with Pydantic schemas and JSON validation
- Tool calling for eligibility checks, appointment search, missing-document detection, and payer scripts
- Guardrails for no diagnosis, no unsupported medical advice, PHI-safe logging, and human review routing
- Agent memory model with procedural memory in code, semantic memory in policy/SOP references, and episodic memory in run traces
- Evaluation harness with golden test cases for retrieval quality, schema validity, action selection, and hallucination checks
- LLMOps path for traces, latency, token cost, model versioning, retrieval quality, and CI/CD eval gates

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/healthcare_ops_copilot_harness_loop.png" title="Healthcare operations copilot harness, loop, and LLMOps architecture" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The architecture separates the agent harness, execution loop, memory stores, and LLMOps evaluation path.
</div>

**Tech stack.** The MVP uses FastAPI, Pydantic, LangGraph, LangChain text splitters, local policy and SOP documents, synthetic healthcare cases, pytest golden cases, Docker Compose, and a planned Postgres + pgvector memory layer. The portfolio roadmap adds Redis-backed queues, a React review dashboard, Langfuse or OpenTelemetry traces, and GitHub Actions evaluation gates.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/healthcare_ops_copilot_mvp_overview.png" title="Healthcare operations copilot MVP overview" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The MVP focuses on a complete, safe vertical slice: synthetic case input, structured extraction, retrieval, tool calls, action recommendation, citations, confidence, and review flags.
</div>

This project intentionally avoids real PHI. It uses synthetic patient/referral examples and public healthcare reference material so the demo can show production AI patterns without exposing sensitive clinical data.
