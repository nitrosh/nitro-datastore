# Publishing Guide for nitro-datastore

This guide explains how to build and publish the package to PyPI.

## Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Create accounts:
   - PyPI: https://pypi.org/account/register/
   - TestPyPI (for testing): https://test.pypi.org/account/register/

## Building the Package

1. Clean previous builds:
```bash
rm -rf dist/ build/ *.egg-info
```

2. Build the package:
```bash
python -m build
```

This creates:
- `dist/nitro_datastore-1.0.0.tar.gz` (source distribution)
- `dist/nitro_datastore-1.0.0-py3-none-any.whl` (wheel distribution)

## Testing with TestPyPI (Recommended)

1. Upload to TestPyPI:
```bash
python -m twine upload --repository testpypi dist/*
```

2. Test installation:
```bash
pip install --index-url https://test.pypi.org/simple/ nitro-datastore
```

3. Verify it works:
```bash
python -c "from nitro_datastore import NitroDataStore; print('Success!')"
```

## Publishing to PyPI

1. Upload to PyPI:
```bash
python -m twine upload dist/*
```

2. Verify on PyPI:
   - Visit: https://pypi.org/project/nitro-datastore/

3. Test installation:
```bash
pip install nitro-datastore
```

## Version Bumping

Before publishing a new version:

1. Update version in `pyproject.toml`:
```toml
version = "1.0.1"
```

2. Update version in `nitro_datastore/__init__.py`:
```python
__version__ = "1.0.1"
```

3. Create a git tag:
```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

## Automated Publishing with GitHub Actions (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: python -m twine upload dist/*
```

## Troubleshooting

### "File already exists" error
- You're trying to upload a version that already exists
- Bump the version number in both files mentioned above

### Import errors after installation
- Make sure `__init__.py` properly exports classes
- Check that all dependencies are listed in `pyproject.toml`

### Package not found on PyPI
- Wait a few minutes after upload (propagation delay)
- Check spelling: `nitro-datastore` vs `nitro_datastore`

## Post-Publishing Checklist

- [ ] Test installation: `pip install nitro-datastore`
- [ ] Verify imports work
- [ ] Check PyPI page looks correct
- [ ] Update GitHub repository with release notes
- [ ] Announce on relevant channels
