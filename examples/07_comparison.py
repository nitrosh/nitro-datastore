"""Example 7: Comparison Operations - Comparing and diffing data.

This example covers:
- Checking equality with equals()
- Finding differences with diff()
- Comparing versions
- Tracking changes
- Merging and conflict detection
"""

from nitro_datastore import NitroDataStore

print("=" * 70)
print("COMPARISON OPERATIONS EXAMPLES")
print("=" * 70)

# ============================================================================
# Basic Equality
# ============================================================================
print("\n1. Basic Equality Checks")
print("-" * 70)

data1 = NitroDataStore({'name': 'Alice', 'age': 30, 'city': 'NYC'})
data2 = NitroDataStore({'name': 'Alice', 'age': 30, 'city': 'NYC'})
data3 = NitroDataStore({'name': 'Bob', 'age': 25, 'city': 'LA'})

print(f"data1 equals data2: {data1.equals(data2)}")
print(f"data1 equals data3: {data1.equals(data3)}")

# Also works with plain dictionaries
dict_version = {'name': 'Alice', 'age': 30, 'city': 'NYC'}
print(f"data1 equals dict: {data1.equals(dict_version)}")

# Nested structures
nested1 = NitroDataStore({
    'user': {'name': 'Alice', 'settings': {'theme': 'dark'}}
})
nested2 = NitroDataStore({
    'user': {'name': 'Alice', 'settings': {'theme': 'dark'}}
})
nested3 = NitroDataStore({
    'user': {'name': 'Alice', 'settings': {'theme': 'light'}}
})

print(f"\nNested equal: {nested1.equals(nested2)}")
print(f"Nested different: {nested1.equals(nested3)}")

# ============================================================================
# Finding Differences
# ============================================================================
print("\n2. Finding Differences with diff()")
print("-" * 70)

old_config = NitroDataStore({
    'app': {
        'name': 'MyApp',
        'version': '1.0.0',
        'debug': False
    },
    'database': {
        'host': 'localhost',
        'port': 5432
    },
    'removed_feature': True
})

new_config = NitroDataStore({
    'app': {
        'name': 'MyApp',  # Same
        'version': '2.0.0',  # Changed
        'debug': True  # Changed
    },
    'database': {
        'host': 'prod-db.example.com',  # Changed
        'port': 5432  # Same
    },
    'new_feature': True  # Added
    # removed_feature is missing (removed)
})

diff = old_config.diff(new_config)

print("Changes from old to new:")
print(f"\nAdded ({len(diff['added'])}):")
for key, value in diff['added'].items():
    print(f"  + {key} = {value}")

print(f"\nRemoved ({len(diff['removed'])}):")
for key, value in diff['removed'].items():
    print(f"  - {key} = {value}")

print(f"\nChanged ({len(diff['changed'])}):")
for key, change in diff['changed'].items():
    print(f"  ~ {key}: {change['old']} -> {change['new']}")

# ============================================================================
# Version Tracking
# ============================================================================
print("\n3. Version Tracking Example")
print("-" * 70)

# Version 1.0
v1 = NitroDataStore({
    'version': '1.0.0',
    'features': ['auth', 'api'],
    'config': {
        'timeout': 5000,
        'retries': 3
    }
})

# Version 1.1 (minor update)
v1_1 = NitroDataStore({
    'version': '1.1.0',
    'features': ['auth', 'api', 'cache'],  # Added cache
    'config': {
        'timeout': 5000,
        'retries': 3,
        'cache_ttl': 3600  # New config
    }
})

# Version 2.0 (major update)
v2_0 = NitroDataStore({
    'version': '2.0.0',
    'features': ['auth', 'api', 'cache', 'webhooks'],  # Added webhooks
    'config': {
        'timeout': 10000,  # Increased
        'retries': 5,  # Increased
        'cache_ttl': 7200  # Increased
    }
})

print("Comparing v1.0 to v1.1 (minor update):")
diff_1_1 = v1.diff(v1_1)
print(f"  Added: {len(diff_1_1['added'])} items")
print(f"  Changed: {len(diff_1_1['changed'])} items")
print(f"  Removed: {len(diff_1_1['removed'])} items")

print("\nComparing v1.1 to v2.0 (major update):")
diff_2_0 = v1_1.diff(v2_0)
print(f"  Added: {len(diff_2_0['added'])} items")
print(f"  Changed: {len(diff_2_0['changed'])} items")
for key, change in diff_2_0['changed'].items():
    print(f"    ~ {key}: {change['old']} -> {change['new']}")

# ============================================================================
# Tracking User Changes
# ============================================================================
print("\n4. Tracking User Profile Changes")
print("-" * 70)

original_profile = NitroDataStore({
    'user': {
        'name': 'Alice Johnson',
        'email': 'alice@example.com',
        'preferences': {
            'theme': 'light',
            'language': 'en',
            'notifications': True
        },
        'subscription': 'free'
    }
})

updated_profile = NitroDataStore({
    'user': {
        'name': 'Alice Johnson',  # Unchanged
        'email': 'alice.johnson@example.com',  # Changed
        'preferences': {
            'theme': 'dark',  # Changed
            'language': 'en',  # Unchanged
            'notifications': False  # Changed
        },
        'subscription': 'premium',  # Changed
        'joined': '2024-01-15'  # Added
    }
})

