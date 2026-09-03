#!/usr/bin/env python3
"""Führt alle Codezellen des Setup-Notebooks ohne separaten Kernel aus."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "00_setup_check.ipynb"


def source_text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else source


def execute_cell(source: str, namespace: dict) -> None:
    tree = ast.parse(source, mode="exec")
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        leading = ast.Module(body=tree.body[:-1], type_ignores=[])
        if leading.body:
            exec(compile(leading, "<setup-notebook>", "exec"), namespace)
        eval(compile(ast.Expression(tree.body[-1].value), "<setup-notebook>", "eval"), namespace)
    else:
        exec(compile(tree, "<setup-notebook>", "exec"), namespace)


def main() -> None:
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    namespace = {"__name__": "__main__"}
    previous_directory = Path.cwd()
    executed = 0
    os.chdir(ROOT)
    try:
        for cell in notebook["cells"]:
            if cell.get("cell_type") != "code":
                continue
            execute_cell(source_text(cell), namespace)
            executed += 1
    finally:
        os.chdir(previous_directory)

    if executed != 3:
        raise SystemExit(f"3 Codezellen erwartet, ausgeführt: {executed}")
    print(f"SETUP NOTEBOOK OK: {executed} Codezellen")


if __name__ == "__main__":
    main()

