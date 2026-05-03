# Project 3 — Stock Picker

## What This Project Does

Three agents — a news analyst, a financial researcher, and a stock picker — collaborate under a manager agent to identify trending companies in a sector, research them in depth, and select the best investment candidate. The manager delegates tasks using a hierarchical process rather than a fixed sequential pipeline. Results are stored as structured JSON (`trending_companies.json`, `research_report.json`) and a markdown decision report (`decision.md`). When a decision is made, the stock picker sends a Discord notification via a custom tool. The sector and current date are passed in as inputs from `main.py`.

## New Concepts Introduced

**Custom `BaseTool` — extending agents with arbitrary capabilities**
Tools in CrewAI are Python classes that inherit from `BaseTool`. You define a Pydantic model for the tool's input (`args_schema`), implement `_run()` to execute the action, and attach the tool to an agent at construction time. The agent then calls the tool autonomously when it determines the tool is needed. The Discord tool wraps a single HTTP POST to a webhook URL — the same pattern applies to any external API, database write, or file operation you want to expose to an agent.

**`output_pydantic` — structured output from tasks**
Setting `output_pydantic=SomeModel` on a task instructs CrewAI to parse the agent's response into a validated Pydantic instance. The parsed object flows to downstream tasks as typed data rather than a blob of text. This makes the pipeline robust: the `research_trending_companies` task receives a guaranteed-valid list of companies, not freeform prose it has to interpret. Pydantic validation catches malformed output early rather than silently passing garbage forward.

**`Process.hierarchical` — manager-delegated execution**
In a hierarchical process, a manager agent receives the full task list and decides how and in what order to delegate them to worker agents. Workers do not communicate directly — all coordination flows through the manager. This is more flexible than `Process.sequential` when the optimal execution order isn't fully predictable at design time. The trade-off is cost: the manager runs on `gpt-4o` and adds tokens on every delegation decision. The manager is constructed inline in `crew()` with `allow_delegation=True` and is intentionally not decorated with `@agent` (which would add it to the worker pool).

**Memory — retaining context across tasks and sessions**
CrewAI provides a unified `Memory` class that replaces the old separate `ShortTermMemory`, `LongTermMemory`, and `EntityMemory` types. A single `Memory` instance handles all three concerns: it uses an LLM to infer scope and importance when saving, blends semantic similarity, recency, and importance scores when recalling, and persists to a LanceDB vector store. Pass it directly to `Crew(memory=Memory(...))`:

```python
memory=Memory(
    storage="./memory/stock_picker/",
    embedder={"provider": "openai", "config": {"model_name": "text-embedding-3-small"}},
)
```

The `storage` path namespaces the LanceDB directory to avoid collisions with other crews sharing the project root.

## Key Principles

**Tools isolate side effects.** The Discord notification is a side effect — it reaches outside the agent system to notify a human. Isolating it in a `BaseTool` means the rest of the crew code has no knowledge of how notifications are delivered. Swapping to Slack, email, or SMS is a one-file change in `discord_tool.py`.

**Structured output is a contract between tasks.** `output_pydantic` turns a task's output from text into a typed object. In a pipeline, this is the difference between agents passing structured data versus passing prose and hoping the next agent can parse it. Define your Pydantic models early — they double as documentation of what each task is expected to produce.

**Hierarchical process trades cost for flexibility.** The manager agent incurs additional tokens on every delegation decision. This is the right trade-off when task ordering or assignment isn't fully deterministic at design time. For a fixed pipeline with a known order, `Process.sequential` is cheaper and equally correct.

**Memory paths must be namespaced.** If multiple crews share the same `./memory/` root without subdirectories, their LanceDB stores will collide. The `storage="./memory/stock_picker/"` argument on `Memory(...)` ensures each crew's memory is isolated even when crews are run from the same project directory.

## Sample Output

**Sector:** Technology  
**Run date:** May 4, 2026

`trending_companies.json` (excerpt):
```json
{
  "companies": [
    {"name": "Databricks", "ticker": "DBX", "reason": "Pre-IPO buzz around $134B valuation and dominance in the data lakehouse and analytics market."},
    {"name": "Anthropic", "ticker": "N/A", "reason": "Strong AI safety positioning and $30B revenue run rate, though facing regulatory scrutiny."},
    {"name": "KKR's Helix", "ticker": "N/A", "reason": "$10B AI infrastructure venture led by former AWS chief attracting investor attention."}
  ]
}
```

`decision.md` (excerpt):
> **Chosen Company: Databricks**
>
> Databricks is selected for its $134B valuation, leadership in the data lakehouse and analytics space, and near-term IPO prospects that offer additional upside. Anthropic was passed over due to regulatory risk; KKR's Helix was too early-stage with unproven market acceptance.

## What to Try

- Change `"sector"` in `main.py` to `"Healthcare"` or `"Energy"` and observe how the trending companies shift
- Set `DISCORD_WEBHOOK_URL` to a test webhook and verify the notification arrives with the correct message
- Remove `output_pydantic` from `find_trending_companies` and observe how the loss of structured output affects the research task downstream
- Add a fourth agent — a `risk_analyst` — whose task is to identify the top 3 risks for the selected company, chained via `context: [pick_best_company]`
- Run the crew twice in the same session and observe entity memory preventing the same companies from being picked again
