#!/usr/bin/env python3
"""Smoke test: run extract_cites sequentially on first N rows of PMC_OA_meta.csv and write a small JSON.
"""
import os
import json
import pandas as pd
import importlib.util

# Load extract_PMC_cites module by file path to avoid import errors
script_dir = os.path.dirname(__file__)
module_path = os.path.join(script_dir, "extract_PMC_cites.py")
spec = importlib.util.spec_from_file_location("extract_PMC_cites", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
extract_cites = mod.extract_cites
data_dir = mod.data_dir

N = 100
meta_path = os.path.join(data_dir, "PMC_OA_meta.csv")
print("Reading meta from:", meta_path)
file_list = pd.read_csv(meta_path)

msgs = [(file_list['file_path'].iloc[i], str(file_list['PMID'].iloc[i])) for i in range(min(N, len(file_list)))]

results = []
for msg in msgs:
    PMID, cites = extract_cites(msg)
    if cites:
        results.append({"PMID": PMID, "cites": cites})

out_path = os.path.join(data_dir, "PMC_cites_smoke.json")
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Wrote {len(results)} entries to {out_path}")
