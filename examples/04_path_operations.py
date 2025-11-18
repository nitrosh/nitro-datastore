"""Example 4: Path Operations - Finding and working with paths.

This example covers:
- Listing all paths with list_paths()
- Finding paths with patterns using find_paths()
- Getting multiple values with get_many()
- Finding keys with find_all_keys()
- Finding values with predicates using find_values()
- Flattening nested structures
"""

from nitro_datastore import NitroDataStore

print("=" * 70)
print("PATH OPERATIONS EXAMPLES")
print("=" * 70)

# Create complex nested data
data = NitroDataStore(
    {
        "site": {
            "name": "Tech Blog",
            "url": "https://blog.example.com",
            "social": {
                "twitter": {"url": "https://twitter.com/techblog", "followers": 1500},
                "github": {"url": "https://github.com/techblog", "stars": 320},
                "linkedin": {
                    "url": "https://linkedin.com/company/techblog",
                    "followers": 800,
                },
            },
        },
        "posts": [
            {
                "title": "First Post",
                "author": {"name": "Alice", "email": "alice@example.com"},
                "metadata": {"views": 150, "likes": 12},
                "images": ["hero.jpg", "diagram.png"],
            },
            {
                "title": "Second Post",
                "author": {"name": "Bob", "email": "bob@example.com"},
                "metadata": {"views": 200, "likes": 18},
                "images": ["cover.jpg"],
            },
        ],
        "config": {
            "theme": {
                "colors": {"primary": "#007bff", "secondary": "#6c757d"},
                "fonts": {"heading": "Inter", "body": "Georgia"},
            },
            "cache": {"enabled": True, "ttl": 3600},
        },
    }
)

# ============================================================================
# Listing All Paths
# ============================================================================
print("\n1. Listing All Paths")
print("-" * 70)

all_paths = data.list_paths()
print(f"Total paths in data structure: {len(all_paths)}")
print("\nFirst 15 paths:")
for i, path in enumerate(all_paths[:15], 1):
    print(f"  {i:2d}. {path}")

# ============================================================================
# Listing Paths with Prefix
# ============================================================================
print("\n2. Listing Paths with Prefix")
print("-" * 70)

# Get all site-related paths
site_paths = data.list_paths(prefix="site")
print(f"Paths under 'site' ({len(site_paths)}):")
for path in site_paths:
    print(f"  - {path}")

# Get all social media paths
social_paths = data.list_paths(prefix="site.social")
print(f"\nPaths under 'site.social' ({len(social_paths)}):")
for path in social_paths:
    print(f"  - {path}")

# Get all config paths
config_paths = data.list_paths(prefix="config")
print(f"\nPaths under 'config' ({len(config_paths)}):")
for path in config_paths:
    print(f"  - {path}")

# ============================================================================
# Finding Paths with Patterns
# ============================================================================
print("\n3. Finding Paths with Patterns")
print("-" * 70)

# Find all 'url' fields anywhere in the structure
url_paths = data.find_paths("**.url")
print(f"All 'url' paths ({len(url_paths)}):")
for path in url_paths:
    value = data.get(path)
    print(f"  {path} = {value}")

# Find all 'name' fields
name_paths = data.find_paths("**.name")
print(f"\nAll 'name' paths ({len(name_paths)}):")
for path in name_paths:
    value = data.get(path)
    print(f"  {path} = {value}")

# Find paths matching specific patterns
# Pattern: posts.*.title (title of each post)
post_titles = data.find_paths("posts.*.title")
print(f"\nPost titles ({len(post_titles)}):")
for path in post_titles:
    value = data.get(path)
    print(f"  {path} = {value}")

# Pattern: posts.*.author.name
author_names = data.find_paths("posts.*.author.name")
print(f"\nAuthor names ({len(author_names)}):")
for path in author_names:
    value = data.get(path)
    print(f"  {path} = {value}")

# Pattern: posts.*.metadata.* (all metadata fields)
metadata_paths = data.find_paths("posts.*.metadata.*")
print(f"\nMetadata paths ({len(metadata_paths)}):")
for path in metadata_paths:
    value = data.get(path)
    print(f"  {path} = {value}")

# ============================================================================
# Getting Multiple Values
# ============================================================================
print("\n4. Getting Multiple Values with get_many()")
print("-" * 70)

# Get specific values in one call
paths_to_get = [
    "site.name",
    "site.url",
    "config.theme.colors.primary",
    "config.cache.enabled",
    "nonexistent.path",
]

values = data.get_many(paths_to_get)
print("Getting multiple paths:")
for path, value in values.items():
    print(f"  {path} = {value}")

# ============================================================================
# Finding All Occurrences of a Key
# ============================================================================
print("\n5. Finding All Occurrences of a Key")
print("-" * 70)

# Find all 'url' keys
all_urls = data.find_all_keys("url")
print(f"All 'url' keys ({len(all_urls)}):")
for path, value in all_urls.items():
    print(f"  {path} = {value}")

