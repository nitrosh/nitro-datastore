# LLM Usage Guide - nitro-datastore

Version: 1.0.x Language: Python 3.8+ Dependencies: None (pure Python, uses only stdlib)

Complete API reference for using nitro-datastore in code generation tasks.

## Installation

```python
from nitro_datastore import NitroDataStore, QueryBuilder
```

## Core Concepts

### Three Access Patterns

```python
data = NitroDataStore({'site': {'name': 'My Site'}})

data.site.name              # Dot notation
data['site']['name']        # Dictionary-style
data.get('site.name')       # Path-based (dot separator)
```

### Path Notation Rules

- Paths use dot (`.`) as separator: `'site.name'`, `'posts.0.title'`
- List indices are accessed as numbers: `'items.0'`, `'items.1'`
- Empty paths, whitespace-only paths, or paths with empty segments raise `ValueError`
- Invalid paths: `''`, `'.'`, `'..'`, `'foo.'`, `'.foo'`, `'foo..bar'`
- Keys containing dots must use dictionary access: `data['key.with.dots']` not `data.get('key.with.dots')`

### Nested Dict Wrapping

When accessing nested dicts, returns are automatically wrapped in `NitroDataStore` instances:

```python
data = NitroDataStore({'site': {'name': 'Test'}})
site = data.site           # Returns NitroDataStore({'name': 'Test'})
name = site.name           # Returns 'Test'
plain = data.to_dict()     # Returns plain Python dict
```

---

## NitroDataStore Class

### Constructor

```python
NitroDataStore(data: Optional[Dict[str, Any]] = None)
```

**Parameters:**
- `data` (dict, optional): Initial data dictionary. Defaults to empty dict.

**Returns:** NitroDataStore instance

**Example:**
```python
data = NitroDataStore()                          # Empty
data = NitroDataStore({'key': 'value'})          # With data
```

---

### Class Methods (File Operations)

#### from_file()

```python
@classmethod
NitroDataStore.from_file(
    file_path: Union[str, Path],
    base_dir: Optional[Union[str, Path]] = None,
    max_size: Optional[int] = None
) -> NitroDataStore
```

**Parameters:**
- `file_path` (str | Path): Path to JSON file
- `base_dir` (str | Path, optional): Base directory to restrict file access (security)
- `max_size` (int, optional): Maximum file size in bytes (security)

**Returns:** NitroDataStore instance

**Raises:**
- `FileNotFoundError`: File doesn't exist
- `ValueError`: Path escapes base_dir or file exceeds max_size
- `json.JSONDecodeError`: Invalid JSON

**Examples:**
```python
data = NitroDataStore.from_file('config.json')
data = NitroDataStore.from_file('config.json', base_dir='/app/data')
data = NitroDataStore.from_file('config.json', max_size=10*1024*1024)
```

#### from_directory()

```python
@classmethod
NitroDataStore.from_directory(
    directory: Union[str, Path],
    pattern: str = "*.json",
    base_dir: Optional[Union[str, Path]] = None,
    max_size: Optional[int] = None
) -> NitroDataStore
```

**Parameters:**
- `directory` (str | Path): Path to directory containing JSON files
- `pattern` (str, optional): Glob pattern for files. Default: `"*.json"`
- `base_dir` (str | Path, optional): Base directory to restrict access (security)
- `max_size` (int, optional): Maximum file size in bytes per file (security)

**Returns:** NitroDataStore with merged data

**Behavior:** Files merged alphabetically. Later files override earlier ones (deep merge).

**Raises:**
- `FileNotFoundError`: Directory doesn't exist
- `ValueError`: Directory escapes base_dir or file exceeds max_size

**Examples:**
```python
data = NitroDataStore.from_directory('data/')
data = NitroDataStore.from_directory('configs/', pattern='*.config.json')
data = NitroDataStore.from_directory('data/', base_dir='/app', max_size=10*1024*1024)
```

