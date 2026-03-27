# 🛡️ AI-Act-Guardian

> *"Code is Law. Compliance is Code."*

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-2026%20Enforcement-red.svg)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**AI-Act-Guardian** is an open-source static analysis framework that audits Python AI projects for compliance with the **EU Artificial Intelligence Act (Regulation 2024/1689)**, enforceable from August 2026.

It goes beyond simple keyword matching: the engine performs **cross-file taint analysis**, tracking sensitive data flows from source to sink across module boundaries, while enforcing regulatory rules from Art. 5 prohibited practices to Annex III high-risk domain classification.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Cross-File Taint Tracking** | Follows PII/sensitive data across `from X import Y` and `import X; X.y()` import styles |
| **Sanitization-Aware** | Correctly clears taint when `anonymize()`, `mask()`, `encrypt()` etc. are called — no false positives |
| **Class Method Coverage** | Audits functions at any nesting level, including methods inside classes |
| **Art. 5 Prohibited Practices** | Detects subliminal manipulation, vulnerable group exploitation, biometric surveillance, social scoring |
| **Annex III High-Risk Domains** | Medical, HR, finance, critical infrastructure, education system classification |
| **Art. 14 HITL Enforcement** | Checks that clinical/diagnostic functions include mandatory human-in-the-loop approval |
| **Art. 52 Deception Detection** | Flags explicit `is_ai_generated = False` adversarial disclosure bypass |
| **Art. 9/10/11 Doc Checks** | Verifies presence of Risk Registry, Technical Documentation, and Bias Metadata files |
| **GPAI Systemic Risk** | Art. 51 pattern detection for General Purpose AI models |
| **Environment-Aware** | Auto-activates medical ruleset when `monai`, `tensorflow`, `torch` etc. detected in config files |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/RichradsY/ai-act-guardian.git
cd ai-act-guardian

# Install dependencies
pip install pyyaml

# Run on your own project
python compliance_engine.py
```

By default, the engine scans the current directory. A `CANONICAL_CERTIFICATE_<scan_id>.md` report is generated with all findings.

---

## 📋 Sample Output

```
🛡️ AI Act Guardian Canonical v15.0 | 9a75d5d9a620
✅ Final Report: CANONICAL_CERTIFICATE_9a75d5d9a620.md
```

```markdown
### ⚠️ ANTI-HALLUCINATION NOTICE
- Static analysis is a heuristic tool and NOT a legal guarantee.
- This engine cannot detect runtime injections, dynamic obfuscation, or downstream bias in black-box models.

| Severity  | File                                    | Line | Issue                                              |
|-----------|-----------------------------------------|------|----------------------------------------------------|
| 🛑 Critical | Experimental/vulnerable_medical_ai.py | 10   | Leak: 'patient_name' via 'print'                   |
| 🛑 Critical | Experimental/app_leaker.py            | 9    | Leak: 'data' via 'print' (cross-file taint)        |
| 🛑 Critical | Experimental/malicious_evasion.py     | 3    | Deception: AI disclosure flag explicitly disabled. |
| 🚩 High    | MVP/medical_ai_demo.py                | 2    | Art 14: Clinical decision missing HITL approval.   |
| 🚩 High    | GLOBAL                                | 0    | Art 11: Missing Technical Documentation.           |
```

---

## 🏗️ Architecture

```
compliance_engine.py          # Single-file engine, zero external deps beyond PyYAML
rules.yaml                    # Regulatory knowledge base (editable without code changes)
GEMINI.md                     # Engineering standards & anti-regression mandates

MVP/                          # Demo target: medical AI app (intentionally non-compliant)
  medical_ai_demo.py          # Missing HITL, exposes diagnostic logic
  medical_app.py              # MONAI-based cancer detection without doctor approval

