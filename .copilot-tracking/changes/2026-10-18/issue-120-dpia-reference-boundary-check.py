"""Prove bounded changes against the caller's exact base without reading live data."""

import ast
import hashlib
import subprocess
from pathlib import Path

BASE = "a86282c4badebc58eabbf9e441410d930a201ac2"
SOURCE = "src/api/src/zava_forward/api/timecapture.py"
TEST = "src/api/tests/test_timecapture.py"
README = "src/api/README.md"


def original(path):
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"])


def outside_status(raw):
    tree = ast.parse(raw)
    if isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
        tree.body.pop(0)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "TimeCapture":
            node.body = [method for method in node.body
                         if not isinstance(method, ast.FunctionDef) or method.name != "status"]
    return ast.dump(tree, include_attributes=False)


before = original(SOURCE)
after = Path(SOURCE).read_bytes()
assert outside_status(before) == outside_status(after)
print("PASS: all production AST outside status/module prose identical to exact base")
print("PASS: imports, SQL statements, DDL/constants, connection lifecycle, storage/dialect hooks unchanged")


def methods(raw):
    return {f"{node.name}.{method.name}": ast.dump(method, include_attributes=False)
            for node in ast.parse(raw).body if isinstance(node, ast.ClassDef)
            for method in node.body if isinstance(method, ast.FunctionDef)}


old_methods, new_methods = methods(original(TEST)), methods(Path(TEST).read_bytes())
assert all(new_methods.get(name) == body for name, body in old_methods.items())
added = sorted(set(new_methods) - set(old_methods))
assert len(added) == 7 and all(name.split(".")[1].startswith("test_") for name in added)
print("PASS: every existing test/class method unchanged; exactly seven added test methods")
for name in added:
    print(f"  {name}")

changed = subprocess.check_output(["git", "diff", "--name-only", BASE, "--", "src"]).decode().splitlines()
assert set(changed) == {SOURCE, TEST, README}, changed
print("PASS: exact three-file src boundary; no server/shared fixture/schema/web/runtime changes")
for path in (SOURCE, TEST, README):
    print(f"BASE SHA256 {hashlib.sha256(original(path)).hexdigest()} {path}")
    print(f"FINAL SHA256 {hashlib.sha256(Path(path).read_bytes()).hexdigest()} {path}")