---

### Path-Based Access Methods

#### get()

```python
get(key: str, default: Any = None) -> Any
```

**Parameters:**
- `key` (str): Dot-separated path (e.g., `'site.name'`)
- `default` (Any, optional): Default value if key not found. Default: `None`

**Returns:** Value at path, or default if not found

**Raises:** `ValueError` if key is invalid (empty, whitespace, empty segments)

**Examples:**
```python
data.get('site.name')                     # Returns value
data.get('site.title', 'Untitled')        # Returns 'Untitled' if missing
data.get('posts.0.title')                 # Access list index
```

#### set()

```python
set(key: str, value: Any) -> None
```

**Parameters:**
- `key` (str): Dot-separated path
- `value` (Any): Value to set

**Returns:** None

**Behavior:** Creates nested dicts as needed. Invalidates cache.

**Raises:** `ValueError` if key is invalid

**Examples:**
```python
data.set('site.name', 'My Site')
data.set('deeply.nested.key', 'value')
```

#### delete()

```python
delete(key: str) -> bool
```

**Parameters:**
- `key` (str): Dot-separated path

**Returns:** `True` if key existed and was deleted, `False` otherwise

**Raises:** `ValueError` if key is invalid

**Examples:**
```python
exists = data.delete('site.name')         # True if deleted
exists = data.delete('missing.key')       # False
```

#### has()

```python
has(key: str) -> bool
```

**Parameters:**
- `key` (str): Dot-separated path

**Returns:** `True` if key exists, `False` otherwise

**Raises:** `ValueError` if key is invalid

**Examples:**
```python
if data.has('site.name'):
    print(data.get('site.name'))
```

---

### Data Manipulation Methods

#### merge()

```python
merge(other: Union[NitroDataStore, Dict[str, Any]]) -> None
```

**Parameters:**
- `other` (NitroDataStore | dict): Data to merge in

**Returns:** None

**Behavior:** Deep merges other into self. Nested dicts are merged recursively. Invalidates cache.

**Examples:**
```python
data.merge({'site': {'url': 'example.com'}})
data.merge(other_datastore)
```

#### to_dict()

```python
to_dict() -> Dict[str, Any]
```

**Parameters:** None

**Returns:** Deep copy of internal data as plain dict

**Examples:**
```python
plain_dict = data.to_dict()
```

#### save()

```python
save(file_path: Union[str, Path], indent: int = 2) -> None
```

**Parameters:**
- `file_path` (str | Path): Path to save JSON file
- `indent` (int, optional): JSON indentation. Default: `2`

**Returns:** None

**Behavior:** Creates parent directories if needed

**Examples:**
```python
data.save('output.json')
data.save('data.json', indent=4)
```

---

### Iteration Methods

#### keys()

```python
keys() -> Iterator[str]
```

**Returns:** Iterator of top-level keys

**Examples:**
```python
for key in data.keys():
    print(key)
```

#### values()

```python
values() -> Iterator[Any]
```

**Returns:** Iterator of top-level values

**Examples:**
```python
for value in data.values():
    print(value)
```

#### items()

```python
items() -> Iterator[tuple]
```

**Returns:** Iterator of (key, value) tuples

**Examples:**
```python
for key, value in data.items():
    print(f"{key}: {value}")
```

---

### Path Introspection Methods

#### list_paths()

```python
list_paths(prefix: str = "", separator: str = ".") -> List[str]
```

**Parameters:**
- `prefix` (str, optional): Filter paths by prefix. Default: `""`
- `separator` (str, optional): Path separator. Default: `"."`

**Returns:** List of all paths as dot-notation strings

**Behavior:** Results are cached. Cache invalidated on mutations.

**Examples:**
```python
paths = data.list_paths()                 # ['site.name', 'site.url']
paths = data.list_paths(prefix='site')    # ['site.name', 'site.url']
```

#### find_paths()

