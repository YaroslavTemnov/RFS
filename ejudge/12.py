import json
import sys


MISSING = object()  


def serialize_value(val):
    if val is MISSING:
        return "<missing>"
    return json.dumps(val, ensure_ascii=False, separators=(",", ":"))


def deep_diff(old, new, path=""):
    diffs = []

    if not isinstance(old, dict) or not isinstance(new, dict):
        if old != new:
            old_str = serialize_value(old)
            new_str = serialize_value(new)
            diffs.append((path, old_str, new_str))
        return diffs

    all_keys = sorted(set(old) | set(new))

    for key in all_keys:
        curr_path = f"{path}.{key}" if path else key

        val_old = old.get(key, MISSING)
        val_new = new.get(key, MISSING)

        if val_old is MISSING or val_new is MISSING:
            old_str = serialize_value(val_old)
            new_str = serialize_value(val_new)
            diffs.append((curr_path, old_str, new_str))
            continue

        if isinstance(val_old, dict) and isinstance(val_new, dict):
            diffs.extend(deep_diff(val_old, val_new, curr_path))
            continue

        if val_old != val_new:
            old_str = serialize_value(val_old)
            new_str = serialize_value(val_new)
            diffs.append((curr_path, old_str, new_str))

    return diffs

data = sys.stdin.read().strip().splitlines()

if len(data) != 2:
    sys.exit(1)

try:
    A = json.loads(data[0])
    B = json.loads(data[1])
except json.JSONDecodeError:
    sys.exit(1)

differences = deep_diff(A, B)

if not differences:
    print("No differences")
else:
    differences.sort(key=lambda x: x[0])

    for path, old_val, new_val in differences:
        print(f"{path} : {old_val} -> {new_val}")