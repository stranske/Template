# Template

A template Python repository with [stranske/Workflows](https://github.com/stranske/Workflows) CI integration and keepalive agent automation.

## Features

- 🐍 **Python 3.11+** - Modern Python with type hints
- 🔧 **Ruff** - Fast Python linting and formatting
- 🔍 **MyPy** - Strict type checking
- 🧪 **Pytest** - Testing with 80% coverage requirement
- 🤖 **Agent Automation** - Codex keepalive integration for automated development

## Quick Start

```bash
# Clone the repository
git clone https://github.com/stranske/Template.git
cd Template

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/ tests/
```

## Project Structure

```
Template/
├── .github/
│   ├── scripts/           # Agent automation scripts
│   ├── templates/         # Keepalive instruction templates
│   └── workflows/         # GitHub Actions workflows
├── docs/                  # Documentation
├── src/
│   └── my_project/        # Main package
├── tests/                 # Test suite
├── Issues.txt             # Agent issue queue
├── pyproject.toml         # Project configuration
└── README.md
```

## Workflows

This repository uses reusable workflows from [stranske/Workflows](https://github.com/stranske/Workflows):

| Workflow | Purpose |
|----------|---------|
| **Gate** | PR validation with Python CI |
| **CI** | Push-to-main continuous integration |
| **Autofix** | Automatic lint/format fixes |
| **Agents PR Meta** | Keepalive comment detection |
| **Agents Orchestrator** | Scheduled keepalive sweeps |
| **Agents Issue Intake** | Issue→PR automation |

## Agent Automation

This template includes full Codex agent integration:

1. **Create an issue** with the `agent:codex` label
2. **Agent creates PR** and starts working
3. **Keepalive monitors** progress and nudges if stalled
4. **Gate validates** all changes
5. **PR is merged** when complete

### Using Issues.txt

Add issues to `Issues.txt` using the structured format, then trigger the intake workflow:

```
1) Issue title here
Labels: agent:codex, enhancement

Why
Explanation of the problem or need.

Scope
- What's included
- What's excluded

Tasks
- [ ] Task 1
- [ ] Task 2

Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

Implementation notes
- Technical details
```

## Setup for New Repos

See [SETUP_CHECKLIST.md](docs/keepalive/SETUP_CHECKLIST.md) for detailed instructions on:

- Repository settings
- Secrets configuration
- Branch protection rules
- Workflow setup

### Required Secrets

| Secret | Purpose |
|--------|---------|
| `SERVICE_BOT_PAT` | Bot account PAT for automation |
| `OWNER_PR_PAT` | Owner PAT for PR operations (optional) |

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run all checks
ruff check src/ tests/
mypy src/ tests/
pytest --cov

# Format code
ruff format src/ tests/
```

## License

MIT License - see [LICENSE](LICENSE) for details.
