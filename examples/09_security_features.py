"""
Example 09: Security Features

Demonstrates security protections built into NitroDataStore:
1. Path traversal protection
2. File size limits
3. Path validation
4. Circular reference protection
"""

import json
import tempfile
from pathlib import Path
from nitro_datastore import NitroDataStore


def section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def demo_path_traversal_protection():
    section("1. Path Traversal Protection")

    print("\nProtects against directory traversal attacks when loading files.")
    print("Use the 'base_dir' parameter to restrict file access to a specific directory.")

    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir) / 'safe'
        safe_dir.mkdir()
        unsafe_dir = Path(tmpdir) / 'unsafe'
        unsafe_dir.mkdir()

        (safe_dir / 'config.json').write_text('{"allowed": true}')
        (unsafe_dir / 'secrets.json').write_text('{"secret": "password123"}')

        print(f"\nDirectory structure:")
        print(f"  {tmpdir}/")
        print(f"    safe/")
        print(f"      config.json")
        print(f"    unsafe/")
        print(f"      secrets.json")

        print("\n✓ Loading file within base_dir (ALLOWED):")
        data = NitroDataStore.from_file(safe_dir / 'config.json', base_dir=safe_dir)
        print(f"  Loaded: {data.to_dict()}")

        print("\n✗ Attempting to load file outside base_dir (BLOCKED):")
        try:
            evil_path = safe_dir / '..' / 'unsafe' / 'secrets.json'
            data = NitroDataStore.from_file(evil_path, base_dir=safe_dir)
            print(f"  ERROR: Should have been blocked!")
        except ValueError as e:
            print(f"  Blocked: {e}")

        print("\n✓ Loading without base_dir (backward compatible):")
        data = NitroDataStore.from_file(unsafe_dir / 'secrets.json')
        print(f"  Loaded: {data.to_dict()}")
        print(f"  Note: Only use without base_dir for trusted paths")


def demo_file_size_limits():
    section("2. File Size Limits")

    print("\nProtects against out-of-memory attacks from large files.")
    print("Use the 'max_size' parameter to limit file size in bytes.")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        small_file = tmpdir / 'small.json'
        small_file.write_text('{"size": "small"}')

        large_file = tmpdir / 'large.json'
        large_data = {"data": "x" * 100000}
        large_file.write_text(json.dumps(large_data))

        small_size = small_file.stat().st_size
        large_size = large_file.stat().st_size

        print(f"\nFiles:")
        print(f"  small.json: {small_size} bytes")
        print(f"  large.json: {large_size} bytes")

        print(f"\n✓ Loading small file with 10KB limit (ALLOWED):")
        data = NitroDataStore.from_file(small_file, max_size=10*1024)
        print(f"  Loaded successfully")

        print(f"\n✗ Attempting to load large file with 10KB limit (BLOCKED):")
        try:
            data = NitroDataStore.from_file(large_file, max_size=10*1024)
            print(f"  ERROR: Should have been blocked!")
        except ValueError as e:
            print(f"  Blocked: {e}")

        print(f"\n✓ Loading large file without limit (backward compatible):")
        data = NitroDataStore.from_file(large_file)
        print(f"  Loaded successfully")
        print(f"  Note: Only use without max_size for trusted sources")


def demo_path_validation():
    section("3. Path Validation")

    print("\nValidates path strings in path-based methods (get, set, delete, has).")
    print("Rejects malformed paths that could cause errors or unexpected behavior.")

    data = NitroDataStore({'user': {'name': 'Alice', 'age': 30}})

    print("\n✓ Valid paths (ALLOWED):")
    valid_paths = ['user', 'user.name', 'user.age', 'config.theme.color']
    for path in valid_paths:
        try:
            result = data.has(path)
            print(f"  '{path}' -> exists={result}")
        except ValueError:
            print(f"  '{path}' -> ERROR")

    print("\n✗ Invalid paths (REJECTED):")
    invalid_paths = [
        ('', 'empty string'),
        ('   ', 'whitespace only'),
        ('.', 'single dot'),
        ('..', 'double dots'),
        ('.foo', 'leading dot'),
        ('foo.', 'trailing dot'),
        ('foo..bar', 'consecutive dots')
    ]

    for path, description in invalid_paths:
        try:
            data.get(path)
            print(f"  '{path}' ({description}) -> ERROR: Should have been rejected!")
        except ValueError as e:
            print(f"  '{path}' ({description}) -> Rejected")

    print("\nWhy this matters:")
    print("  - Prevents accidental bugs from malformed paths")
    print("  - Catches typos early (e.g., 'user..name')")
    print("  - Ensures consistent path behavior")


