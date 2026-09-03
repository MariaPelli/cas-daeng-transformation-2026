#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="cas-daeng-transformation"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

if command -v mamba >/dev/null 2>&1; then
  ENV_MANAGER="mamba"
else
  ENV_MANAGER="conda"
fi

if conda run -n "$ENV_NAME" python --version >/dev/null 2>&1; then
  "$ENV_MANAGER" env update -n "$ENV_NAME" -f environment.yml --prune
else
  "$ENV_MANAGER" env create -f environment.yml
fi

conda run -n "$ENV_NAME" python -m ipykernel install --user \
  --name "$ENV_NAME" \
  --display-name "Python (CAS DAENG Transformation)"

# Neue Terminals aktivieren das Workshop-Environment automatisch. Die Marker
# halten den Schritt bei einem Container-Neubau idempotent.
for RC_FILE in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [[ -f "$RC_FILE" ]] && ! grep -Fq "# CAS DAENG Transformation" "$RC_FILE"; then
    {
      printf '\n# CAS DAENG Transformation\n'
      printf 'source "$(conda info --base)/etc/profile.d/conda.sh"\n'
      printf 'conda activate cas-daeng-transformation\n'
    } >> "$RC_FILE"
  fi
done

conda run --no-capture-output -n "$ENV_NAME" python scripts/verify_setup.py

