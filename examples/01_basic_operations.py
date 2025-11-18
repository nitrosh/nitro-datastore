"""Example 1: Basic Operations - Creating and accessing data.

This example covers:
- Creating a datastore
- Three access patterns (dot notation, dictionary, path-based)
- Setting values
- Getting values with defaults
- Checking existence
- Deleting values
- Basic iteration
"""

from nitro_datastore import NitroDataStore

print("=" * 70)
print("BASIC OPERATIONS EXAMPLES")
print("=" * 70)

# ============================================================================
# Creating a DataStore
# ============================================================================
print("\n1. Creating a DataStore")
print("-" * 70)

# Create from dictionary
data = NitroDataStore({
    'site': {
        'name': 'My Awesome Site',
        'url': 'https://example.com',
        'author': 'John Doe'
    },
    'settings': {
        'theme': 'dark',
        'language': 'en'
    }
})

print("Created datastore with site and settings data")

# ============================================================================
# Access Patterns
# ============================================================================
print("\n2. Three Access Patterns")
print("-" * 70)

# Pattern 1: Dot notation (most convenient)
print(f"Dot notation:        {data.site.name}")

# Pattern 2: Dictionary access
print(f"Dictionary access:   {data['site']['url']}")

# Pattern 3: Path-based access (best for dynamic paths)
print(f"Path-based access:   {data.get('site.author')}")

# ============================================================================
# Setting Values
# ============================================================================
print("\n3. Setting Values")
print("-" * 70)

# Simple set
data.set('site.title', 'Welcome!')
print(f"Set site.title: {data.get('site.title')}")

# Creating nested structures automatically
data.set('config.cache.ttl', 3600)
print(f"Created nested path config.cache.ttl: {data.get('config.cache.ttl')}")

# Using dot notation
data.site.tagline = 'Building awesome things'
print(f"Set via dot notation: {data.site.tagline}")

# Using dictionary access
data['settings']['notifications'] = True
print(f"Set via dict access: {data['settings']['notifications']}")

# ============================================================================
# Getting Values with Defaults
# ============================================================================
print("\n4. Getting Values with Defaults")
print("-" * 70)

# Existing key
name = data.get('site.name', 'Default Name')
print(f"Existing key: {name}")

# Missing key with default
email = data.get('site.email', 'no-email@example.com')
print(f"Missing key with default: {email}")

# Nested missing key
color = data.get('settings.theme.primary', '#000000')
print(f"Nested missing key: {color}")

# ============================================================================
# Checking Existence
# ============================================================================
print("\n5. Checking if Keys Exist")
print("-" * 70)

# Check top-level key
print(f"'site' exists: {data.has('site')}")
print(f"'blog' exists: {data.has('blog')}")

# Check nested key
print(f"'site.name' exists: {data.has('site.name')}")
print(f"'site.email' exists: {data.has('site.email')}")

# Using 'in' operator (top-level only)
print(f"'settings' in data: {'settings' in data}")
print(f"'missing' in data: {'missing' in data}")

# ============================================================================
# Deleting Values
# ============================================================================
print("\n6. Deleting Values")
print("-" * 70)

# Add a temporary value
data.set('temp.value', 'delete me')
print(f"Before delete - temp.value exists: {data.has('temp.value')}")

# Delete using path notation
deleted = data.delete('temp.value')
print(f"Delete result: {deleted}")
print(f"After delete - temp.value exists: {data.has('temp.value')}")

# Try deleting non-existent key
deleted = data.delete('nonexistent.key')
print(f"Delete non-existent key: {deleted}")

# Delete using dictionary access
data['settings']['test'] = 'temporary'
del data['settings']['test']
print(f"Deleted using 'del' operator")

# ============================================================================
# Iteration
# ============================================================================
print("\n7. Iteration (Top-level)")
print("-" * 70)

# Iterate over keys
print("Top-level keys:")
for key in data.keys():
    print(f"  - {key}")

# Iterate over items
print("\nTop-level items:")
for key, value in data.items():
    value_type = type(value).__name__
    print(f"  {key}: <{value_type}>")

# Get length (number of top-level keys)
print(f"\nNumber of top-level keys: {len(data)}")

# ============================================================================
# Merging Data
# ============================================================================
print("\n8. Merging Data")
print("-" * 70)

# Create another datastore
updates = NitroDataStore({
    'site': {
        'name': 'Updated Site Name',  # This will override
        'version': '2.0'              # This will be added
    },
    'new_section': {
        'value': 'new data'
    }
})

print(f"Before merge - site.name: {data.site.name}")
print(f"Before merge - site.version exists: {data.has('site.version')}")

# Deep merge
data.merge(updates)

print(f"After merge - site.name: {data.site.name}")
print(f"After merge - site.url (preserved): {data.site.url}")
print(f"After merge - site.version: {data.site.version}")
print(f"After merge - new_section exists: {data.has('new_section')}")

# ============================================================================
# Converting to Dictionary
# ============================================================================
print("\n9. Converting to Dictionary")
print("-" * 70)

plain_dict = data.to_dict()
print(f"Type: {type(plain_dict)}")
print(f"Keys: {list(plain_dict.keys())}")
print("Exported as plain dictionary (deep copy)")

# ============================================================================
# String Representation
# ============================================================================
print("\n10. String Representation")
print("-" * 70)

# __repr__ shows the class
print(f"repr(data): {repr(data)[:50]}...")

# __str__ shows JSON
print(f"str(data) shows formatted JSON (first 100 chars):")
print(str(data)[:100] + "...")

print("\n" + "=" * 70)
print("Basic operations examples completed!")
print("=" * 70)
