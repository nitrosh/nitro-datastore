"""Example 2: File Operations - Loading and saving data.

This example covers:
- Loading from JSON files
- Loading from directories (auto-merge)
- Saving to JSON files
- Working with file-based data
"""

import json
import tempfile
from pathlib import Path
from nitro_datastore import NitroDataStore

print("=" * 70)
print("FILE OPERATIONS EXAMPLES")
print("=" * 70)

# Create a temporary directory for our examples
temp_dir = Path(tempfile.mkdtemp())
print(f"\nUsing temporary directory: {temp_dir}")

# ============================================================================
# Saving to JSON Files
# ============================================================================
print("\n1. Saving to JSON Files")
print("-" * 70)

# Create a datastore
config = NitroDataStore(
    {
        "database": {"host": "localhost", "port": 5432, "name": "myapp"},
        "cache": {"enabled": True, "ttl": 3600},
    }
)

# Save to file (creates parent directories automatically)
config_file = temp_dir / "config.json"
config.save(config_file)
print(f"Saved to: {config_file}")

# Verify the file was created
print(f"File exists: {config_file.exists()}")
print(f"File size: {config_file.stat().st_size} bytes")

# Save with custom indentation
config.save(temp_dir / "config_compact.json", indent=None)
config.save(temp_dir / "config_pretty.json", indent=4)
print("Saved with different indentation levels")

# ============================================================================
# Loading from JSON Files
# ============================================================================
print("\n2. Loading from JSON Files")
print("-" * 70)

# Load the file we just saved
loaded = NitroDataStore.from_file(config_file)
print(f"Loaded from file")
print(f"Database host: {loaded.database.host}")
print(f"Cache enabled: {loaded.cache.enabled}")

# Verify data integrity
print(f"Data matches original: {loaded.equals(config)}")

# ============================================================================
# Loading from Directory (Auto-merge)
# ============================================================================
print("\n3. Loading from Directory (Auto-merge)")
print("-" * 70)

# Create a data directory
data_dir = temp_dir / "data"
data_dir.mkdir()

# Create multiple JSON files
# File 1: Base configuration
base_config = {
    "app": {"name": "MyApp", "version": "1.0.0", "debug": False},
    "features": {"auth": True, "api": True},
}
with open(data_dir / "01_base.json", "w") as f:
    json.dump(base_config, f, indent=2)

# File 2: Override some values, add new ones
dev_overrides = {
    "app": {"debug": True, "environment": "development"},  # Override  # New
    "database": {"host": "localhost"},  # New section
}
with open(data_dir / "02_dev.json", "w") as f:
    json.dump(dev_overrides, f, indent=2)

# File 3: More additions
extra_config = {"features": {"experimental": True}}  # Add to features
with open(data_dir / "03_extra.json", "w") as f:
    json.dump(extra_config, f, indent=2)

print(f"Created 3 JSON files in {data_dir}")

# Load and merge all files
merged = NitroDataStore.from_directory(data_dir)

print("\nMerged data:")
print(f"  app.name: {merged.get('app.name')} (from 01_base.json)")
print(f"  app.debug: {merged.get('app.debug')} (overridden by 02_dev.json)")
print(f"  app.environment: {merged.get('app.environment')} (from 02_dev.json)")
print(f"  database.host: {merged.get('database.host')} (from 02_dev.json)")
print(f"  features.auth: {merged.get('features.auth')} (from 01_base.json)")
print(
    f"  features.experimental: {merged.get('features.experimental')} (from 03_extra.json)"
)

# ============================================================================
# Loading with Custom Pattern
# ============================================================================
print("\n4. Loading with Custom Pattern")
print("-" * 70)

# Create some files with different patterns
(data_dir / "settings.config.json").write_text('{"setting": "value"}')
(data_dir / "other.json").write_text('{"other": "data"}')

