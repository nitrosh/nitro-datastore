"""Example 5: Bulk Operations - Updating, cleaning, and transforming data.

This example covers:
- Conditional updates with update_where()
- Removing null values with remove_nulls()
- Removing empty containers with remove_empty()
- Filtering lists with filter_list()
- Transforming all values with transform_all()
- Transforming all keys with transform_keys()
"""

from nitro_datastore import NitroDataStore

print("=" * 70)
print("BULK OPERATIONS EXAMPLES")
print("=" * 70)

# ============================================================================
# Conditional Updates with update_where()
# ============================================================================
print("\n1. Conditional Updates with update_where()")
print("-" * 70)

# Sample data with URLs to update
data = NitroDataStore({
    'links': {
        'blog': 'http://blog.example.com',
        'api': 'https://api.example.com',
        'docs': 'http://docs.example.com'
    },
    'social': {
        'twitter': 'http://twitter.com/user',
        'github': 'https://github.com/user'
    },
    'count': 42
})

print("Original URLs:")
print(f"  blog: {data.links.blog}")
print(f"  docs: {data.links.docs}")
print(f"  twitter: {data.social.twitter}")

# Upgrade all HTTP URLs to HTTPS
count = data.update_where(
    condition=lambda path, value: isinstance(value, str) and 'http://' in value,
    transform=lambda value: value.replace('http://', 'https://')
)

print(f"\nUpdated {count} URLs from HTTP to HTTPS")
print("Updated URLs:")
print(f"  blog: {data.links.blog}")
print(f"  docs: {data.links.docs}")
print(f"  twitter: {data.social.twitter}")

# More examples
data2 = NitroDataStore({
    'prices': {'item1': 100, 'item2': 200, 'item3': 50},
    'discounts': {'sale1': 0.1, 'sale2': 0.2},
    'name': 'Store'
})

# Apply 10% discount to all prices over 75
count = data2.update_where(
    condition=lambda p, v: 'prices' in p and isinstance(v, (int, float)) and v > 75,
    transform=lambda v: v * 0.9
)

print(f"\nApplied discount to {count} items")
print(f"Updated prices: {data2.prices.to_dict()}")

# ============================================================================
# Removing Null Values
# ============================================================================
print("\n2. Removing Null Values with remove_nulls()")
print("-" * 70)

# Data with None values
messy_data = NitroDataStore({
    'user': {
        'name': 'Alice',
        'email': None,
        'phone': '555-1234',
        'address': None
    },
    'settings': {
        'theme': 'dark',
        'language': None,
        'notifications': True
    },
    'metadata': None,
    'items': [1, None, 2, None, 3, None]
})

print("Before removing nulls:")
print(f"  user.email: {messy_data.get('user.email')}")
print(f"  settings.language: {messy_data.get('settings.language')}")
print(f"  metadata: {messy_data.get('metadata')}")
print(f"  items: {messy_data.get('items')}")

count = messy_data.remove_nulls()
print(f"\nRemoved {count} null values")

print("After removing nulls:")
print(f"  user keys: {list(messy_data.user.to_dict().keys())}")
print(f"  settings keys: {list(messy_data.settings.to_dict().keys())}")
print(f"  metadata exists: {messy_data.has('metadata')}")
print(f"  items: {messy_data.get('items')}")

# ============================================================================
# Removing Empty Containers
# ============================================================================
print("\n3. Removing Empty Containers with remove_empty()")
print("-" * 70)

# Data with empty dicts and lists
cluttered_data = NitroDataStore({
    'config': {},
    'tags': [],
    'valid': {
        'value': 1,
        'nested': {
            'empty_dict': {},
            'empty_list': [],
            'actual_value': 'keep this'
        }
    },
    'items': [1, 2, 3],
    'more_empty': {}
})

print("Before removing empty containers:")
print(f"  Top-level keys: {list(cluttered_data.keys())}")
print(f"  valid.nested keys: {list(cluttered_data.valid.nested.to_dict().keys())}")

count = cluttered_data.remove_empty()
print(f"\nRemoved {count} empty containers")

print("After removing empty containers:")
print(f"  Top-level keys: {list(cluttered_data.keys())}")
print(f"  valid.nested keys: {list(cluttered_data.valid.nested.to_dict().keys())}")

# ============================================================================
# Filtering Lists
# ============================================================================
print("\n4. Filtering Lists with filter_list()")
print("-" * 70)

blog_data = NitroDataStore({
    'posts': [
        {'title': 'Post 1', 'published': True, 'views': 100},
        {'title': 'Post 2', 'published': False, 'views': 50},
        {'title': 'Post 3', 'published': True, 'views': 200},
        {'title': 'Post 4', 'published': True, 'views': 150},
        {'title': 'Post 5', 'published': False, 'views': 25}
    ]
})

print(f"Total posts: {len(blog_data.posts)}")

# Filter published posts
published = blog_data.filter_list('posts', lambda p: p.get('published'))
print(f"Published posts: {len(published)}")
for post in published:
    print(f"  - {post['title']}")

# Filter posts with more than 100 views
popular = blog_data.filter_list('posts', lambda p: p.get('views', 0) > 100)
print(f"\nPopular posts (>100 views): {len(popular)}")
for post in popular:
    print(f"  - {post['title']} ({post['views']} views)")

# Filter drafts
drafts = blog_data.filter_list('posts', lambda p: not p.get('published'))
print(f"\nDraft posts: {len(drafts)}")
for post in drafts:
    print(f"  - {post['title']}")