# Find all 'name' keys
all_names = data.find_all_keys("name")
print(f"\nAll 'name' keys ({len(all_names)}):")
for path, value in all_names.items():
    print(f"  {path} = {value}")

# Find all 'followers' keys
all_followers = data.find_all_keys("followers")
print(f"\nAll 'followers' keys ({len(all_followers)}):")
for path, value in all_followers.items():
    print(f"  {path} = {value}")

# Find all 'email' keys
all_emails = data.find_all_keys("email")
print(f"\nAll 'email' keys ({len(all_emails)}):")
for path, value in all_emails.items():
    print(f"  {path} = {value}")

# ============================================================================
# Finding Values with Predicates
# ============================================================================
print("\n6. Finding Values with Predicates")
print("-" * 70)

# Find all string values that are URLs (contain 'http')
urls = data.find_values(lambda v: isinstance(v, str) and "http" in v)
print(f"All URL values ({len(urls)}):")
for path, value in urls.items():
    print(f"  {path} = {value}")

# Find all numeric values greater than 100
big_numbers = data.find_values(lambda v: isinstance(v, (int, float)) and v > 100)
print(f"\nNumeric values > 100 ({len(big_numbers)}):")
for path, value in big_numbers.items():
    print(f"  {path} = {value}")

# Find all email addresses
emails = data.find_values(lambda v: isinstance(v, str) and "@" in v)
print(f"\nEmail addresses ({len(emails)}):")
for path, value in emails.items():
    print(f"  {path} = {value}")

# Find all image files (ending with .jpg or .png)
images = data.find_values(lambda v: isinstance(v, str) and v.endswith((".jpg", ".png")))
print(f"\nImage files ({len(images)}):")
for path, value in images.items():
    print(f"  {path} = {value}")

# Find all boolean values
booleans = data.find_values(lambda v: isinstance(v, bool))
print(f"\nBoolean values ({len(booleans)}):")
for path, value in booleans.items():
    print(f"  {path} = {value}")

# Find all lists
lists = data.find_values(lambda v: isinstance(v, list))
print(f"\nList values ({len(lists)}):")
for path, value in lists.items():
    print(f"  {path} = {value[:2]}..." if len(value) > 2 else f"  {path} = {value}")

# ============================================================================
# Flattening Nested Structures
# ============================================================================
print("\n7. Flattening Nested Structures")
print("-" * 70)

# Flatten entire structure
flat = data.flatten()
print(f"Flattened structure ({len(flat)} keys):")
# Show first 10 items
for i, (key, value) in enumerate(list(flat.items())[:10], 1):
    value_str = (
        str(value)
        if not isinstance(value, (dict, list))
        else f"<{type(value).__name__}>"
    )
    print(f"  {i:2d}. {key} = {value_str}")

# Flatten with custom separator
flat_underscore = data.flatten(separator="_")
print(f"\nFlattened with '_' separator (first 5):")
for i, (key, value) in enumerate(list(flat_underscore.items())[:5], 1):
    value_str = (
        str(value)
        if not isinstance(value, (dict, list))
        else f"<{type(value).__name__}>"
    )
    print(f"  {i}. {key} = {value_str}")

# ============================================================================
# Practical Use Cases
# ============================================================================
print("\n8. Practical Use Cases")
print("-" * 70)

# Use case 1: Find all configuration values
print("Configuration values:")
config_values = {k: v for k, v in flat.items() if k.startswith("config.")}
for key, value in list(config_values.items())[:5]:
    print(f"  {key} = {value}")

# Use case 2: Extract all social media data
print("\nSocial media data:")
social_data = {k: v for k, v in flat.items() if "social" in k}
for key, value in social_data.items():
    print(f"  {key} = {value}")

# Use case 3: Get all post metadata
print("\nPost metadata:")
metadata = {k: v for k, v in flat.items() if "metadata" in k}
for key, value in metadata.items():
    print(f"  {key} = {value}")

# Use case 4: Find all colors
print("\nColor values:")
colors = {k: v for k, v in flat.items() if "color" in k}
for key, value in colors.items():
    print(f"  {key} = {value}")

# ============================================================================
# Working with Dynamic Paths
# ============================================================================
print("\n9. Working with Dynamic Paths")
print("-" * 70)

# Build paths dynamically
post_index = 0
author_name_path = f"posts.{post_index}.author.name"
author_name = data.get(author_name_path)
print(f"Author of post {post_index}: {author_name}")

# Get all authors using pattern
all_post_authors = data.find_paths("posts.*.author.name")
print(f"\nAll post authors:")
for path in all_post_authors:
    author = data.get(path)
    post_num = path.split(".")[1]
    print(f"  Post {post_num}: {author}")

# Get view counts for all posts
view_paths = data.find_paths("posts.*.metadata.views")
print(f"\nView counts:")
total_views = 0
for path in view_paths:
    views = data.get(path, 0)
    post_num = path.split(".")[1]
    total_views += views
    print(f"  Post {post_num}: {views} views")
print(f"Total views across all posts: {total_views}")

print("\n" + "=" * 70)
print("Path operations examples completed!")
print("=" * 70)