diff = original_profile.diff(updated_profile)

print("User profile changes:")
if diff['added']:
    print("\n  New information:")
    for key, value in diff['added'].items():
        print(f"    + {key}: {value}")

if diff['changed']:
    print("\n  Updated information:")
    for key, change in diff['changed'].items():
        field = key.split('.')[-1]
        print(f"    ~ {field}: '{change['old']}' -> '{change['new']}'")

# ============================================================================
# Configuration Drift Detection
# ============================================================================
print("\n5. Configuration Drift Detection")
print("-" * 70)

# Expected production config
expected_config = NitroDataStore({
    'database': {
        'host': 'prod-db.example.com',
        'port': 5432,
        'ssl': True,
        'pool_size': 20
    },
    'cache': {
        'enabled': True,
        'redis_url': 'redis://prod-redis:6379'
    },
    'security': {
        'cors_enabled': True,
        'rate_limit': 1000
    }
})

# Actual production config (with drift)
actual_config = NitroDataStore({
    'database': {
        'host': 'prod-db.example.com',
        'port': 5432,
        'ssl': False,  # DRIFT: Should be True!
        'pool_size': 10  # DRIFT: Should be 20
    },
    'cache': {
        'enabled': True,
        'redis_url': 'redis://dev-redis:6379'  # DRIFT: Wrong Redis!
    },
    'security': {
        'cors_enabled': True,
        'rate_limit': 1000
    },
    'debug': True  # DRIFT: Debug mode in production!
})

drift = expected_config.diff(actual_config)

print("Configuration drift detected!")

if drift['added']:
    print("\n  WARNING - Unexpected settings:")
    for key, value in drift['added'].items():
        print(f"    ! {key}: {value}")

if drift['changed']:
    print("\n  WARNING - Mismatched settings:")
    for key, change in drift['changed'].items():
        print(f"    ! {key}")
        print(f"      Expected: {change['old']}")
        print(f"      Actual:   {change['new']}")

if drift['removed']:
    print("\n  WARNING - Missing settings:")
    for key, value in drift['removed'].items():
        print(f"    ! {key} is missing (expected: {value})")

# ============================================================================
# Merge Conflict Detection
# ============================================================================
print("\n6. Merge Conflict Detection")
print("-" * 70)

# Base document
base = NitroDataStore({
    'document': {
        'title': 'Project Plan',
        'status': 'draft',
        'owner': 'Alice'
    }
})

# Alice's edits
alice_edits = NitroDataStore({
    'document': {
        'title': 'Project Plan - Q1',  # Changed
        'status': 'review',  # Changed
        'owner': 'Alice',
        'reviewers': ['Bob']  # Added
    }
})

# Bob's edits (made independently)
bob_edits = NitroDataStore({
    'document': {
        'title': 'Updated Project Plan',  # Changed (conflict!)
        'status': 'draft',
        'owner': 'Alice',
        'priority': 'high'  # Added
    }
})

# Find conflicts
alice_changes = base.diff(alice_edits)
bob_changes = base.diff(bob_edits)

# Check for conflicting changes
conflicting_fields = set()
for key in alice_changes['changed'].keys():
    if key in bob_changes['changed']:
        if alice_changes['changed'][key]['new'] != bob_changes['changed'][key]['new']:
            conflicting_fields.add(key)

print("Merge conflict analysis:")
print(f"\n  Alice's changes: {len(alice_changes['changed']) + len(alice_changes['added'])}")
print(f"  Bob's changes: {len(bob_changes['changed']) + len(bob_changes['added'])}")
print(f"\n  CONFLICTS: {len(conflicting_fields)}")

if conflicting_fields:
    for field in conflicting_fields:
        print(f"\n  Field: {field}")
        print(f"    Base:  {base.get(field)}")
        print(f"    Alice: {alice_changes['changed'][field]['new']}")
        print(f"    Bob:   {bob_changes['changed'][field]['new']}")

# ============================================================================
# Change History
# ============================================================================
print("\n7. Tracking Change History")
print("-" * 70)

# Simulate a series of changes
versions = []

v0 = NitroDataStore({'count': 0, 'status': 'initial'})
versions.append(('v0', v0))

v1 = NitroDataStore({'count': 5, 'status': 'initial'})
versions.append(('v1', v1))

v2 = NitroDataStore({'count': 10, 'status': 'updated'})
versions.append(('v2', v2))

v3 = NitroDataStore({'count': 10, 'status': 'updated', 'verified': True})
versions.append(('v3', v3))

print("Change history:")
for i in range(len(versions) - 1):
    prev_name, prev_data = versions[i]
    curr_name, curr_data = versions[i + 1]

    diff = prev_data.diff(curr_data)
    total_changes = len(diff['added']) + len(diff['changed']) + len(diff['removed'])

    print(f"\n  {prev_name} -> {curr_name} ({total_changes} changes)")

    for key, value in diff['added'].items():
        print(f"    + {key} = {value}")
    for key, change in diff['changed'].items():
        print(f"    ~ {key}: {change['old']} -> {change['new']}")
    for key, value in diff['removed'].items():
        print(f"    - {key}")

print("\n" + "=" * 70)
print("Comparison operations examples completed!")
print("=" * 70)
