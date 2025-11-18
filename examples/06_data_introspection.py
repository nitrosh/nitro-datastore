"""Example 6: Data Introspection and Transformations - Understanding and reshaping data.

This example covers:
- Getting statistics with stats()
- Describing structure with describe()
- Transforming all values with transform_all()
- Transforming all keys with transform_keys()
- Flattening nested structures
"""

from nitro_datastore import NitroDataStore
import json

print("=" * 70)
print("DATA INTROSPECTION AND TRANSFORMATIONS")
print("=" * 70)

# Create sample data
data = NitroDataStore(
    {
        "site": {
            "name": "Tech Blog",
            "tagline": "exploring technology",
            "metadata": {"created": "2024-01-01", "updated": "2024-02-15"},
        },
        "posts": [
            {
                "title": "First Post",
                "author": "alice",
                "content": "Lorem ipsum...",
                "tags": ["python", "tutorial"],
            },
            {
                "title": "Second Post",
                "author": "bob",
                "content": "More content...",
                "tags": ["javascript", "web"],
            },
        ],
        "config": {
            "theme-color": "#007bff",
            "font-family": "Inter",
            "cache-enabled": True,
        },
        "count": 42,
    }
)

# ============================================================================
# Statistics
# ============================================================================
print("\n1. Data Statistics")
print("-" * 70)

stats = data.stats()
print("Structure statistics:")
print(f"  Total keys: {stats['total_keys']}")
print(f"  Maximum depth: {stats['max_depth']}")
print(f"  Total dictionaries: {stats['total_dicts']}")
print(f"  Total lists: {stats['total_lists']}")
print(f"  Total leaf values: {stats['total_values']}")

# ============================================================================
# Structure Description
# ============================================================================
print("\n2. Structure Description")
print("-" * 70)

description = data.describe()
print("Data structure description:")
print(json.dumps(description, indent=2)[:500] + "...")

# Analyze specific sections
print("\nSite structure:")
if "site" in description and "structure" in description["site"]:
    site_struct = description["site"]["structure"]
    print(f"  Type: {description['site']['type']}")
    print(f"  Keys: {description['site']['keys']}")

print("\nPosts structure:")
if "posts" in description:
    posts_struct = description["posts"]
    print(f"  Type: {posts_struct['type']}")
    print(f"  Length: {posts_struct['length']}")
    print(f"  Item types: {posts_struct['item_types']}")

# ============================================================================
# Transform All Values
# ============================================================================
print("\n3. Transforming All Values")
print("-" * 70)

# Example 1: Uppercase all strings
print("Example 1: Uppercase all strings")
print(f"  Original site.name: {data.site.name}")
print(f"  Original site.tagline: {data.site.tagline}")

uppercase_data = data.transform_all(
    lambda path, value: value.upper() if isinstance(value, str) else value
)

print(f"  Transformed site.name: {uppercase_data.site.name}")
print(f"  Transformed site.tagline: {uppercase_data.site.tagline}")
print(f"  Original unchanged: {data.site.name}")

# Example 2: Add prefix to all strings in a specific section
print("\nExample 2: Add prefix to specific paths")
prefixed_data = data.transform_all(
    lambda path, value: (
        f"BLOG: {value}"
        if (path.startswith("site.") and isinstance(value, str))
        else value
    )
)
print(f"  site.name: {prefixed_data.site.name}")
print(f"  posts[0].title: {prefixed_data.posts[0]['title']}")

# Example 3: Round all numbers
numeric_data = NitroDataStore(
    {"metrics": {"average": 42.789, "total": 1234.567, "ratio": 0.333333}}
)

rounded_data = numeric_data.transform_all(
    lambda path, value: round(value, 2) if isinstance(value, float) else value
)

print("\nExample 3: Round all numbers to 2 decimal places")
print(f"  Original average: {numeric_data.metrics.average}")
print(f"  Rounded average: {rounded_data.metrics.average}")
print(f"  Original ratio: {numeric_data.metrics.ratio}")
print(f"  Rounded ratio: {rounded_data.metrics.ratio}")

# Example 4: Sanitize data
sensitive_data = NitroDataStore(
    {
        "users": [
            {"name": "Alice", "email": "alice@example.com", "password": "secret123"},
            {"name": "Bob", "email": "bob@example.com", "password": "password456"},
        ]
    }
)

sanitized = sensitive_data.transform_all(
    lambda path, value: "***REDACTED***" if path.endswith(".password") else value
)

print("\nExample 4: Sanitize sensitive data")
print(f"  Original user 0: {sensitive_data.users[0]}")
print(f"  Sanitized user 0: {sanitized.users[0]}")

# ============================================================================
# Transform All Keys
# ============================================================================
print("\n4. Transforming All Keys")
print("-" * 70)

# Example 1: Convert kebab-case to snake_case
print("Example 1: kebab-case to snake_case")
print(f"  Original keys: {list(data.config.to_dict().keys())}")

snake_case_data = data.transform_keys(lambda k: k.replace("-", "_"))
print(f"  Transformed keys: {list(snake_case_data.config.to_dict().keys())}")
print(
    f"  Access: snake_case_data.config.theme_color = {snake_case_data.config.theme_color}"
)


# Example 2: Convert to camelCase
def to_camel_case(s):
    """Convert string to camelCase."""
    parts = s.replace("-", "_").split("_")
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


