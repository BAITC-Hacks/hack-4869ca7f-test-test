# Agent Guidelines & Preferences

Project instructions and engineering preferences for AI coding agents.

## Core Philosophy: Standard Library & Anti-Slop
- **Prefer Python Standard Library**: Default to built-in modules (`json`, `argparse`, `sys`, `time`, `os`, `pathlib`, `collections`). Do not introduce third-party packages (e.g., `python-dotenv`, extra CLI helpers) when standard libraries suffice.
- **No Boilerplate Slop in Code**:
  - Do not add file-header docstrings (`"""..."""`) or redundant inline comments explaining obvious code.
  - Avoid over-engineered class abstractions or wrappers for simple tasks.
  - For data models (e.g. Pydantic), use plain typed attributes without redundant `Field(description=...)` descriptors.
- **Modern Python 3.14+ Typing**:
  - Never import `List`, `Dict`, `Set`, `Tuple`, or `Any` from `typing`.
  - Use native built-in types: `list[...]`, `dict[...]`, `set[...]`, `tuple[...]`.
  - Keep function signatures clean and readable.
- **Cross-Platform UTF-8**:
  - Always reconfigure stdout/stderr for UTF-8 (`sys.stdout.reconfigure(encoding="utf-8")`) when printing non-ASCII text (e.g., Cyrillic) to avoid Windows console encoding errors.

## Environment & Secrets Management
- **Isolated Virtual Environment**: Always create and use `venv`. Install dependencies strictly inside `venv`.
- **Exact Pinned Packages**: After installing necessary root packages, pin exact versions using `pip freeze` into `requirements.txt`. Specify the root package in documentation.
- **Secrets in JSON**: Store secrets/keys in `config.json` read via standard `json`. Never use `.env` files or dotenv libraries.
- **Git Hygiene**: Ensure `config.json` and `venv/` are always in `.gitignore`. Provide a clean, non-sensitive `config.example.json` template.

## Documentation & Text Standards
- **English Only**: All documentation (`README.md`) must strictly be written in English.
- **Clean, No-Slop Formatting**:
  - Avoid decorative horizontal dividers (`---`) or filler prose.
  - Maintain a clean hierarchy with clear markdown headings.
  - Provide copy-pasteable terminal commands, CLI tables, and exact raw output samples.

## Verification & Execution
- **Mandatory Live Testing**: Always execute and test scripts locally in the terminal. Verify that output matches requirements and does not break existing functionality before completing a task.
