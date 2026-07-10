# PDF Merger API

A REST API that accepts multiple PDF files and merges them into a single PDF, returned as a binary stream. Built as a portfolio project with a focus on production-grade practices: typed configuration, structured logging, rate limiting, containerised deployment, and infrastructure as code.

**Live:** [Swagger UI](https://ca-pdf-merger-production.icyrock-1ab134ed.uksouth.azurecontainerapps.io/api/docs) · Deployed on Azure Container Apps

---

## API Reference

### `POST /api/merge/`

Accepts a multipart form upload of two or more PDF files and returns a merged PDF as a binary stream.

**Request**

| Field | Type | Required | Description |
|---|---|---|---|
| `files` | `UploadFile[]` | Yes | Two or more PDF files to merge, in order |
| `filename` | `string` | No | Base name for the returned file (default: `merged`) |

**Response**

| Status | Content-Type | Description |
|---|---|---|
| `200 OK` | `application/pdf` | The merged PDF, returned as an attachment |

The `Content-Disposition` header is set to `attachment; filename=<filename>.pdf`.

**Example**

```bash
curl -X POST \
  https://ca-pdf-merger-production.icyrock-1ab134ed.uksouth.azurecontainerapps.io/api/merge/ \
  -F "files=@first.pdf" \
  -F "files=@second.pdf" \
  -F "filename=combined" \
  --output combined.pdf
```

**Rate limiting** is applied per IP address. The default limit is configurable via environment variable.

---

## Tech Stack

### Application

| Technology | Role |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework, with application factory pattern and service layer |
| [pypdf](https://pypdf.readthedocs.io/) | In-memory PDF merging |
| [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) | Typed, environment-aware configuration |
| [slowapi](https://github.com/laurentS/slowapi) | Rate limiting |
| [python-json-logger](https://github.com/madzak/python-json-logger) | Structured JSON logging |
| [pytest](https://pytest.org/) | Testing |

### Infrastructure & CI/CD

| Technology | Role |
|---|---|
| [Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/) | Hosting (test + production environments) |
| [Terraform](https://www.terraform.io/) | Infrastructure as code, with remote state in Azure Blob Storage |
| [GitHub Actions](https://github.com/features/actions) | CI/CD pipeline |
| [GHCR](https://ghcr.io/) | Container image registry |
| Docker | Local development and production runtime |

---

## Infrastructure Overview

The project runs across two isolated environments — **test** and **production** — both hosted on Azure Container Apps.

Infrastructure is managed entirely with Terraform, with separate state files per environment stored in Azure Blob Storage. This prevents Terraform from treating differences between environments as drift to resolve, which would risk destructive cross-environment operations.

**Pipeline flow:**

- **Push to `main`** → builds a Docker image tagged with the commit SHA → automatically deploys to the test environment
- **GitHub Release** → retags the image with the version → deploys to production, gated by a manual approval step

Authentication between GitHub Actions and Azure uses **OIDC federation**, meaning no long-lived credentials or secrets are stored. GitHub Actions assumes an Azure identity at runtime via a federated credential scoped to each environment.

---

## Local Development

Docker is the only supported local runtime, matching the production environment exactly.

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/pdf-merger.git
cd pdf-merger
```

**2. Create a `.env` file**

```env
ENV=development
RATE_LIMIT=10/minute
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

| Variable | Description |
|---|---|
| `ENV` | Application environment (`development` / `production`) |
| `RATE_LIMIT` | Rate limit applied per IP (e.g. `10/minute`, `100/hour`) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins |

**3. Build and run**

```bash
docker build -t pdf-merger .
docker run --env-file .env -p 8000:8000 pdf-merger
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/api/docs`.

---

## Notable Technical Decisions

A few non-obvious problems that shaped the implementation:

**PDF merging requires a proper library.** Naively concatenating PDF bytes does not produce a valid PDF — the format has internal structure (cross-reference tables, object graphs) that must be rebuilt. `pypdf` handles this correctly and operates entirely in memory, with no temporary files written to disk.

**CORS origins need a custom validator.** `pydantic-settings` pre-parses fields typed as `list[str]` before validators run. Storing `CORS_ALLOWED_ORIGINS` as a comma-separated string (the natural format for an environment variable) requires a `field_validator` with `mode='before'` to intercept the raw string before pydantic attempts its own parsing.

**Azure intercepts FastAPI's trailing slash redirects.** FastAPI redirects `POST /merge` → `POST /merge/` by default, returning a `307`. Azure Container Apps intercepts this redirect and returns a `405 Method Not Allowed`. The fix is to register both paths on the same handler using the double decorator pattern — one without a trailing slash (excluded from the schema) and one with.

**Terraform state must be isolated per environment.** A single shared state file would cause Terraform to see test and production as divergence from a single desired state, risking destructive operations. Separate state files (`pdf-merger-test.tfstate`, `pdf-merger-production.tfstate`) give each environment its own source of truth.