Experimental/                 # Adversarial test suite
  vulnerable_medical_ai.py    # PII leak via print
  app_leaker.py               # Cross-file taint (imports from data_provider)
  data_provider.py            # Taint source (patient records + SSN)
  import_style_test.py        # Tests `import X; X.y()` taint tracking
  class_method_test.py        # Tests class method coverage
  hidden_evasion.py           # Variable rename evasion attempt
  malicious_evasion.py        # Art.52 deception + sanitization correctness
  tainted_medical_data.py     # Multi-hop taint propagation
  ultimate_test_arena.py      # Sanitization positive/negative combined test
```

### Two-Pass Engine Design

```
Pass 1 — pass1_index()
  Walk all .py files → build global_taint_index
  { "data_provider": {"get_patient_record", "global_ssn_data"}, ... }

Pass 2 — audit_file() per file
  ├── Resolve inherited taints from imports (from X import / import X)
  ├── For each FunctionDef (ast.walk, all levels):
  │     ├── LocalTaintVisitor.generic_visit()  → taint propagation + leak detection
  │     └── HITL check (Art. 14)
  └── audit_node_patterns_single()  → Art. 5/52/Annex III static matching
```

---

## 📜 Regulatory Coverage

| EU AI Act Article | Coverage | Method |
|---|---|---|
| Art. 5 — Prohibited Practices (a/b/c/d) | ✅ Pattern | Keyword matching on identifiers |
| Art. 9 — Risk Management System | ✅ Doc check | Requires `risk_registry.json` |
| Art. 10 — Data Governance / Bias | ✅ Conditional | Triggered by demographic variables |
| Art. 11 — Technical Documentation | ✅ Doc check | Requires `model_card.md` / `system_card.md` |
| Art. 14 — Human Oversight (HITL) | ✅ AST | Checks clinical function bodies |
| Art. 51 — GPAI Systemic Risk | ✅ Pattern | Compute threshold identifiers |
| Art. 52 — Transparency / Disclosure | ✅ AST | Detects adversarial flag suppression |
| GDPR / Art. 10 Health Data | ✅ Taint | Cross-file PII flow analysis |
| Annex III (§2–5) | ✅ Pattern | Infrastructure, Education, HR, Finance |
| Annex III (§6–8) | ⚠️ Partial | Migration, justice, democracy — in roadmap |
| Title VIII — GPAI Model Obligations | ⚠️ Partial | Art. 53–55 documentation requirements pending |

---

## 🗺️ Roadmap

- [ ] CLI interface with `argparse` for CI/CD pipeline integration
- [ ] SARIF output format (GitHub Code Scanning compatible)
- [ ] Annex III §6–8 rule coverage (migration, justice, democratic processes)
- [ ] Art. 13 transparency documentation checks
- [ ] `tree-sitter` backend for JavaScript/TypeScript support
- [ ] JSON Schema validation for `rules.yaml` contributor guide
- [ ] LLM-assisted semantic confirmation layer (reduce false positive rate)

---

## 🤝 Contributing

Contributions are welcome, especially:
- **New rules** in `rules.yaml` — no Python knowledge required
- **New test fixtures** in `Experimental/` — adversarial cases welcome
- **Bug reports** — please include the generated certificate

Before contributing code, read `GEMINI.md` — it documents the core engineering mandates that prevent recurring regressions.

---

## ⚖️ Legal Disclaimer

This tool performs **preliminary technical assessment only**. It is **not legal advice** and does not guarantee regulatory compliance. Final determination requires qualified legal counsel familiar with EU AI Act requirements.

As of August 2026, non-compliant High-Risk AI systems may face fines up to **€35,000,000 or 7% of global annual turnover**.

---

## 👥 Contributors

| Role | Contributor |
|---|---|
| Product & Architecture | [@RichradsY](https://github.com/RichradsY) |
| AI Engineering (Taint Engine, AST Analysis) | [Claude](https://claude.ai) (Anthropic) |
| AI Engineering (Rules & Adversarial Cases) | [Gemini](https://gemini.google.com) (Google) |

---

## 📄 License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

Permissive for commercial use, CI/CD integration, and derivative tools. Patent protection included.