camel_data = data.transform_keys(to_camel_case)
print("\nExample 2: Convert to camelCase")
camel_config = camel_data.config.to_dict()
print(f"  Transformed keys: {list(camel_config.keys())}")

# Example 3: Uppercase all keys
upper_keys_data = data.transform_keys(lambda k: k.upper())
print("\nExample 3: Uppercase all keys")
print(f"  Top-level keys: {list(upper_keys_data.keys())}")
print(f"  Site keys: {list(upper_keys_data.SITE.to_dict().keys())}")

# Example 4: Add namespace prefix
namespaced = data.transform_keys(lambda k: f"app_{k}")
print("\nExample 4: Add namespace prefix")
print(f"  Top-level keys: {list(namespaced.keys())}")

# ============================================================================
# Flattening for Analysis
# ============================================================================
print("\n5. Flattening for Analysis")
print("-" * 70)

# Flatten with default separator
flat = data.flatten()
print(f"Flattened structure ({len(flat)} keys):")
for i, (key, value) in enumerate(list(flat.items())[:10], 1):
    value_str = (
        str(value)
        if not isinstance(value, (list, dict))
        else f"<{type(value).__name__}>"
    )
    print(f"  {i:2d}. {key:40s} = {value_str}")

# Flatten with custom separator
flat_slash = data.flatten(separator="/")
print(f"\nFlattened with '/' separator (first 5):")
for i, (key, value) in enumerate(list(flat_slash.items())[:5], 1):
    value_str = (
        str(value)
        if not isinstance(value, (list, dict))
        else f"<{type(value).__name__}>"
    )
    print(f"  {i}. {key} = {value_str}")

# Use flattened data for analysis
print("\nAnalyzing flattened data:")
string_values = {k: v for k, v in flat.items() if isinstance(v, str)}
print(f"  String values: {len(string_values)}")
numeric_values = {k: v for k, v in flat.items() if isinstance(v, (int, float))}
print(f"  Numeric values: {len(numeric_values)}")
bool_values = {k: v for k, v in flat.items() if isinstance(v, bool)}
print(f"  Boolean values: {len(bool_values)}")

# ============================================================================
# Complex Transformations
# ============================================================================
print("\n6. Complex Transformations")
print("-" * 70)

# Scenario: Blog post processing
blog_posts = NitroDataStore(
    {
        "posts": [
            {
                "title": "getting started with python",
                "excerpt": "learn the basics...",
                "published-date": "2024-01-15",
                "author-name": "alice johnson",
            },
            {
                "title": "advanced javascript",
                "excerpt": "dive deep into...",
                "published-date": "2024-01-20",
                "author-name": "bob smith",
            },
        ]
    }
)

print("Original post:")
print(f"  Title: {blog_posts.posts[0]['title']}")
print(f"  Keys: {list(blog_posts.posts[0].keys())}")

# Step 1: Title case all titles
blog_posts = blog_posts.transform_all(
    lambda p, v: v.title() if p.endswith(".title") and isinstance(v, str) else v
)

# Step 2: Convert keys from kebab-case to snake_case
blog_posts = blog_posts.transform_keys(lambda k: k.replace("-", "_"))

print("\nTransformed post:")
print(f"  Title: {blog_posts.posts[0]['title']}")
print(f"  Keys: {list(blog_posts.posts[0].keys())}")
print(f"  Author: {blog_posts.posts[0]['author_name']}")

# ============================================================================
# Data Migration Example
# ============================================================================
print("\n7. Data Migration Example")
print("-" * 70)

# Old API response format
old_format = NitroDataStore(
    {
        "user-data": {
            "first-name": "john",
            "last-name": "doe",
            "email-address": "john@example.com",
            "phone-number": "555-1234",
        },
        "preferences": {"theme-mode": "dark", "language-code": "en"},
    }
)

print("Old format:")
print(f"  Keys: {list(old_format.keys())}")
print(f"  User data keys: {list(old_format['user-data'].to_dict().keys())}")

# Migrate to new format
# 1. Convert keys to snake_case
new_format = old_format.transform_keys(lambda k: k.replace("-", "_"))

# 2. Capitalize names
new_format = new_format.transform_all(
    lambda p, v: v.capitalize() if p.endswith("_name") and isinstance(v, str) else v
)

print("\nNew format:")
print(f"  Keys: {list(new_format.keys())}")
print(f"  User data keys: {list(new_format.user_data.to_dict().keys())}")
print(f"  First name: {new_format.user_data.first_name}")
print(f"  Last name: {new_format.user_data.last_name}")

# ============================================================================
# Chaining Transformations
# ============================================================================
print("\n8. Chaining Transformations")
print("-" * 70)

original = NitroDataStore(
    {
        "product-data": {
            "product-name": "awesome widget",
            "product-price": 19.99,
            "in-stock": True,
        }
    }
)

print("Original:")
print(f"  {original.to_dict()}")

# Chain multiple transformations
result = (
    original.transform_keys(lambda k: k.replace("-", "_"))  # snake_case keys
    .transform_all(
        lambda p, v: (  # Title case product names
            v.title() if p.endswith("_name") and isinstance(v, str) else v
        )
    )
    .transform_all(
        lambda p, v: (  # Round prices
            round(v, 2) if p.endswith("_price") and isinstance(v, (int, float)) else v
        )
    )
)

print("\nAfter chaining transformations:")
print(f"  {result.to_dict()}")

print("\n" + "=" * 70)
print("Data introspection and transformations examples completed!")
print("=" * 70)
