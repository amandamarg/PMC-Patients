#!/usr/bin/env bash
# Simple runner to execute extract_PMC_cites.py using the project venv python from repo root
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)/.."
VENV_PY="$REPO_ROOT/.venv/bin/python"
SCRIPT="$REPO_ROOT/code/PMC-Patients_collection/PMC_OA_utils/extract_PMC_cites.py"

cd "$REPO_ROOT" || exit 1
exec "$VENV_PY" "$SCRIPT"
