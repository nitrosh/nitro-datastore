"""Example 8: Comprehensive Real-World Example - Blog Management System.

This example demonstrates a complete workflow using multiple features:
- Loading data from files
- Querying and filtering
- Path operations
- Bulk updates
- Transformations
- Comparison and tracking changes
- Saving results

Scenario: Managing a tech blog with posts, authors, and analytics.
"""

import json
import tempfile
from pathlib import Path
from nitro_datastore import NitroDataStore

print("=" * 70)
print("COMPREHENSIVE EXAMPLE: BLOG MANAGEMENT SYSTEM")
print("=" * 70)

# Create temporary directory for demo files
temp_dir = Path(tempfile.mkdtemp())
data_dir = temp_dir / "blog_data"
data_dir.mkdir()

print(f"\nDemo directory: {temp_dir}")

# ============================================================================
# Step 1: Set Up Initial Data
# ============================================================================
print("\n" + "=" * 70)
print("STEP 1: Setting Up Initial Blog Data")
print("=" * 70)

# Create blog posts data
posts_data = {
    "posts": [
        {
            "id": 1,
            "title": "getting started with python",
            "slug": "getting-started-python",
            "author-id": 1,
            "category": "python",
            "status": "published",
            "published-date": "2024-01-15",
            "content": "Learn Python basics...",
            "tags": ["python", "beginners"],
            "views": 1500,
            "likes": 120,
        },
        {
            "id": 2,
            "title": "advanced javascript patterns",
            "slug": "advanced-javascript",
            "author-id": 2,
            "category": "javascript",
            "status": "published",
            "published-date": "2024-01-20",
            "content": "Deep dive into JS...",
            "tags": ["javascript", "advanced"],
            "views": 2300,
            "likes": 200,
        },
        {
            "id": 3,
            "title": "draft machine learning post",
            "slug": "ml-basics",
            "author-id": 1,
            "category": "python",
            "status": "draft",
            "published-date": None,
            "content": "Coming soon...",
            "tags": ["python", "ml"],
            "views": 0,
            "likes": 0,
        },
    ]
}

# Create authors data
authors_data = {
    "authors": [
        {
            "id": 1,
            "name": "alice johnson",
            "email": "alice@example.com",
            "bio": "python expert",
            "avatar": "http://example.com/alice.jpg",
        },
        {
            "id": 2,
            "name": "bob smith",
            "email": "bob@example.com",
            "bio": "javascript guru",
            "avatar": "http://example.com/bob.jpg",
        },
    ]
}

# Create settings data
settings_data = {
    "site": {"name": "TechBlog", "url": "http://techblog.example.com", "theme": "dark"},
    "features": {"comments-enabled": True, "analytics-enabled": True},
}

# Save to files
with open(data_dir / "posts.json", "w") as f:
    json.dump(posts_data, f, indent=2)
with open(data_dir / "authors.json", "w") as f:
    json.dump(authors_data, f, indent=2)
with open(data_dir / "settings.json", "w") as f:
    json.dump(settings_data, f, indent=2)

print(f"Created 3 data files in {data_dir}")

# ============================================================================
# Step 2: Load and Merge Data
# ============================================================================
print("\n" + "=" * 70)
print("STEP 2: Loading Blog Data")
print("=" * 70)

# Load all data files and merge
blog = NitroDataStore.from_directory(data_dir)

print(f"Loaded blog data:")
print(f"  Posts: {len(blog.posts)}")
print(f"  Authors: {len(blog.authors)}")
print(f"  Site name: {blog.site.name}")

# Get statistics
stats = blog.stats()
print(f"\nData structure statistics:")
print(f"  Total keys: {stats['total_keys']}")
print(f"  Max depth: {stats['max_depth']}")
print(f"  Total values: {stats['total_values']}")

# ============================================================================
# Step 3: Data Cleaning and Normalization
# ============================================================================
print("\n" + "=" * 70)
print("STEP 3: Cleaning and Normalizing Data")
print("=" * 70)

