# Agents Knowledge


## Code Conventions

- Write modular, clean and fully typed modern python code.
- Use new style Python types (e.g., `list`, `dict`, `tuple`, `set`, `int | None` instead of `List`, `Dict`, `Tuple`, `Set`, `Optional`).
- Use lower case for logs: logger.info("starting xyz").
- Prefer logger instead of print statements.
- Log lines and exceptions should always start with a lowercase char.
- Log lines should not end with a period.
- Try not to use `Any` for typing.
- All code should be typed using modern python.
- Use early returns to reduce indentation.
- Extract complex logic into functions.
- Flatten loops with list comprehensions.
- Leverage data structures instead of deeply nested conditions.
- Write self-explanatory code – Prefer clear variable and function names over comments.
- Explain "why," not "what" – Comments should clarify intent, not restate code.
- Avoid redundant comments – Don't comment obvious things.
- Use comments for complex logic – Explain non-trivial decisions or workarounds.
- Write docstrings for functions/classes – Document purpose, inputs, and outputs.
- Keep comments updated – Outdated comments are worse than none.
- Use inline comments sparingly – Only when necessary for clarity.
- Let Python handle exceptions by default - prefer crashing over complex error handling
- Only add try-except blocks when:
  - Explicitly required to keep the application running.
  - Requested by the user/product requirements.
  - Handling a specific, recoverable error case.
- Instead of defensive programming with try-except blocks:
  - Use assertions to validate critical assumptions.
  - Let functions fail fast with invalid inputs - Don't catch broad exceptions (except Exception).
  - Trust Python's built-in error handling.
- Let stack traces expose issues during development.

## Linting

```
make lint
```

```
make mypy
```

## Formatting

```
make format
```

## Dependency Management

We use uv to manage Python dependencies.

Run

```
uv add <your-package-name>
```

This installs the package and adds it to `pyproject.toml`.

## Running The Application

```
make run
```