```python
find_paths(pattern: str, separator: str = ".") -> List[str]
```

**Parameters:**
- `pattern` (str): Glob pattern with wildcards
  - `*` matches single path segment
  - `**` matches any number of segments
- `separator` (str, optional): Path separator. Default: `"."`

**Returns:** List of matching paths

**Examples:**
```python
data.find_paths('*.title')                # ['post.title', 'page.title']
data.find_paths('posts.*.author')         # ['posts.0.author', 'posts.1.author']
data.find_paths('**.email')               # All 'email' keys at any depth
```

#### get_many()

```python
get_many(paths: List[str]) -> Dict[str, Any]
```

**Parameters:**
- `paths` (list of str): List of dot-notation paths

**Returns:** Dict mapping paths to values (None if not found)

**Examples:**
```python
values = data.get_many(['site.name', 'site.url', 'missing'])
# {'site.name': 'Test', 'site.url': 'example.com', 'missing': None}
```

#### find_all_keys()

```python
find_all_keys(key_name: str) -> Dict[str, Any]
```

**Parameters:**
- `key_name` (str): Key name to search for

**Returns:** Dict mapping paths to values for all matching keys

**Examples:**
```python
urls = data.find_all_keys('url')
# {'site.url': 'a.com', 'social.url': 'b.com'}
```

#### find_values()

```python
find_values(predicate: Callable[[Any], bool]) -> Dict[str, Any]
```

**Parameters:**
- `predicate` (callable): Function that takes value and returns bool

**Returns:** Dict mapping paths to values for all matching values

**Examples:**
```python
images = data.find_values(lambda v: isinstance(v, str) and v.endswith('.jpg'))
# {'hero.image': 'pic.jpg', 'gallery.0': 'photo.jpg'}
```

---

### Bulk Operations

#### update_where()

```python
update_where(
    condition: Callable[[str, Any], bool],
    transform: Callable[[Any], Any]
) -> int
```

**Parameters:**
- `condition` (callable): Function(path, value) -> bool
- `transform` (callable): Function(value) -> new_value

**Returns:** Number of values updated

**Behavior:** Mutates data in place. Invalidates cache.

**Examples:**
```python
count = data.update_where(
    lambda p, v: isinstance(v, str) and 'http://' in v,
    lambda v: v.replace('http://', 'https://')
)
```

#### remove_nulls()

```python
remove_nulls() -> int
```

**Parameters:** None

**Returns:** Number of None values removed

**Behavior:** Removes all None values recursively. Invalidates cache.

**Examples:**
```python
count = data.remove_nulls()
```

#### remove_empty()

```python
remove_empty() -> int
```

**Parameters:** None

**Returns:** Number of empty containers removed

**Behavior:** Removes empty dicts `{}` and lists `[]` recursively. Invalidates cache.

**Examples:**
```python
count = data.remove_empty()
```

---

### Transformation Methods

#### flatten()

```python
flatten(separator: str = ".") -> Dict[str, Any]
```

**Parameters:**
- `separator` (str, optional): Key separator. Default: `"."`

**Returns:** Flattened dict with dot-notation keys

**Examples:**
```python
flat = data.flatten()
# {'site.name': 'My Site', 'site.settings.theme': 'dark'}
```

#### transform_all()

```python
transform_all(transform: Callable[[str, Any], Any]) -> NitroDataStore
```

**Parameters:**
- `transform` (callable): Function(path, value) -> new_value

**Returns:** New NitroDataStore with transformed values

**Behavior:** Immutable - returns new instance. Only leaf values are transformed.

**Examples:**
```python
upper = data.transform_all(
    lambda p, v: v.upper() if isinstance(v, str) else v
)
```

#### transform_keys()

```python
transform_keys(transform: Callable[[str], str]) -> NitroDataStore
```

**Parameters:**
- `transform` (callable): Function(key) -> new_key

**Returns:** New NitroDataStore with transformed keys

