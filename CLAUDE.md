# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run a specific crew
python main.py debate
python main.py financial_researcher
python main.py stock_picker
python main.py coder
python main.py engineering_team
```

Inputs are hardcoded per crew in `main.py` and can be edited directly before running.

Phase 4 (`coder`) requires Docker Desktop running for sandboxed code execution.

## Architecture

This is a progressive CrewAI learning repository. Each phase (crew) builds on the last, introducing new concepts. The code is the learning material — clarity and readability are the primary design goals.

**Entry point:** `main.py` maps CLI arguments to crew classes and calls `.kickoff()`.

**Crew structure** — every crew follows this layout:
```
src/crews/<name>/
  crew.py                  # @CrewBase class with @agent, @task, @crew decorators
  config/agents.yaml       # agent definitions: role, goal, backstory, llm
  config/tasks.yaml        # task definitions: description, expected_output, agent, context, output_file
```
Config paths resolve relative to `crew.py` (required by `@CrewBase` for nested folder structure). Outputs write to `output/<crew_name>/` (gitignored, created at runtime).

**LLM selection:** `gpt-4o` for manager/complex-reasoning agents, `gpt-4o-mini` for workers. Model is a one-line change in `agents.yaml`.

**Phase progression and new concepts per phase:**
- Phase 1 `debate` — `Agent`/`Task`/`Crew` primitives, `Process.sequential`, YAML config, `output_file`
- Phase 2 `financial_researcher` — `SerperDevTool` (web search), `context` passing between tasks
- Phase 3 `stock_picker` — custom `BaseTool` (Discord webhook), `output_pydantic` (Pydantic structured output), `Process.hierarchical`, short/long-term/entity memory
- Phase 4 `coder` — `allow_code_execution=True`, `code_execution_mode="safe"` (Docker), execution loops, `max_execution_time`/`max_retry_limit`
- Phase 5 `engineering_team` — multi-agent collaboration, chained context, mixed execution (some agents run code, others write it), Gradio UI generation

**Adding a new crew:**
1. Create `src/crews/<name>/crew.py` + `config/`
2. Add the crew to the dispatcher in `main.py`
3. Add a learning README to `projects/`
4. Commit as a single unit after testing

## Environment Variables

```
OPENAI_API_KEY=           # always required
SERPER_API_KEY=           # required Phase 2+
DISCORD_WEBHOOK_URL=      # required Phase 3+
```

Copy `.env.example` to `.env` and fill in the keys.

## Tracing

CrewAI tracing is enabled via `CREWAI_TRACING_ENABLED=true` in `.env`. It captures agent decisions, task timelines, tool usage, LLM calls, tokens, and costs.

Setup (one-time):
```bash
crewai login
```

Then set `CREWAI_TRACING_ENABLED=true` in `.env` and view traces at [app.crewai.com](https://app.crewai.com) → Traces tab.

## Build / Commit Discipline

Each phase is one commit, committed only after the crew runs successfully and produces correct output. Verify phase-specific acceptance criteria (see `temp/plan.md`) before committing.
