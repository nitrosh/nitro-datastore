# Package Structure

```
nitro-datastore/
├── nitro_datastore/              # Main package directory
│   ├── __init__.py              # Package initialization, exports NitroDataStore & QueryBuilder
│   ├── datastore.py             # Main NitroDataStore class
│   └── query_builder.py         # QueryBuilder class for chainable queries
│
├── tests/                        # Test suite
│   └── test_datastore.py        # Comprehensive test cases
│
├── examples/                     # Usage examples
│   └── basic_usage.py           # Basic usage demonstration
│
├── pyproject.toml               # Modern Python package metadata
├── setup.py                     # Backwards compatibility for older pip
├── MANIFEST.in                  # Package data inclusion rules
├── README.md                    # Package documentation for PyPI
├── LICENSE                      # MIT License
├── PUBLISHING.md                # Guide for publishing to PyPI
├── .gitignore                   # Git ignore rules
└── datastore-readme.md          # Original documentation (can be removed)
```

## Key Files

### pyproject.toml
- Package metadata and dependencies
- Build system configuration
- PyPI classifiers and keywords

### nitro_datastore/__init__.py
- Exports main classes: `NitroDataStore` and `QueryBuilder`
- Package version: `1.0.0`

### setup.py
- Minimal backwards-compatible setup
- Defers to pyproject.toml for configuration

## Installation

### As User
```bash
pip install nitro-datastore
```

### As Developer
```bash
git clone <repo-url>
cd nitro-datastore
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

## Building Distribution

```bash
# Install build tools
pip install build twine

# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# This creates:
# - dist/nitro_datastore-1.0.0.tar.gz
# - dist/nitro_datastore-1.0.0-py3-none-any.whl
```

## Testing

```bash
# Run tests
python -m pytest tests/

# Test basic import
python -c "from nitro_datastore import NitroDataStore; print('Success!')"

# Run example
python examples/basic_usage.py
```

## Publishing to PyPI

See `PUBLISHING.md` for detailed instructions.

Quick version:
```bash
# Test on TestPyPI first
python -m twine upload --repository testpypi dist/*

# Then publish to PyPI
python -m twine upload dist/*
```
