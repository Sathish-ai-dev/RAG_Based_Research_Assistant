# Code Quality Standards

This document outlines the code quality standards and practices for this project.

## Type Hints

All functions should include type hints for parameters and return values:

```python
from typing import List, Dict, Optional

def process_documents(documents: List[Dict[str, Any]]) -> int:
    """Process documents and return count."""
    return len(documents)
```

## Docstrings

Follow Google-style docstrings:

```python
def search(self, query: str, n_results: int = 5) -> Dict[str, Any]:
    """
    Search for similar documents in the vector database.

    Args:
        query: Search query string
        n_results: Number of results to return (default: 5)

    Returns:
        Dictionary containing search results with keys: 'documents', 
        'metadatas', 'distances', 'ids'
    """
```

## Code Formatting

- **Black**: Use Black formatter with 100 character line length
- **PEP 8**: Follow PEP 8 style guidelines
- **Line Length**: Maximum 100 characters (configurable exceptions)

## Linting

We use **flake8** for linting. Run before committing:

```bash
flake8 src/
```

## Type Checking

Optional type checking with **mypy**:

```bash
mypy src/
```

## Code Review Checklist

- [ ] Type hints added to all functions
- [ ] Docstrings added to all classes and functions
- [ ] Code formatted with Black
- [ ] No linting errors (flake8)
- [ ] Error handling implemented
- [ ] Tests pass (if applicable)

## Best Practices

1. **Error Handling**: Always handle exceptions gracefully
2. **Logging**: Use print statements for user-facing messages, logging for debugging
3. **Constants**: Define constants at module level
4. **Imports**: Group imports (stdlib, third-party, local)
5. **Naming**: Use descriptive names following PEP 8 conventions