def demo_circular_reference_protection():
    section("4. Circular Reference Protection")

    print("\nDetects circular references to prevent infinite recursion.")
    print("Applied during deep copy, merge, and serialization operations.")

    print("\n✓ Normal nested structures (ALLOWED):")
    normal_data = {
        'level1': {
            'level2': {
                'level3': {
                    'value': 'deep'
                }
            }
        }
    }
    data = NitroDataStore(normal_data)
    copied = data.to_dict()
    print(f"  Successfully copied nested structure")
    print(f"  Depth: 4 levels")

    print("\n✗ Circular reference in dict (DETECTED):")
    circular_dict = {'a': 1}
    circular_dict['self'] = circular_dict

    try:
        data = NitroDataStore(circular_dict)
        exported = data.to_dict()
        print(f"  ERROR: Should have detected circular reference!")
    except ValueError as e:
        print(f"  Detected: {e}")

    print("\n✗ Circular reference in list (DETECTED):")
    circular_list = [1, 2, 3]
    circular_list.append(circular_list)

    try:
        result = NitroDataStore._deep_copy(circular_list)
        print(f"  ERROR: Should have detected circular reference!")
    except ValueError as e:
        print(f"  Detected: {e}")

    print("\n✗ Circular reference during merge (DETECTED):")
    data = NitroDataStore({'config': {}})
    data._data['config']['self'] = data._data['config']
    overlay = {'config': {'self': {'new': 'value'}}}

    try:
        data.merge(overlay)
        print(f"  ERROR: Should have detected circular reference!")
    except ValueError as e:
        print(f"  Detected: {e}")

    print("\nWhy this matters:")
    print("  - Prevents infinite recursion and stack overflow")
    print("  - Protects against malicious or corrupted data")
    print("  - Ensures operations complete successfully")


def demo_combined_protections():
    section("5. Combined Protections")

    print("\nSecurity features can be combined for defense in depth.")

    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir) / 'data'
        safe_dir.mkdir()

        config_file = safe_dir / 'config.json'
        config_file.write_text('{"app": "secure", "version": "1.0"}')

        print(f"\n✓ Loading with both path and size protections:")
        data = NitroDataStore.from_file(
            config_file,
            base_dir=safe_dir,
            max_size=1024*1024
        )
        print(f"  Loaded: {data.to_dict()}")
        print(f"  - Path validated against base_dir")
        print(f"  - Size checked against max_size")

        print(f"\n✓ All operations validate paths:")
        data.set('app.name', 'SecureApp')
        print(f"  set() validated path: 'app.name'")

        value = data.get('app.name', 'default')
        print(f"  get() validated path: 'app.name' -> '{value}'")

        exists = data.has('app.version')
        print(f"  has() validated path: 'app.version' -> {exists}")


def demo_security_best_practices():
    section("6. Security Best Practices")

    print("\n✓ DO: Use base_dir for user-supplied paths")
    print("  data = NitroDataStore.from_file(user_path, base_dir='/safe/uploads')")

    print("\n✓ DO: Use max_size to prevent DoS attacks")
    print("  data = NitroDataStore.from_file(path, max_size=10*1024*1024)  # 10MB")

    print("\n✓ DO: Validate paths early with has() before operations")
    print("  if data.has(user_key):")
    print("      value = data.get(user_key)")

    print("\n✓ DO: Use try-except for error handling")
    print("  try:")
    print("      data = NitroDataStore.from_file(path, base_dir=safe_dir)")
    print("  except (FileNotFoundError, ValueError) as e:")
    print("      log_error(e)")

    print("\n✗ DON'T: Skip security checks for convenience")
    print("  # Bad: Allows path traversal")
    print("  data = NitroDataStore.from_file(user_path)  # No base_dir!")

    print("\n✗ DON'T: Use very large max_size values")
    print("  # Bad: Still vulnerable to large files")
    print("  data = NitroDataStore.from_file(path, max_size=1024**4)  # 1TB!")

    print("\n✗ DON'T: Ignore validation errors")
    print("  # Bad: Silently fails")
    print("  try:")
    print("      data.get('')")
    print("  except ValueError:")
    print("      pass  # Error ignored!")


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    NitroDataStore Security Features                  ║
║                                                                      ║
║  Comprehensive security protections for safe data operations        ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    demo_path_traversal_protection()
    demo_file_size_limits()
    demo_path_validation()
    demo_circular_reference_protection()
    demo_combined_protections()
    demo_security_best_practices()

    print(f"\n{'='*70}")
    print("Security features demonstration complete!")
    print('='*70)


if __name__ == '__main__':
    main()