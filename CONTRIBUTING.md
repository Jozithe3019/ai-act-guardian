# Contributing to AI-Act-Guardian

Thank you for your interest. Contributions are welcome in three areas:

## 1. Adding Rules (`rules.yaml`)

The easiest way to contribute. No Python required.

Each rule needs:
```yaml
- id: "UNIQUE_RULE_ID"
  pattern: "keyword_one|keyword_two"
  msg: "Article X: Human-readable description."
```

For documentation-presence checks:
```yaml
- id: "ART_XX_DOC"
  required_file: "filename.md|filename.json"
  trigger_pattern: "optional_trigger_keyword"   # only check if this appears in code
  msg: "Art XX: Missing required documentation."
```

## 2. Adding Test Fixtures (`Experimental/`)

Add a `.py` file that demonstrates a specific compliance scenario. Good fixtures are:
- **Targeted**: tests one specific rule or evasion technique
- **Commented**: explains what should and should not be flagged
- **Adversarial**: try to evade detection (rename variables, use closures, etc.)

## 3. Engine Contributions (`compliance_engine.py`)

Before modifying the engine, read `GEMINI.md` in full. It documents the engineering mandates that prevent recurring regressions.

Key rules:
- Always use `visitor.generic_visit(func_node)` as entry point, never `visitor.visit(func_node)`
- Use `ast.walk(tree)` to find `FunctionDef` nodes — never assume top-level only
- New sanitization functions belong in `rules.yaml` (`cleanup_funcs`), not hardcoded
- All findings must use `(file_path, rule_id, line)` deduplication key

## Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/annex-iii-justice-rules`
3. Run the engine against the test suite: `python compliance_engine.py`
4. Verify your fixture appears (or doesn't appear) in the certificate as expected
5. Open a Pull Request with a description of the regulatory article addressed