# Load only .config.json files
config_only = NitroDataStore.from_directory(data_dir, pattern="*.config.json")
print(f"Loaded *.config.json files")
print(f"Has 'setting': {config_only.has('setting')}")
print(f"Has 'other': {config_only.has('other')}")

# ============================================================================
# Working with Real-world File Structure
# ============================================================================
print("\n5. Real-world Example: Blog Data")
print("-" * 70)

# Create a blog data structure
blog_dir = temp_dir / "blog"
blog_dir.mkdir()

# Site metadata
site_data = {
    "site": {
        "name": "My Tech Blog",
        "url": "https://blog.example.com",
        "author": "Jane Developer",
    }
}
with open(blog_dir / "site.json", "w") as f:
    json.dump(site_data, f, indent=2)

# Posts data
posts_data = {
    "posts": [
        {
            "id": 1,
            "title": "Getting Started with Python",
            "date": "2024-01-15",
            "published": True,
            "tags": ["python", "tutorial"],
        },
        {
            "id": 2,
            "title": "Advanced Data Structures",
            "date": "2024-01-20",
            "published": True,
            "tags": ["python", "advanced"],
        },
        {
            "id": 3,
            "title": "Draft Post",
            "date": "2024-01-25",
            "published": False,
            "tags": ["draft"],
        },
    ]
}
with open(blog_dir / "posts.json", "w") as f:
    json.dump(posts_data, f, indent=2)

# Theme configuration
theme_data = {
    "theme": {
        "colors": {"primary": "#007bff", "secondary": "#6c757d"},
        "fonts": {"heading": "Inter", "body": "Georgia"},
    }
}
with open(blog_dir / "theme.json", "w") as f:
    json.dump(theme_data, f, indent=2)

# Load all blog data
blog = NitroDataStore.from_directory(blog_dir)

print("Loaded blog data from multiple files:")
print(f"  Site name: {blog.site.name}")
print(f"  Total posts: {len(blog.posts)}")
print(f"  Primary color: {blog.theme.colors.primary}")

# Use the loaded data
published_count = len([p for p in blog.posts if p.get("published")])
print(f"  Published posts: {published_count}")

# Modify and save back
blog.set("site.updated", "2024-01-25")
blog.save(temp_dir / "blog_complete.json")
print(f"\nSaved complete blog data to blog_complete.json")

# ============================================================================
# Error Handling
# ============================================================================
print("\n6. Error Handling")
print("-" * 70)

# Try to load non-existent file
try:
    NitroDataStore.from_file("nonexistent.json")
    print("ERROR: Should have raised FileNotFoundError")
except FileNotFoundError as e:
    print(f"Caught expected error: FileNotFoundError")

# Try to load non-existent directory
try:
    NitroDataStore.from_directory("nonexistent_dir")
    print("ERROR: Should have raised FileNotFoundError")
except FileNotFoundError as e:
    print(f"Caught expected error: FileNotFoundError")

# Create invalid JSON file
invalid_file = temp_dir / "invalid.json"
invalid_file.write_text("{ invalid json }")

try:
    NitroDataStore.from_file(invalid_file)
    print("ERROR: Should have raised JSONDecodeError")
except json.JSONDecodeError:
    print(f"Caught expected error: JSONDecodeError")

# Note: from_directory silently skips invalid files
dir_with_invalid = temp_dir / "mixed"
dir_with_invalid.mkdir()
(dir_with_invalid / "valid.json").write_text('{"valid": true}')
(dir_with_invalid / "invalid.json").write_text("{ bad json }")

mixed_data = NitroDataStore.from_directory(dir_with_invalid)
print(f"from_directory with invalid files: loaded {len(mixed_data)} top-level keys")
print(f"  (Invalid files are silently skipped)")

# ============================================================================
# Cleanup
# ============================================================================
print("\n" + "=" * 70)
print("File operations examples completed!")
print(f"Temporary files created in: {temp_dir}")
print("=" * 70)
