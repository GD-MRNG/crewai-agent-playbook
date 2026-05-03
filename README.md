# crewai-agent-playbook

A progressive, hands-on learning repository for multi-agent systems using CrewAI. Each phase builds on the last, introducing new concepts through working code.

## Setup

```bash
# Install dependencies
uv sync --python 3.12

# Copy and fill in your API keys
cp .env.example .env
```

## Running a crew

```bash
uv run python main.py debate
uv run python main.py financial_researcher
uv run python main.py stock_picker
uv run python main.py coder
uv run python main.py engineering_team
```

Inputs are hardcoded per crew in `main.py` — edit them directly before running.

> Phase 4 (`coder`) requires Docker Desktop to be running.

## Phases

| Phase | Crew | New concepts |
|---|---|---|
| 1 | `debate` | `Agent`, `Task`, `Crew`, `Process.sequential`, YAML config, `output_file` |
| 2 | `financial_researcher` | `SerperDevTool`, `context` passing between tasks |
| 3 | `stock_picker` | Custom `BaseTool`, `output_pydantic`, `Process.hierarchical`, memory |
| 4 | `coder` | `allow_code_execution`, Docker sandbox, execution loops |
| 5 | `engineering_team` | Multi-agent collaboration, chained context, Gradio UI generation |

## Environment variables

```
PYTHONUTF8=1              # prevents emoji encoding errors on Windows
OPENAI_API_KEY=           # all phases
SERPER_API_KEY=           # Phase 2+
DISCORD_WEBHOOK_URL=      # Phase 3+
CREWAI_TRACING_ENABLED=true  # optional — requires crewai login
```

## Tracing

CrewAI can capture agent decisions, task timelines, tool usage, LLM calls, tokens, and costs via the [CrewAI AMP](https://app.crewai.com) platform.

```bash
# One-time authentication
crewai login
```

Then set `CREWAI_TRACING_ENABLED=true` in `.env`. Traces appear under the **Traces** tab at [app.crewai.com](https://app.crewai.com).

## Structure

```
src/crews/<name>/
  crew.py                 # @CrewBase class with agents, tasks, crew
  config/agents.yaml      # role, goal, backstory, llm
  config/tasks.yaml       # description, expected_output, agent, output_file
projects/                 # learning notes, one per phase
output/                   # generated at runtime, gitignored
```