# ============================================================================
# Data Cleaning Pipeline
# ============================================================================
print("\n5. Data Cleaning Pipeline")
print("-" * 70)

# Messy data from external source
raw_data = NitroDataStore({
    'users': [
        {
            'name': 'alice',
            'email': 'alice@example.com',
            'profile': {'bio': None, 'avatar': 'http://example.com/alice.jpg'},
            'tags': []
        },
        {
            'name': 'bob',
            'email': None,
            'profile': {'bio': 'Developer', 'avatar': 'http://example.com/bob.jpg'},
            'tags': ['admin']
        },
        {
            'name': 'carol',
            'email': 'carol@example.com',
            'profile': {},
            'tags': None
        }
    ],
    'settings': {
        'theme': None,
        'cache': {},
        'features': {'a': 1, 'b': None}
    }
})

print("Before cleaning:")
print(f"  Total users: {len(raw_data.users)}")
print(f"  Settings keys: {list(raw_data.settings.to_dict().keys())}")

# Step 1: Remove nulls
null_count = raw_data.remove_nulls()
print(f"\nStep 1: Removed {null_count} null values")

# Step 2: Remove empty containers
empty_count = raw_data.remove_empty()
print(f"Step 2: Removed {empty_count} empty containers")

# Step 3: Upgrade HTTP to HTTPS
http_count = raw_data.update_where(
    condition=lambda p, v: isinstance(v, str) and 'http://' in v,
    transform=lambda v: v.replace('http://', 'https://')
)
print(f"Step 3: Upgraded {http_count} URLs to HTTPS")

# Step 4: Capitalize names
name_count = raw_data.update_where(
    condition=lambda p, v: p.endswith('.name') and isinstance(v, str),
    transform=lambda v: v.capitalize()
)
print(f"Step 4: Capitalized {name_count} names")

print("\nAfter cleaning:")
print(f"  Users: {len(raw_data.users)}")
for user in raw_data.users:
    print(f"    - {user.get('name')}: {user.get('email', 'no email')}")
print(f"  Settings keys: {list(raw_data.settings.to_dict().keys())}")

# ============================================================================
# Complex Transformations
# ============================================================================
print("\n6. Complex Transformations")
print("-" * 70)

ecommerce_data = NitroDataStore({
    'products': [
        {'name': 'Widget', 'price': 19.99, 'currency': 'USD', 'stock': 100},
        {'name': 'Gadget', 'price': 29.99, 'currency': 'USD', 'stock': 50},
        {'name': 'Tool', 'price': 39.99, 'currency': 'USD', 'stock': 75}
    ]
})

print("Original prices:")
for product in ecommerce_data.products:
    print(f"  {product['name']}: ${product['price']}")

# Apply tax and round
tax_rate = 0.10
count = ecommerce_data.update_where(
    condition=lambda p, v: p.endswith('.price') and isinstance(v, (int, float)),
    transform=lambda v: round(v * (1 + tax_rate), 2)
)

print(f"\nApplied {tax_rate*100}% tax to {count} prices:")
for product in ecommerce_data.products:
    print(f"  {product['name']}: ${product['price']}")

# Add sale discount to low stock items
count = ecommerce_data.update_where(
    condition=lambda p, v: (
        p.endswith('.price') and
        isinstance(v, (int, float)) and
        # Get stock for this product
        any(prod.get('stock', 999) < 60 and prod.get('price') == v
            for prod in ecommerce_data.products)
    ),
    transform=lambda v: round(v * 0.9, 2)
)

print(f"\nApplied 10% clearance discount to {count} low-stock items:")
for product in ecommerce_data.products:
    stock_status = "LOW STOCK" if product['stock'] < 60 else "in stock"
    print(f"  {product['name']}: ${product['price']} ({stock_status})")

# ============================================================================
# Batch Operations Example
# ============================================================================
print("\n7. Batch Operations Example")
print("-" * 70)

# Configuration update scenario
old_config = NitroDataStore({
    'api': {
        'endpoint': 'http://old-api.example.com',
        'timeout': 5000,
        'retries': 3
    },
    'database': {
        'host': 'old-db.example.com',
        'port': 5432
    },
    'cache': {
        'enabled': False,
        'ttl': None
    }
})

print("Migrating configuration...")

# 1. Update all old-*.example.com to new-*.example.com
count1 = old_config.update_where(
    condition=lambda p, v: isinstance(v, str) and 'old-' in v,
    transform=lambda v: v.replace('old-', 'new-')
)
print(f"  Updated {count1} hostnames")

# 2. Increase all timeout values by 50%
count2 = old_config.update_where(
    condition=lambda p, v: 'timeout' in p or 'ttl' in p,
    transform=lambda v: int(v * 1.5) if isinstance(v, (int, float)) and v else v
)
print(f"  Updated {count2} timeout/TTL values")

# 3. Enable cache and remove nulls
old_config.set('cache.enabled', True)
null_count = old_config.remove_nulls()
print(f"  Enabled cache, removed {null_count} nulls")

print("\nMigrated configuration:")
print(f"  API endpoint: {old_config.api.endpoint}")
print(f"  API timeout: {old_config.api.timeout}")
print(f"  DB host: {old_config.database.host}")
print(f"  Cache: enabled={old_config.cache.enabled}")

print("\n" + "=" * 70)
print("Bulk operations examples completed!")
print("=" * 70)
