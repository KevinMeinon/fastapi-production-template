<div align="center">

# ⚡ FastAPI Production Template

**Battle-tested Python backend architecture — ready to ship.**

*By [Kevin Meinon](mailto:kevin@meinon.de) · Freelance Backend Engineer*

<br/>

[![CI](https://img.shields.io/github/actions/workflow/status/KevinMeinon/fastapi-production-template/ci.yml?branch=main&label=CI%2FCD&style=for-the-badge)](https://github.com/KevinMeinon/fastapi-production-template/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/github/actions/workflow/status/KevinMeinon/fastapi-production-template/tests.yml?branch=main&label=Tests&style=for-the-badge)](https://github.com/KevinMeinon/fastapi-production-template/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=for-the-badge)](https://github.com/KevinMeinon/fastapi-production-template/blob/main/pyproject.toml)
[![PyPI](https://img.shields.io/pypi/v/fastapi-production-template?style=for-the-badge&label=PyPI)](https://pypi.org/project/fastapi-production-template/)

<br/>

[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat-square&logo=terraform&logoColor=white)](https://www.terraform.io/)
[![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com/)
[![GCP](https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com/)
[![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/Ruff-46a758?style=flat-square)](https://github.com/astral-sh/ruff)

<br/>

**→ [Available for freelance projects](mailto:kevin@meinon.de?subject=FastAPI%20Freelance%20Inquiry) ←**

</div>

---

## About

I'm **Kevin Meinon**, a freelance backend engineer specialising in Python and production-grade API systems — primarily **FastAPI**, but equally at home with **Flask** and **Django** depending on what the project calls for.

This template is a living showcase of the architecture patterns and engineering standards I bring to every engagement — not boilerplate to fill in, but a reference for what production-ready actually looks like.

**What I build:**
- High-throughput REST & async APIs with clean domain separation
- End-to-end CI pipelines with strict quality gates (lint, types, coverage)
- Cloud-portable infrastructure baselines (AWS / Azure / GCP)
- Systems that are easy for your team to own after I'm done

If your team needs a backend that ships fast and holds up — [let's talk](mailto:kevin@meinon.de).

---

## What this demonstrates

| Concern | Approach |
|---|---|
| **Architecture** | App factory, versioned routes, repository pattern, domain layer separation — framework-agnostic patterns that port cleanly to Flask or Django |
| **Data layer** | SQLAlchemy async ORM + asyncpg + dependency-injected sessions |
| **Auth** | API key middleware (`X-API-Key`) with per-route enforcement |
| **Observability** | Structured JSON logging, request ID propagation, Prometheus-style metrics |
| **Quality** | 100% coverage gate, Ruff linting, Pyrefly type checking, pre-commit hooks |
| **Infrastructure** | Terraform modules for ECR (AWS), ACR (Azure), GAR (GCP) |
| **Dev experience** | Docker Compose with hot-reload dev profile, full local parity |

---

## Tech stack

- **Runtime:** Python 3.14
- **Framework:** FastAPI + Pydantic v2 · Flask · Django
- **Database:** PostgreSQL · SQLAlchemy async · asyncpg
- **Tooling:** uv · Ruff · Pyrefly · pytest · tox
- **Infrastructure:** Docker · Docker Compose · Terraform (AWS / Azure / GCP)
- **CI/CD:** GitHub Actions

> The FastAPI layer is intentionally thin and architecturally isolated — swapping it for Flask or Django is a configuration change, not a rewrite.

---

## API surface
```
GET    /api/v1/health                       # public
GET    /api/v1/metrics                      # public
POST   /api/v1/documents/analyze            # requires X-API-Key
POST   /api/v1/documents                    # requires X-API-Key
GET    /api/v1/documents                    # requires X-API-Key
GET    /api/v1/documents/{document_id}      # requires X-API-Key
PUT    /api/v1/documents/{document_id}      # requires X-API-Key
DELETE /api/v1/documents/{document_id}      # requires X-API-Key
```

---

## Local development
```bash
uv sync --all-groups
uv run uvicorn fastapi_production_template.main:app --reload
```
```bash
curl -H "X-API-Key: dev-api-key" http://localhost:8000/api/v1/documents
```

## Quality gates
```bash
uv run pytest          # tests + coverage
uv run ruff check .    # linting
uv run pyrefly check . # type checking
uv run tox             # full gate
```
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

## Docker
```bash
docker compose up --build

# Dev profile with hot reload
docker compose --profile dev up --build --watch api-dev postgres
```

## Using this template

Click **Use this template** on GitHub, then:

1. Rename the package: `src/fastapi_production_template/` -> `src/<your_package>/`, and update
   `name`, `description` and `authors` in `pyproject.toml` plus every import and the
   `uvicorn <your_package>.main:app` commands (README, Dockerfile, compose.yml, CI).
2. Delete what you do not need: unused `infra/terraform-*` stacks, the PyPI `publish-pypi` job
   (it only runs on `v*` tags, so leaving it in place is safe), or the personal branding sections
   in this README.
3. Set your own secrets: `API_KEY` in `.env` / compose, real Postgres credentials.
4. `uv sync --all-groups && uv run tox` to confirm the gates pass on your machine.

## Terraform
```bash
terraform -chdir=infra/terraform-aws   init && validate
terraform -chdir=infra/terraform-azure init && validate
terraform -chdir=infra/terraform-gcp   init && validate
```

---

<div align="center">

## Hire me

**I'm available for backend contracts and freelance projects.**

Backend feature delivery · API performance & reliability · CI quality gates · Cloud deployment

[kevin@meinon.de](mailto:kevin@meinon.de?subject=Backend%20Project%20Inquiry)

</div>