# Framework Organization

This project is organized according to a structured framework with five main categories that ensure best practices, maintainability, and clarity.

## 1. Documentation 📚

**Purpose**: Written explanations and guides that help users understand and use the project.

### Files:
- **README.md**: Main project documentation with setup instructions, usage guide, and feature overview
- **ARCHITECTURE.md**: System architecture, component design, data flow, and technology stack
- **CONTRIBUTING.md**: Guidelines for contributors, development workflow, and code standards
- **CHANGELOG.md**: Version history tracking all notable changes
- **docs/CODE_QUALITY.md**: Code quality standards, type hints, docstrings, and best practices
- **docs/ENVIRONMENT_SETUP.md**: Detailed environment setup and dependency management guide
- **docs/README.md**: Documentation index

### Best Practices:
- Clear, concise writing
- Code examples where applicable
- Step-by-step instructions
- Regular updates with changes

---

## 2. Repository Structure 📁

**Purpose**: Organization of directories and files within the repository.

### Structure:
```
RAG_Based_AI_Asst/
├── src/                    # Source code
│   ├── app.py             # Core RAG logic
│   ├── server.py          # Web server
│   ├── vectordb.py        # Vector DB wrapper
│   ├── static/            # Frontend assets
│   └── templates/         # HTML templates
├── data/                  # Initial documents
├── uploads/               # User uploads
├── chroma_db/            # Vector DB storage
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
├── pyproject.toml         # Project config
└── [config files]        # Various configs
```

### Best Practices:
- Clear separation of concerns
- Logical grouping of related files
- Consistent naming conventions
- Minimal nesting depth

---

## 3. Environment and Dependencies 🔧

**Purpose**: Specification of software requirements and configuration needed to run the code.

### Files:
- **.env.example**: Template for environment variables
- **requirements.txt**: Python package dependencies with versions
- **pyproject.toml**: Project metadata and build configuration
- **docs/ENVIRONMENT_SETUP.md**: Comprehensive setup guide

### Configuration:
- API keys for LLM providers (OpenAI, Groq, Google)
- Optional: Vector DB collection name, embedding model
- Virtual environment setup instructions
- Dependency version management

### Best Practices:
- Never commit `.env` files (in `.gitignore`)
- Pin dependency versions for reproducibility
- Document all required environment variables
- Provide clear setup instructions

---

## 4. License and Legal ⚖️

**Purpose**: Permissions and terms governing the use of the code and associated assets.

### Files:
- **LICENSE**: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
- **README.md**: License section with attribution requirements

### License Details:
- **Type**: CC BY-NC-SA 4.0
- **Permissions**: 
  - Share and adapt for non-commercial purposes
  - Must give appropriate credit
  - Must share adaptations under same license
- **Restrictions**: No commercial use without permission

### Best Practices:
- Clear license statement in README
- License file in root directory
- Attribution requirements documented
- Legal compliance maintained

---

## 5. Code Quality 🎯

**Purpose**: Technical standards and practices applied to the codebase.

### Configuration Files:
- **.flake8**: Linting configuration (line length, exclusions)
- **pyproject.toml**: Black formatter, mypy type checking, pytest settings
- **docs/CODE_QUALITY.md**: Standards documentation

### Standards:
- **Type Hints**: All functions include parameter and return type hints
- **Docstrings**: Google-style docstrings for all classes and functions
- **Formatting**: Black formatter with 100 character line length
- **Linting**: Flake8 for code quality checks
- **Type Checking**: Optional mypy for static type analysis

### Tools:
- `black`: Code formatter
- `flake8`: Linter
- `mypy`: Type checker (optional)
- `pytest`: Testing framework (optional)

### Best Practices:
- Consistent code style
- Comprehensive documentation
- Error handling
- Type safety where applicable
- Regular code reviews

---

## Framework Compliance Checklist

- [x] **Documentation**: Comprehensive guides and architecture docs
- [x] **Repository Structure**: Well-organized directory structure
- [x] **Environment and Dependencies**: Clear setup and configuration
- [x] **License and Legal**: Proper license and attribution
- [x] **Code Quality**: Standards, linting, and best practices

---

## Maintenance

This framework should be maintained and updated as the project evolves:

1. **Documentation**: Update when features change
2. **Structure**: Refactor if organization becomes unclear
3. **Dependencies**: Keep requirements.txt updated
4. **License**: Ensure compliance with license terms
5. **Code Quality**: Enforce standards in code reviews

---

For more details on each category, refer to the respective documentation files listed above.

