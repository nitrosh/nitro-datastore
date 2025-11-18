"""Example 3: Querying Collections - Using the query builder.

This example covers:
- Basic filtering with where()
- Sorting collections
- Pagination with limit() and offset()
- Getting first result
- Counting results
- Extracting fields with pluck()
- Grouping with group_by()
- Complex query chains
"""

from nitro_datastore import NitroDataStore

print("=" * 70)
print("QUERYING COLLECTIONS EXAMPLES")
print("=" * 70)

# Create sample data for a blog
data = NitroDataStore({
    'posts': [
        {
            'id': 1,
            'title': 'Getting Started with Python',
            'category': 'python',
            'author': 'Alice',
            'views': 1500,
            'likes': 120,
            'published': True,
            'date': '2024-01-15',
            'tags': ['python', 'beginners', 'tutorial']
        },
        {
            'id': 2,
            'title': 'Advanced JavaScript Patterns',
            'category': 'javascript',
            'author': 'Bob',
            'views': 2300,
            'likes': 200,
            'published': True,
            'date': '2024-01-20',
            'tags': ['javascript', 'advanced', 'patterns']
        },
        {
            'id': 3,
            'title': 'Python Data Structures Deep Dive',
            'category': 'python',
            'author': 'Alice',
            'views': 1800,
            'likes': 150,
            'published': True,
            'date': '2024-01-25',
            'tags': ['python', 'data-structures', 'advanced']
        },
        {
            'id': 4,
            'title': 'Web Development with React',
            'category': 'javascript',
            'author': 'Carol',
            'views': 3200,
            'likes': 280,
            'published': True,
            'date': '2024-02-01',
            'tags': ['react', 'javascript', 'web']
        },
        {
            'id': 5,
            'title': 'Draft: Machine Learning Basics',
            'category': 'python',
            'author': 'Alice',
            'views': 50,
            'likes': 5,
            'published': False,
            'date': '2024-02-05',
            'tags': ['python', 'ml', 'draft']
        },
        {
            'id': 6,
            'title': 'TypeScript Best Practices',
            'category': 'javascript',
            'author': 'Bob',
            'views': 2800,
            'likes': 240,
            'published': True,
            'date': '2024-02-10',
            'tags': ['typescript', 'javascript', 'best-practices']
        }
    ]
})

print(f"\nSample data: {len(data.posts)} blog posts")

# ============================================================================
# Basic Filtering with where()
# ============================================================================
print("\n1. Basic Filtering with where()")
print("-" * 70)

# Get all published posts
published = data.query('posts').where(lambda p: p.get('published')).execute()
print(f"Published posts: {len(published)}")

# Get posts by category
python_posts = data.query('posts').where(lambda p: p.get('category') == 'python').execute()
print(f"Python posts: {len(python_posts)}")

# Get posts by author
alice_posts = data.query('posts').where(lambda p: p.get('author') == 'Alice').execute()
print(f"Posts by Alice: {len(alice_posts)}")

# Get posts with more than 2000 views
popular = data.query('posts').where(lambda p: p.get('views', 0) > 2000).execute()
print(f"Popular posts (>2000 views): {len(popular)}")

# ============================================================================
# Multiple Filters (AND Logic)
# ============================================================================
print("\n2. Multiple Filters (AND Logic)")
print("-" * 70)

# Published Python posts
published_python = (data.query('posts')
    .where(lambda p: p.get('published'))
    .where(lambda p: p.get('category') == 'python')
    .execute())

print(f"Published Python posts: {len(published_python)}")
for post in published_python:
    print(f"  - {post['title']}")

# Popular published posts
popular_published = (data.query('posts')
    .where(lambda p: p.get('published'))
    .where(lambda p: p.get('views') > 2000)
    .execute())

print(f"\nPopular published posts: {len(popular_published)}")
for post in popular_published:
    print(f"  - {post['title']} ({post['views']} views)")

# ============================================================================
# Sorting
# ============================================================================
print("\n3. Sorting")
print("-" * 70)

# Sort by views (ascending)
by_views_asc = data.query('posts').sort(key=lambda p: p.get('views', 0)).execute()
print("Posts sorted by views (ascending):")
for post in by_views_asc[:3]:
    print(f"  {post['views']:4d} views - {post['title']}")

# Sort by views (descending)
by_views_desc = data.query('posts').sort(key=lambda p: p.get('views', 0), reverse=True).execute()
print("\nTop 3 posts by views:")
for post in by_views_desc[:3]:
    print(f"  {post['views']:4d} views - {post['title']}")

# Sort by date (most recent first)
by_date = data.query('posts').sort(key=lambda p: p.get('date', ''), reverse=True).execute()
print("\nMost recent posts:")
for post in by_date[:3]:
    print(f"  {post['date']} - {post['title']}")

# Sort by likes
by_likes = data.query('posts').sort(key=lambda p: p.get('likes', 0), reverse=True).execute()
print("\nMost liked posts:")
for post in by_likes[:3]:
    print(f"  {post['likes']:3d} likes - {post['title']}")

# ============================================================================
# Pagination
# ============================================================================
print("\n4. Pagination with limit() and offset()")
print("-" * 70)

# First page (3 posts)
page1 = data.query('posts').limit(3).execute()
print(f"Page 1 (first 3 posts): {len(page1)} posts")
for post in page1:
    print(f"  - {post['title']}")

# Second page
page2 = data.query('posts').offset(3).limit(3).execute()
print(f"\nPage 2 (next 3 posts): {len(page2)} posts")
for post in page2:
    print(f"  - {post['title']}")

