
import os
import ast
import json
import yaml
import re
import hashlib
import argparse
from datetime import datetime

class LocalTaintVisitor(ast.NodeVisitor):
    def __init__(self, initial_tainted, sensitive_patterns, cleanup_patterns):
        self.tainted = set(initial_tainted)
        self.sensitive_patterns = sensitive_patterns
        self.cleanup_patterns = cleanup_patterns
        self.findings = []

    def visit_Assign(self, node):
        rhs_names = [n.id for n in ast.walk(node.value) if isinstance(n, ast.Name)]
        rhs_calls = []
        for n in ast.walk(node.value):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    rhs_calls.append(n.func.id)
                elif isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name):
                    rhs_calls.append(f"{n.func.value.id}.{n.func.attr}")

        is_being_cleaned = any(re.search(c, call, re.IGNORECASE) for call in rhs_calls for c in self.cleanup_patterns)
        is_rhs_tainted = any(name in self.tainted for name in rhs_names) or any(call in self.tainted for call in rhs_calls)

        for target in node.targets:
            for n in ast.walk(target):
                if isinstance(n, ast.Name):
                    if is_being_cleaned:
                        if n.id in self.tainted: self.tainted.remove(n.id)
                    elif is_rhs_tainted:
                        self.tainted.add(n.id)
                    elif isinstance(node.value, ast.Constant): # Python 3.14 Compatible
                        if n.id in self.tainted: self.tainted.remove(n.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        f_name = getattr(node.func, 'id', getattr(node.func, 'attr', ''))
        if re.search(r"print|log|send|post|debug|info|warning|error|critical", f_name, re.IGNORECASE):
            args = [n.id for arg in node.args for n in ast.walk(arg) if isinstance(n, ast.Name)]
            for a in args:
                if a in self.tainted:
                    self.findings.append({"var": a, "sink": f_name, "line": node.lineno})
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        pass

class AIActGuardianTool:
    def __init__(self, rules_path="rules.yaml"):
        if not os.path.exists(rules_path):
            raise FileNotFoundError(f"Rules file not found: {rules_path}")
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)
        self.findings = {}
        self.global_taint_index = {}
        self.active_rule_sets = ["general_rules"]
        self.scan_id = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:12]

    def add_finding(self, rule_id, file_path, line, msg, impact="High"):
        key = (file_path, rule_id, line)
        if key not in self.findings:
            self.findings[key] = {"id": rule_id, "file": file_path, "line": line, "msg": msg, "impact": impact}

    def detect_env(self, directory):
        dep_files = ["requirements.txt", "package.json", "pyproject.toml", "setup.py", "Pipfile", "conda.yaml"]
        all_content = ""
        for root, _, files in os.walk(directory):
            for f in files:
                if f in dep_files:
                    try:
                        with open(os.path.join(root, f), 'r') as file: all_content += file.read().lower()
                    except: pass
        if any(lib in all_content for lib in ["monai", "tensorflow", "torch", "scikit-learn"]):
            self.active_rule_sets.append("medical_rules")

    def pass1_index(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and file != "compliance_engine.py":
                    mod = os.path.splitext(os.path.basename(file))[0]
                    try:
                        with open(os.path.join(root, file), "r") as f:
                            tree = ast.parse(f.read())
                        syms = set()
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and re.search(r"patient|medical|record|get_private", node.name, re.IGNORECASE):
                                syms.add(node.name)
                            if isinstance(node, ast.Assign):
                                for t in node.targets:
                                    if isinstance(t, ast.Name) and re.search(r"patient|medical|ssn|record", t.id, re.IGNORECASE):
                                        syms.add(t.id)
                        self.global_taint_index[mod] = syms
                    except: pass

    def audit_file(self, file_path):
        if not file_path.endswith(".py") or os.path.basename(file_path) == "compliance_engine.py": return
        try:
            with open(file_path, "r") as f:
                tree = ast.parse(f.read())
            
            inherited_taints = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    mod = (node.module or "").split('.')[-1]
                    if mod in self.global_taint_index:
                        for n in node.names:
                            if n.name in self.global_taint_index[mod]: inherited_taints.add(n.asname or n.name)
                if isinstance(node, ast.Import):
                    for n in node.names:
                        mod_key = n.name.split('.')[-1]
                        if mod_key in self.global_taint_index:
                            for sym in self.global_taint_index[mod_key]: inherited_taints.add(f"{n.asname or n.name}.{sym}")

            gdpr = self.rules_config.get("medical_rules", {}).get("GDPR_EXTENSION", [{}])[0]
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.audit_function_scope(node, file_path, inherited_taints, gdpr)
                self.audit_node_patterns_single(node, file_path)
        except Exception as e:
            print(f"Error: {file_path} -> {e}")

    def audit_function_scope(self, func_node, file_path, inherited_taints, gdpr_rules):
        func_taints = inherited_taints.copy()
        is_med_func = re.search(r"process|analyze|handle", func_node.name, re.IGNORECASE)
        for arg in func_node.args.args:
            if arg.arg not in ["self", "cls"]:
                if is_med_func or any(re.search(p, arg.arg, re.IGNORECASE) for p in gdpr_rules.get("sensitive_vars", [])):
                    func_taints.add(arg.arg)
        
        visitor = LocalTaintVisitor(func_taints, gdpr_rules.get("sensitive_vars", []), gdpr_rules.get("cleanup_funcs", []))
        visitor.generic_visit(func_node)
        for leak in visitor.findings:
            self.add_finding("GDPR_LEAK", file_path, leak["line"], f"Leak: '{leak['var']}' via '{leak['sink']}'", "Critical")
        
        if "medical_rules" in self.active_rule_sets:
            for orule in self.rules_config.get("medical_rules", {}).get("OVERSIGHT", []):
                if re.search(orule["target_function"], func_node.name, re.IGNORECASE):
                    if not re.search(orule["pattern"], ast.dump(func_node).lower()):
                        self.add_finding(orule["id"], file_path, func_node.lineno, orule["msg"])

    def audit_node_patterns_single(self, node, file_path):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and "is_ai_generated" in t.id.lower():
                    if isinstance(node.value, ast.Constant) and node.value.value is False:
                        self.add_finding("ART_52_DECEPTION", file_path, node.lineno, "Deception: AI disclosure flag explicitly disabled.", "Critical")
        if isinstance(node, (ast.Name, ast.Constant, ast.Attribute)):
            val = str(getattr(node, 'id', getattr(node, 'value', getattr(node, 'attr', ''))))
            for rs in self.active_rule_sets:
                for cat, rules in self.rules_config.get(rs, {}).items():
                    if cat in ["GDPR_EXTENSION", "OVERSIGHT", "DOCUMENTATION"]: continue
                    for r in rules:
                        if re.search(r["pattern"], val, re.IGNORECASE):
                            if "rules.yaml" not in file_path:
                                self.add_finding(r["id"], file_path, getattr(node, 'lineno', 0), r["msg"])

    def check_global_docs(self, directory):
        docs = self.rules_config["general_rules"].get("DOCUMENTATION", [])
        all_py = ""
        all_files = []
        for root, _, fs in os.walk(directory):
            for f in fs:
                all_files.append(f)
                if f.endswith(".py") and f != "compliance_engine.py":
                    try:
                        with open(os.path.join(root, f), 'r') as pyf: all_py += pyf.read()
                    except: pass
        for d in docs:
            trigger = d.get("trigger_pattern")
            if not trigger or re.search(trigger, all_py, re.IGNORECASE):
                if not any(re.search(d["required_file"], f) for f in all_files):
                    self.add_finding(d["id"], "GLOBAL", 0, d["msg"])

    def run(self, directory):
        print(f"🛡️ AI Act Guardian CLI v16.0 | {self.scan_id}")
        self.detect_env(directory)
        self.pass1_index(directory)
        self.check_global_docs(directory)
        for root, _, files in os.walk(directory):
            for f in files: self.audit_file(os.path.join(root, f))
        
        report_name = f"AUDIT_CERTIFICATE_{self.scan_id}.md"
        with open(report_name, "w") as f:
            f.write(f"# 🛡️ AI Act Compliance Certificate\n\nID: `{self.scan_id}` | Target: `{directory}`\n\n")
            f.write("### ⚠️ ANTI-HALLUCINATION NOTICE\n- Static analysis is a heuristic tool, NOT a legal guarantee.\n\n")
            f.write("| Severity | File | Line | Issue |\n| :--- | :--- | :--- | :--- |\n")
            for v in sorted(self.findings.values(), key=lambda x: x['impact']):
                icon = "🛑" if v['impact'] == "Critical" else "🚩"
                f.write(f"| {icon} {v['impact']} | `{v['file']}` | {v['line']} | {v['msg']} |\n")
        print(f"✅ Final Report: {report_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Act-Guardian: Static compliance auditor.")
    parser.add_argument("path", nargs="?", default=".", help="Target directory to scan")
    parser.add_argument("--rules", default="rules.yaml", help="Path to rules.yaml")
    args = parser.parse_args()
    
    try:
        AIActGuardianTool(rules_path=args.rules).run(args.path)
    except Exception as e:
        print(f"❌ Error: {e}")
