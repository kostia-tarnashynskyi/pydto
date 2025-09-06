# Pydto Development Commands

# Default: show help
default:
	@echo "Pydto Development Commands"
	@echo "========================="
	@echo ""
	@echo "Core:"
	@echo "  just test       # Run tests"
	@echo "  just lint       # Check code quality"
	@echo "  just format     # Format code"
	@echo "  just build      # Build package"
	@echo "  just clean      # Clean artifacts"
	@echo ""
	@echo "Setup:"
	@echo "  just install    # Install dependencies"
	@echo "  just update     # Update dependencies"
	@echo ""
	@echo "Tasks:"
	@echo "  just tasks      # Show current tasks"
	@echo ""
	@echo "Workflows:"
	@echo "  just dev        # Development workflow"
	@echo "  just ci         # CI check"


pre-commit:
    @echo "Running pre-commit hooks"
    uv run pre-commit run --all-files

# Test
test:
	@echo "Running tests"
	uv run pytest tests/

# Test with coverage
test-cov:
	@echo "Running tests with coverage"
	uv run pytest tests/ --cov=src --cov-report=html

# Lint
lint:
	@echo "Linting code"
	uv run ruff check src/ tests/

# Format
format:
	@echo "Formatting code"
	uv run ruff format src/ tests/

# Type check
type-check:
	@echo "Type checking"
	uv run pyright src/

# Build package
build:
	@echo "Building package"
	uv build

# Clean artifacts
clean:
	@echo "Cleaning up"
	rm -rf dist/ .coverage htmlcov/ .pytest_cache/ .mypy_cache/ .ruff_cache/

# Install dependencies
install:
	@echo "Installing dependencies"
	uv sync --all-extras

# Update dependencies
update:
	@echo "Updating dependencies"
	uv lock --upgrade

# CI check
ci:
	@echo "Running CI check"
	just lint
	just type-check
	just test-cov
	just build
	@echo "CI check complete"

# Show project info
info:
	@echo "Pydto Project Info"
	@echo "================="
	@echo ""
	@echo "Project structure:"
	@find src/ -name "*.py" -type f | head -5
	@echo ""
	@echo "Test files:"
	@find tests/ -name "*.py" -type f | head -3