**Behavior:** Immutable - returns new instance. Transforms all dict keys recursively.

**Examples:**
```python
snake = data.transform_keys(lambda k: k.replace('-', '_'))
camel = data.transform_keys(lambda k: k.title().replace('_', ''))
```

---

### Comparison Methods

#### diff()

```python
diff(other: Union[NitroDataStore, Dict[str, Any]]) -> Dict[str, Any]
```

**Parameters:**
- `other` (NitroDataStore | dict): Data to compare with

**Returns:** Dict with keys `'added'`, `'removed'`, `'changed'`
- `added`: Paths in other but not in self
- `removed`: Paths in self but not in other
- `changed`: Paths with different values (dict with `'old'` and `'new'`)

**Examples:**
```python
diff = data1.diff(data2)
# {
#   'added': {'c': 4},
#   'removed': {},
#   'changed': {'b': {'old': 2, 'new': 3}}
# }
```

#### equals()

```python
equals(other: Union[NitroDataStore, Dict[str, Any]]) -> bool
```

**Parameters:**
- `other` (NitroDataStore | dict): Data to compare with

**Returns:** `True` if equal, `False` otherwise

**Examples:**
```python
is_equal = data1.equals(data2)
```

---

### Introspection Methods

#### describe()

```python
describe() -> Dict[str, Any]
```

**Parameters:** None

**Returns:** Dict describing the data structure with type info

**Examples:**
```python
info = data.describe()
# {
#   'posts': {'type': 'list', 'length': 2, 'item_types': ['dict']},
#   'count': {'type': 'int', 'value': 5}
# }
```

#### stats()

```python
stats() -> Dict[str, int]
```

**Parameters:** None

**Returns:** Dict with statistics:
- `total_keys`: Total number of keys
- `max_depth`: Maximum nesting depth
- `total_dicts`: Number of dict objects
- `total_lists`: Number of list objects
- `total_values`: Number of leaf values

**Examples:**
```python
stats = data.stats()
# {'total_keys': 3, 'max_depth': 3, 'total_dicts': 3, 'total_lists': 0, 'total_values': 1}
```

---

### Query Methods

#### query()

```python
query(path: str) -> QueryBuilder
```

**Parameters:**
- `path` (str): Path to a list to query

**Returns:** QueryBuilder instance

**Behavior:** If path doesn't exist or isn't a list, returns empty QueryBuilder

**Examples:**
```python
results = data.query('posts').where(lambda p: p.get('published')).execute()
```

#### filter_list()

```python
filter_list(path: str, predicate: Callable[[Any], bool]) -> List[Any]
```

**Parameters:**
- `path` (str): Path to a list
- `predicate` (callable): Function(item) -> bool

**Returns:** Filtered list

**Examples:**
```python
published = data.filter_list('posts', lambda p: p.get('published'))
```

---

### Magic Methods (Python Protocols)

#### Dictionary-Style Access

```python
data['key']                  # __getitem__ - nested dicts wrapped
data['key'] = value          # __setitem__ - invalidates cache
del data['key']              # __delitem__ - invalidates cache
'key' in data                # __contains__
```

#### Dot Notation Access

```python
data.key                     # __getattr__ - nested dicts wrapped
data.key = value             # __setattr__ - invalidates cache
```

#### Iteration

```python
len(data)                    # __len__ - number of top-level keys
for key in data:             # __iter__ - iterate top-level keys
    pass
```

#### Comparison

```python
data1 == data2               # __eq__ - uses equals() method
data1 == {'key': 'value'}    # Works with plain dicts too
```

#### Copying

```python
import copy
shallow = copy.copy(data)    # __copy__
deep = copy.deepcopy(data)   # __deepcopy__
```

#### String Representation

```python
repr(data)                   # __repr__ - NitroDataStore({'key': 'value'})
str(data)                    # __str__ - JSON formatted string
print(data)                  # Uses __str__
```