# Page 3
page3 = data.query('posts').offset(6).limit(3).execute()
print(f"\nPage 3 (remaining posts): {len(page3)} posts")
for post in page3:
    print(f"  - {post['title']}")

# ============================================================================
# Getting First Result
# ============================================================================
print("\n5. Getting First Result")
print("-" * 70)

# Most viewed post
most_viewed = data.query('posts').sort(key=lambda p: p.get('views'), reverse=True).first()
if most_viewed:
    print(f"Most viewed post: {most_viewed['title']} ({most_viewed['views']} views)")

# First Python post
first_python = data.query('posts').where(lambda p: p.get('category') == 'python').first()
if first_python:
    print(f"First Python post: {first_python['title']}")

# First post by Carol
carol_post = data.query('posts').where(lambda p: p.get('author') == 'Carol').first()
if carol_post:
    print(f"First post by Carol: {carol_post['title']}")

# No results (returns None)
golang_post = data.query('posts').where(lambda p: p.get('category') == 'golang').first()
print(f"First Golang post: {golang_post}")

# ============================================================================
# Counting Results
# ============================================================================
print("\n6. Counting Results")
print("-" * 70)

total_posts = data.query('posts').count()
print(f"Total posts: {total_posts}")

published_count = data.query('posts').where(lambda p: p.get('published')).count()
print(f"Published posts: {published_count}")

python_count = data.query('posts').where(lambda p: p.get('category') == 'python').count()
print(f"Python posts: {python_count}")

popular_count = data.query('posts').where(lambda p: p.get('views', 0) > 2000).count()
print(f"Popular posts: {popular_count}")

# ============================================================================
# Extracting Fields with pluck()
# ============================================================================
print("\n7. Extracting Fields with pluck()")
print("-" * 70)

# Get all titles
titles = data.query('posts').pluck('title')
print(f"All titles ({len(titles)}):")
for title in titles:
    print(f"  - {title}")

# Get titles of published posts
published_titles = (data.query('posts')
    .where(lambda p: p.get('published'))
    .pluck('title'))
print(f"\nPublished titles ({len(published_titles)}):")
for title in published_titles:
    print(f"  - {title}")

# Get authors (with duplicates)
authors = data.query('posts').pluck('author')
print(f"\nAll authors: {authors}")
print(f"Unique authors: {set(authors)}")

# ============================================================================
# Grouping with group_by()
# ============================================================================
print("\n8. Grouping with group_by()")
print("-" * 70)

# Group by category
by_category = data.query('posts').group_by('category')
print("Posts grouped by category:")
for category, posts in by_category.items():
    print(f"  {category}: {len(posts)} posts")

# Group by author
by_author = data.query('posts').group_by('author')
print("\nPosts grouped by author:")
for author, posts in by_author.items():
    print(f"  {author}: {len(posts)} posts")

# Group published posts by category
published_by_category = (data.query('posts')
    .where(lambda p: p.get('published'))
    .group_by('category'))
print("\nPublished posts by category:")
for category, posts in published_by_category.items():
    print(f"  {category}: {len(posts)} posts")

# ============================================================================
# Complex Query Chains
# ============================================================================
print("\n9. Complex Query Chains")
print("-" * 70)

# Top 3 published Python posts by views
top_python = (data.query('posts')
    .where(lambda p: p.get('published'))
    .where(lambda p: p.get('category') == 'python')
    .sort(key=lambda p: p.get('views'), reverse=True)
    .limit(3)
    .execute())

print("Top 3 published Python posts by views:")
for post in top_python:
    print(f"  {post['views']:4d} views - {post['title']}")

# Most liked posts by each author (using group_by + sorting)
print("\nMost liked post by each author:")
by_author_groups = data.query('posts').group_by('author')
for author, posts in by_author_groups.items():
    sorted_posts = sorted(posts, key=lambda p: p.get('likes', 0), reverse=True)
    top_post = sorted_posts[0] if sorted_posts else None
    if top_post:
        print(f"  {author}: {top_post['title']} ({top_post['likes']} likes)")

# Recent popular posts (published, >1500 views, sorted by date)
recent_popular = (data.query('posts')
    .where(lambda p: p.get('published'))
    .where(lambda p: p.get('views', 0) > 1500)
    .sort(key=lambda p: p.get('date'), reverse=True)
    .execute())

print(f"\nRecent popular posts (published, >1500 views):")
for post in recent_popular:
    print(f"  {post['date']} - {post['title']} ({post['views']} views)")

# ============================================================================
# Advanced Filtering
# ============================================================================
print("\n10. Advanced Filtering Examples")
print("-" * 70)

# Posts with specific tag
tutorial_posts = data.query('posts').where(
    lambda p: 'tutorial' in p.get('tags', [])
).execute()
print(f"Posts with 'tutorial' tag: {len(tutorial_posts)}")

# Posts with multiple tags
advanced_posts = data.query('posts').where(
    lambda p: 'advanced' in p.get('tags', [])
).execute()
print(f"Posts with 'advanced' tag: {len(advanced_posts)}")

# Posts with high engagement (views > 2000 OR likes > 200)
high_engagement = data.query('posts').where(
    lambda p: p.get('views', 0) > 2000 or p.get('likes', 0) > 200
).execute()
print(f"High engagement posts: {len(high_engagement)}")

# Posts from specific date range
jan_posts = data.query('posts').where(
    lambda p: p.get('date', '').startswith('2024-01')
).execute()
print(f"Posts from January 2024: {len(jan_posts)}")

print("\n" + "=" * 70)
print("Querying examples completed!")
print("=" * 70)
