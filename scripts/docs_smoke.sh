#!/usr/bin/env bash
set -euo pipefail

uv sync --all-groups

# Smoke-check command examples from README without starting long-running services.
uv run uvicorn fastapi_production_template.main:app --help >/dev/null
uv run pytest --help >/dev/null
uv run ruff check . --statistics >/dev/null
uv run pyrefly check . >/dev/null
uv run tox --help >/dev/null

terraform -chdir=infra/terraform-aws fmt -check
terraform -chdir=infra/terraform-azure fmt -check
terraform -chdir=infra/terraform-gcp fmt -check