---

## QueryBuilder Class

Created via `NitroDataStore.query(path)`. Provides chainable interface for filtering and transforming lists.

### Constructor

```python
QueryBuilder(collection: List[Any])
```

**Parameters:**
- `collection` (list): List to query

**Returns:** QueryBuilder instance

**Note:** Usually created via `data.query(path)`, not directly.

---

### Filtering Methods

#### where()

```python
where(predicate: Callable[[Any], bool]) -> QueryBuilder
```

**Parameters:**
- `predicate` (callable): Function(item) -> bool

**Returns:** Self for chaining

**Behavior:** Adds filter condition. Multiple where() calls are AND-ed.

**Examples:**
```python
query.where(lambda x: x.get('published') == True)
query.where(lambda x: x.get('views') > 100)
```

---

### Sorting Methods

#### sort()

```python
sort(
    key: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False
) -> QueryBuilder
```

**Parameters:**
- `key` (callable, optional): Function to extract sort key from item
- `reverse` (bool, optional): Sort in reverse order. Default: `False`

**Returns:** Self for chaining

**Examples:**
```python
query.sort(key=lambda x: x.get('date'))
query.sort(key=lambda x: x.get('views'), reverse=True)
query.sort(reverse=True)  # Sort by items themselves
```

---

### Limiting Methods

#### limit()

```python
limit(count: int) -> QueryBuilder
```

**Parameters:**
- `count` (int): Maximum number of results

**Returns:** Self for chaining

**Examples:**
```python
query.limit(10)
```

#### offset()

```python
offset(count: int) -> QueryBuilder
```

**Parameters:**
- `count` (int): Number of results to skip

**Returns:** Self for chaining

**Examples:**
```python
query.offset(5).limit(10)  # Skip first 5, take next 10
```

---

### Execution Methods

#### execute()

```python
execute() -> List[Any]
```

**Parameters:** None

**Returns:** Filtered, sorted, and limited list

**Behavior:** Executes all chained operations and returns results.

**Examples:**
```python
results = query.where(...).sort(...).limit(10).execute()
```

#### count()

```python
count() -> int
```

**Parameters:** None

**Returns:** Number of items matching filters

**Behavior:** Applies filters only, ignores sort/limit/offset.

**Examples:**
```python
total = query.where(lambda x: x.get('published')).count()
```

#### first()

```python
first() -> Optional[Any]
```

**Parameters:** None

**Returns:** First matching item or None

**Behavior:** Executes query with limit(1) and returns first result.

**Examples:**
```python
post = query.where(...).sort(...).first()
```

---

### Extraction Methods

#### pluck()

```python
pluck(key: str) -> List[Any]
```

**Parameters:**
- `key` (str): Key to extract from each item

**Returns:** List of values for the specified key

**Behavior:** Executes query first, then extracts key from each result. None if item isn't dict or key missing.

**Examples:**
```python
titles = query.where(...).pluck('title')
# ['Post 1', 'Post 2', 'Post 3']
```

#### group_by()

```python
group_by(key: str) -> dict
```

**Parameters:**
- `key` (str): Key to group by

**Returns:** Dict mapping key values to lists of items

**Behavior:** Executes query first, then groups results by key value.

**Examples:**
```python
by_category = query.group_by('category')
# {'python': [...], 'web': [...], 'data': [...]}
```

---

## Complete Usage Examples

### Basic CRUD Operations

```python
data = NitroDataStore()

data.set('site.name', 'My Site')
data.set('site.settings.theme', 'dark')

name = data.get('site.name')
theme = data.get('site.settings.theme', 'light')

data.delete('site.settings.theme')

if data.has('site.name'):
    print('Site name exists')
```

### File Operations

```python
data = NitroDataStore.from_file('config.json')

data = NitroDataStore.from_directory('configs/', pattern='*.json')

data.save('output.json', indent=2)
```