# Remove null values
null_count = blog.remove_nulls()
print(f"Removed {null_count} null values")

# Normalize keys: kebab-case to snake_case
print("\nNormalizing keys (kebab-case -> snake_case)...")
blog = blog.transform_keys(lambda k: k.replace("-", "_"))
print(f"  Sample keys: {list(blog.posts[0].keys())[:5]}")

# Normalize data values
print("\nNormalizing data values...")

# Title case all titles
blog = blog.transform_all(
    lambda p, v: v.title() if p.endswith(".title") and isinstance(v, str) else v
)

# Capitalize author names
blog = blog.transform_all(
    lambda p, v: v.title() if p.endswith(".name") and isinstance(v, str) else v
)

# Upgrade HTTP to HTTPS
http_count = blog.update_where(
    condition=lambda p, v: isinstance(v, str) and "http://" in v,
    transform=lambda v: v.replace("http://", "https://"),
)
print(f"  Upgraded {http_count} URLs to HTTPS")

print(f"\nAfter normalization:")
print(f"  Post title: {blog.posts[0]['title']}")
print(f"  Author name: {blog.authors[0]['name']}")
print(f"  Site URL: {blog.site.url}")

# ============================================================================
# Step 4: Querying and Analysis
# ============================================================================
print("\n" + "=" * 70)
print("STEP 4: Querying and Analysis")
print("=" * 70)

# Get published posts
published = (
    blog.query("posts").where(lambda p: p.get("status") == "published").execute()
)
print(f"Published posts: {len(published)}")

# Get most popular posts
popular = (
    blog.query("posts")
    .where(lambda p: p.get("status") == "published")
    .sort(key=lambda p: p.get("views", 0), reverse=True)
    .execute()
)

print(f"\nMost popular posts:")
for i, post in enumerate(popular[:3], 1):
    print(f"  {i}. {post['title']} - {post['views']} views, {post['likes']} likes")

# Group posts by category
by_category = blog.query("posts").group_by("category")
print(f"\nPosts by category:")
for category, posts in by_category.items():
    print(f"  {category}: {len(posts)} posts")

# Group posts by author
by_author = blog.query("posts").group_by("author_id")
print(f"\nPosts by author:")
for author_id, posts in by_author.items():
    author = next((a for a in blog.authors if a.get("id") == author_id), None)
    if author:
        print(f"  {author['name']}: {len(posts)} posts")

# Find all tags
all_tag_paths = blog.find_paths("posts.*.tags")
all_tags = set()
for path in all_tag_paths:
    tags = blog.get(path, [])
    all_tags.update(tags)
print(f"\nAll tags used: {sorted(all_tags)}")

# ============================================================================
# Step 5: Analytics Calculation
# ============================================================================
print("\n" + "=" * 70)
print("STEP 5: Calculating Analytics")
print("=" * 70)

# Calculate total engagement
total_views = sum(p.get("views", 0) for p in blog.posts)
total_likes = sum(p.get("likes", 0) for p in blog.posts)
avg_views = total_views / len(blog.posts)
avg_likes = total_likes / len(blog.posts)

print(f"Overall analytics:")
print(f"  Total posts: {len(blog.posts)}")
print(f"  Published: {len(published)}")
print(f"  Total views: {total_views:,}")
print(f"  Total likes: {total_likes:,}")
print(f"  Avg views per post: {avg_views:.1f}")
print(f"  Avg likes per post: {avg_likes:.1f}")

# Calculate per-author analytics
print(f"\nPer-author analytics:")
for author in blog.authors:
    author_posts = [p for p in blog.posts if p.get("author_id") == author["id"]]
    author_views = sum(p.get("views", 0) for p in author_posts)
    author_likes = sum(p.get("likes", 0) for p in author_posts)

    print(f"  {author['name']}:")
    print(f"    Posts: {len(author_posts)}")
    print(f"    Total views: {author_views:,}")
    print(f"    Total likes: {author_likes:,}")

# ============================================================================
# Step 6: Making Updates
# ============================================================================
print("\n" + "=" * 70)
print("STEP 6: Making Updates")
print("=" * 70)

