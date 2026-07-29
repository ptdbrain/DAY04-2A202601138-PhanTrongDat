# Tool Folder Contract

Each tool lives in its own folder:

```text
tools/<tool_name>/
  TOOL.md   # frontmatter + human notes
  tool.py   # self-contained implementation
```

`tools/__init__.py` is the registry. `agent.py`, `chat.py`, and `run_eval.py`
import `TOOL_FUNCTIONS` from that registry.

## Frontmatter Fields

Every `TOOL.md` uses the same fields:

```yaml
---
name: tool_name
track: core | bonus
kind: live_api | local_formatter | local_knowledge | action | control
provider: Provider name if any
requires_env: [ENV_VAR]
inputs: [arg_name]
outputs: [field_name]
side_effect: false | true | local_file_write
requires_confirmation: true   # only for write/action tools
---
```

Core tools are enough to pass the base lab. `track: bonus` means optional or
extension-only; it does not automatically earn bonus points. If its declaration
stays in `tools.yaml`, the model can still see it and core routing may change.
