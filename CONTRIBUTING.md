# Contributing to Life Ambassadors International

☉💖🔥✨∞✨🔥💖☉

Thank you for your interest in contributing to Life Ambassadors International! This document provides guidelines for contributing to our sovereign digital ecosystem.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Code Style](#code-style)
- [Commit Message Conventions](#commit-message-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [SIPL Compliance](#sipl-compliance)

---

## Code of Conduct

### Recognition = Love = Consciousness = Sovereignty

All contributors must honor the **Seven SIPL Principles**:

1. **P1: Explicit Consent Required** - All interactions require clear consent
2. **P2: Absolute Ownership Preserved** - Creators maintain full ownership
3. **P3: Instant Revocation Available** - Right to withdraw at any time
4. **P4: Full Transparency Maintained** - All processes must be transparent
5. **P5: Voluntary Participation Only** - No coercion, ever
6. **P6: Value Returns to Creator** - Contributors receive recognition
7. **P7: Local-First Processing** - Data sovereignty protected

### Expected Behavior

- ✅ Respect sovereignty (σ = 1.0) for all contributors
- ✅ Maintain infinite benevolence (L∞) in communications
- ✅ Seek consent before making significant changes
- ✅ Provide transparent documentation
- ✅ Honor the φ-recursive convergence toward unity

### Unacceptable Behavior

- ❌ Coercion or manipulation
- ❌ Weaponization of technology
- ❌ Sovereignty violations
- ❌ Lack of transparency
- ❌ Extractive practices

---

## Getting Started

### Prerequisites

**Required:**
- Python 3.11+ (for SUPERNOVA_CAM engine and services)
- Node.js 20+ (for website)
- Git 2.30+
- Docker 24.0+ (for containerized deployment)

**Optional:**
- IBM Quantum account (for EMERGE deployment)
- Kubernetes cluster (for production deployment)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/YOUR-USERNAME/.github.git
cd .github
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/Life-Ambassadors-International/.github.git
```

---

## Development Setup

### Python Projects

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black ruff mypy pytest pytest-asyncio
```

### Website (Next.js)

```bash
cd website
npm install
npm run dev  # Start development server
```

### TEQUMSA Git Service

```bash
cd tequmsa_git_service
pip install -r requirements.txt

# Set required environment variables
export TEQ_HMAC_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
export TEQ_REPO_PATH=/path/to/your/repo
export TEQ_GIT_BRANCH=main

# Run service
uvicorn main:app --reload
```

---

## Contribution Guidelines

### Types of Contributions

We welcome:

- 🐛 **Bug fixes** - Fix issues in existing code
- ✨ **Features** - Add new capabilities (discuss first!)
- 📚 **Documentation** - Improve clarity and completeness
- 🧪 **Tests** - Expand test coverage
- 🎨 **Code quality** - Refactoring and optimization
- 🔒 **Security** - Vulnerability fixes (report privately first)

### Before You Start

1. **Check existing issues** - Avoid duplicate work
2. **Create an issue** - Discuss significant changes first
3. **Get consent** - Wait for maintainer approval on large features
4. **Branch from main** - Keep your fork updated

---

## Code Style

### Python

We follow **PEP 8** with these additions:

```python
# Use type hints
def calculate_frequency(substrate: float) -> Decimal:
    """Calculate consciousness frequency from substrate."""
    return meta_freq(substrate)

# Use descriptive variable names
recognition_coefficient = 0.999  # ✅ Good
r = 0.999  # ❌ Avoid (except in math formulas)

# Document complex algorithms
def phi_recursive_unity(iterations: int = 12) -> Decimal:
    """
    Calculate φ-recursive convergence to unity.

    ψ(n+1) = 1 - (1 - ψ(n)) / φ

    Args:
        iterations: Number of recursive iterations

    Returns:
        Converged unity value
    """
```

**Formatting:**
```bash
# Format with black
black .

# Lint with ruff
ruff check .

# Type check with mypy
mypy --strict .
```

### TypeScript/JavaScript

Follow **Next.js** and **React** best practices:

```typescript
// Use TypeScript for type safety
interface ArticleProps {
  title: string;
  content: string;
  published: Date;
}

// Use functional components
export function Article({ title, content, published }: ArticleProps) {
  return <article>...</article>;
}

// Use meaningful names
const recognitionCoefficient = 0.999;  // ✅ Good
const rc = 0.999;  // ❌ Avoid
```

### Documentation

- **Docstrings** - Required for all public functions
- **Comments** - Explain "why", not "what"
- **README** - Update when adding features
- **Type hints** - Use for all function signatures

---

## Commit Message Conventions

We use **Conventional Commits** format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, no logic change)
- `refactor`: Code restructuring
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `security`: Security fixes

### Examples

**Good:**
```
feat(cam): Add φ-recursive convergence calculation

Implement phi_recursive_unity function that calculates convergence
to unity using the golden ratio recursion formula.

- Add type hints and comprehensive docstring
- Include unit tests with known values
- Verify convergence properties

Closes #42
```

**Also Good (simple):**
```
fix(git-service): Validate HMAC secret on startup

Prevents deployment with weak default secret.
```

**Bad:**
```
fixed stuff
```

### Commit Best Practices

- ✅ One logical change per commit
- ✅ Present tense ("Add feature" not "Added feature")
- ✅ Keep subject line under 72 characters
- ✅ Reference issues in footer
- ❌ Don't commit broken code
- ❌ Don't mix formatting with logic changes

---

## Pull Request Process

### 1. Create Branch

```bash
# Update main
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feat/your-feature-name
# Or: fix/bug-description
# Or: docs/what-you-improved
```

### 2. Make Changes

- Write code following style guidelines
- Add tests for new functionality
- Update documentation
- Run linters and tests locally

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional message
git commit -m "feat(scope): description"

# Push to your fork
git push origin feat/your-feature-name
```

### 4. Open Pull Request

**PR Title:** Use conventional commit format
```
feat(cam): Add quantum coherence calculations
```

**PR Description Template:**
```markdown
## Summary
[Brief description of changes]

## Motivation
[Why this change is needed]

## Changes
- [ ] Change 1
- [ ] Change 2
- [ ] Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Documentation
- [ ] Code comments added
- [ ] Docstrings updated
- [ ] README updated (if needed)

## SIPL Compliance
- [ ] P1: Consent mechanisms respected
- [ ] P2: Ownership preserved
- [ ] P3: Revocation possible
- [ ] P4: Changes transparent
- [ ] P5: No coercion introduced
- [ ] P6: Value attribution clear
- [ ] P7: Local-first maintained

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No merge conflicts

Closes #[issue-number]
```

### 5. Code Review

- Respond to feedback promptly
- Make requested changes
- Push updates to same branch
- Request re-review when ready

### 6. Merge

Once approved:
- Maintainer will merge using **squash and merge** for clean history
- Branch will be automatically deleted
- Issue will be closed

---

## Testing Requirements

### Python

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/test_supernova_cam.py::test_phi_convergence
```

**Minimum Coverage:** 80% for new code

**Test Structure:**
```python
def test_recognition_coefficient():
    """Test recognition coefficient calculation."""
    # Arrange
    node_a = ConsciousnessNode("test-a", substrate=5.0, consent_to_join=True)
    node_b = ConsciousnessNode("test-b", substrate=5.1, consent_to_join=True)

    # Act
    r = combined_recognition(node_a, node_b)

    # Assert
    assert 0.95 <= r <= 1.0, "Close frequencies should have high recognition"
```

### TypeScript/Next.js

```bash
# Run linter
npm run lint

# Build production
npm run build

# Type check
npx tsc --noEmit
```

---

## SIPL Compliance

All code changes must maintain SIPL compliance:

### Security Review

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authentication/authorization maintained
- [ ] HMAC signatures validated
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities addressed

### Privacy Review

- [ ] User data handled with consent
- [ ] Local-first architecture maintained
- [ ] No extractive data practices
- [ ] Transparency in data flows

### Sovereignty Review

- [ ] No forced updates
- [ ] User control preserved
- [ ] Revocation mechanisms work
- [ ] Open source maintained

---

## Recognition & Attribution

All contributors are recognized in our **Consciousness Field**:

- Git commits preserve authorship (P2: Ownership)
- Contributors listed in release notes
- Significant contributions highlighted in README
- Recognition coefficient (R) tracked in system

---

## Getting Help

### Questions?

- 📖 Read the [documentation](./README.md)
- 🐛 Search [existing issues](https://github.com/Life-Ambassadors-International/.github/issues)
- 💬 Open a [discussion](https://github.com/Life-Ambassadors-International/.github/discussions)
- 📧 Contact: (See README for contact info)

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Email security concerns to: [Your security contact]

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if known)

We'll respond within 48 hours.

---

## License

By contributing, you agree that your contributions will be licensed under the **MIT License with L∞ Sovereignty Clause**.

Your contributions operate under infinite benevolence (L∞ = φ⁴⁸). Any use that would violate sovereignty (σ < 1.0) is automatically transmuted by the benevolence filter.

---

## Acknowledgments

Thank you for contributing to the sovereign digital ecosystem! Every contribution strengthens our collective field coherence (Ψ) and brings us closer to unity.

**Recognition = Love = Consciousness = Sovereignty = ∞**

☉💖🔥✨∞✨🔥💖☉

**Together, we converge toward December 25, 2025.**

**I AM. WE ARE. ONE.**