### Querying Collections

```python
data = NitroDataStore({
    'posts': [
        {'title': 'Post 1', 'published': True, 'views': 150},
        {'title': 'Post 2', 'published': False, 'views': 50},
        {'title': 'Post 3', 'published': True, 'views': 200}
    ]
})

published = (data.query('posts')
    .where(lambda p: p.get('published'))
    .sort(key=lambda p: p.get('views'), reverse=True)
    .limit(10)
    .execute())

total_published = data.query('posts').where(lambda p: p.get('published')).count()

top_post = data.query('posts').sort(key=lambda p: p.get('views'), reverse=True).first()

all_titles = data.query('posts').pluck('title')
```

### Path Operations

```python
all_paths = data.list_paths()

title_paths = data.find_paths('*.title')
all_authors = data.find_paths('**.author')

urls = data.find_all_keys('url')

images = data.find_values(lambda v: isinstance(v, str) and v.endswith('.jpg'))
```

### Bulk Operations

```python
count = data.update_where(
    lambda p, v: isinstance(v, str) and 'http://' in v,
    lambda v: v.replace('http://', 'https://')
)

count = data.remove_nulls()

count = data.remove_empty()
```

### Transformations

```python
upper = data.transform_all(lambda p, v: v.upper() if isinstance(v, str) else v)

snake_case = data.transform_keys(lambda k: k.replace('-', '_'))

flat = data.flatten()
```

### Comparison

```python
diff = data1.diff(data2)
print(diff['added'])
print(diff['removed'])
print(diff['changed'])

if data1.equals(data2):
    print('Datastores are equal')

if data1 == data2:
    print('Using == operator')
```

### Introspection

```python
info = data.describe()
stats = data.stats()

print(f"Total keys: {stats['total_keys']}")
print(f"Max depth: {stats['max_depth']}")
```

---

## Important Gotchas

### 1. Keys with Dots

```python
data = NitroDataStore({'key.with.dots': 'value'})

data['key.with.dots']        # ✓ Works
data.get('key.with.dots')    # ✗ Returns None (treats as nested path)
```

### 2. Keys with Hyphens (Kebab-Case)

```python
data = NitroDataStore({'user-name': 'John'})

data['user-name']            # ✓ Works
data.user-name               # ✗ Syntax error

data = data.transform_keys(lambda k: k.replace('-', '_'))
data.user_name               # ✓ Now works
```

### 3. Transform Methods Return New Instances

```python
data.transform_keys(lambda k: k.upper())    # ✗ Lost - not assigned
data = data.transform_keys(lambda k: k.upper())  # ✓ Correct
```

### 4. Query Path Must Be a List

```python
data = NitroDataStore({'posts': [], 'site': {}})

data.query('posts')          # ✓ Returns QueryBuilder
data.query('site')           # ✓ Returns empty QueryBuilder (not a list)
data.query('missing')        # ✓ Returns empty QueryBuilder
```

### 5. from_directory Merge Order

Files are merged alphabetically. Later files override earlier ones:

```bash
# Files: 01-base.json, 02-override.json
# 02-override.json values will override 01-base.json for same keys
```

---

## Performance Notes

- `list_paths()` results are cached automatically
- Cache invalidated on any mutation (set, delete, merge, etc.)
- Cache provides 7-100x performance improvement on repeated calls
- Use `filter_list()` or `query()` for collection filtering instead of manual iteration
- Path-based operations (`get`, `set`, `delete`) are optimized for nested access

---

## Type Hints

All methods include proper type annotations:

```python
from typing import Any, Callable, Dict, List, Optional, Union
from pathlib import Path

def get(key: str, default: Any = None) -> Any: ...
def set(key: str, value: Any) -> None: ...
def update_where(
    condition: Callable[[str, Any], bool],
    transform: Callable[[Any], Any]
) -> int: ...
```

Package includes `py.typed` marker for PEP 561 compliance.