# Save current state for comparison
original_blog = NitroDataStore(blog.to_dict())

# Publish a draft post
draft = blog.query("posts").where(lambda p: p.get("status") == "draft").first()
if draft:
    draft_id = draft["id"]
    print(f"Publishing draft: {draft['title']}")

    # Find and update the draft
    for i, post in enumerate(blog.posts):
        if post.get("id") == draft_id:
            blog.posts[i]["status"] = "published"
            blog.posts[i]["published_date"] = "2024-02-15"
            break

# Update view counts (simulate traffic)
print("\nSimulating traffic...")
view_increase = blog.update_where(
    condition=lambda p, v: (
        p.endswith(".views")
        and isinstance(v, (int, float))
        and
        # Only published posts get views
        any(
            post.get("views") == v and post.get("status") == "published"
            for post in blog.posts
        )
    ),
    transform=lambda v: v + 100,
)
print(f"  Increased views for {view_increase} posts")

# Add a new author
new_author = {
    "id": 3,
    "name": "Carol Davis",
    "email": "carol@example.com",
    "bio": "DevOps Specialist",
    "avatar": "https://example.com/carol.jpg",
}
blog.authors.append(new_author)
print(f"\nAdded new author: {new_author['name']}")

# ============================================================================
# Step 7: Track Changes
# ============================================================================
print("\n" + "=" * 70)
print("STEP 7: Tracking Changes")
print("=" * 70)

# Compare with original
diff = original_blog.diff(blog)

print(f"Changes made:")
print(f"  Added: {len(diff['added'])} items")
print(f"  Changed: {len(diff['changed'])} items")
print(f"  Removed: {len(diff['removed'])} items")

if diff["added"]:
    print(f"\n  Added items:")
    for key in list(diff["added"].keys())[:5]:
        print(f"    + {key}")

if diff["changed"]:
    print(f"\n  Changed items:")
    for key in list(diff["changed"].keys())[:5]:
        change = diff["changed"][key]
        print(f"    ~ {key}: {change['old']} -> {change['new']}")

# ============================================================================
# Step 8: Save Results
# ============================================================================
print("\n" + "=" * 70)
print("STEP 8: Saving Updated Data")
print("=" * 70)

# Save complete updated data
output_file = temp_dir / "blog_updated.json"
blog.save(output_file, indent=2)
print(f"Saved updated blog data to: {output_file}")

# Save analytics summary
analytics = NitroDataStore(
    {
        "generated": "2024-02-15",
        "summary": {
            "total_posts": len(blog.posts),
            "published_posts": len(
                [p for p in blog.posts if p.get("status") == "published"]
            ),
            "total_views": total_views + 100 * view_increase,
            "total_likes": total_likes,
            "total_authors": len(blog.authors),
        },
        "top_posts": [
            {"title": p["title"], "views": p["views"], "likes": p["likes"]}
            for p in popular[:3]
        ],
    }
)

analytics_file = temp_dir / "analytics.json"
analytics.save(analytics_file, indent=2)
print(f"Saved analytics to: {analytics_file}")

# ============================================================================
# Final Summary
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY: Blog Management Workflow Complete")
print("=" * 70)

print(
    f"""
Workflow completed successfully!

Final state:
  - Total posts: {len(blog.posts)}
  - Published posts: {len([p for p in blog.posts if p.get('status') == 'published'])}
  - Authors: {len(blog.authors)}
  - Categories: {len(by_category)}
  - Total views: {sum(p.get('views', 0) for p in blog.posts):,}
  - Total likes: {sum(p.get('likes', 0) for p in blog.posts):,}

Files created:
  - {output_file}
  - {analytics_file}

This example demonstrated:
  ✓ Loading data from multiple files
  ✓ Data cleaning and normalization
  ✓ Querying and filtering
  ✓ Path operations
  ✓ Bulk updates and transformations
  ✓ Analytics calculation
  ✓ Change tracking
  ✓ Saving results
"""
)

print("=" * 70)
