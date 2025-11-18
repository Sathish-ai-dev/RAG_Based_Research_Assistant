# Contributing to RAG-Based AI Assistant

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. **Fork the repository** and clone your fork
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

## Development Workflow

1. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards (see Code Quality section)

3. **Test your changes**:
   ```bash
   # Run the CLI version
   python src/app.py
   
   # Or run the web server
   uvicorn src.server:app --reload
   ```

4. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add: description of your change"
   ```

5. **Push and create a Pull Request**

## Code Quality Standards

- **Type Hints**: Use type hints for function parameters and return values
- **Docstrings**: Add docstrings to all classes and functions
- **Formatting**: Follow PEP 8 style guidelines
- **Testing**: Test your changes before submitting

## Pull Request Guidelines

- Provide a clear description of what your PR does
- Reference any related issues
- Ensure all tests pass
- Update documentation if needed

## Questions?

Feel free to open an issue for any questions or clarifications.

