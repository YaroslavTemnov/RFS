import json
import sys


def apply_patch(source, patch):

    if not isinstance(patch, dict):
        return patch

    result = source.copy() if isinstance(source, dict) else {}

    for key, patch_value in patch.items():
        if patch_value is None:
            result.pop(key, None)
        elif isinstance(patch_value, dict) and isinstance(result.get(key), dict):
            result[key] = apply_patch(result.get(key, {}), patch_value)
        else:
            result[key] = patch_value

    return result


input_lines = sys.stdin.read().strip().splitlines()

if len(input_lines) != 2:
    sys.exit("Ожидалось ровно две строки: source и patch")

source_str = input_lines[0].strip()
patch_str  = input_lines[1].strip()

try:
    source = json.loads(source_str)
    patch  = json.loads(patch_str)
except json.JSONDecodeError:
    sys.exit("Некорректный JSON во входных данных")

result = apply_patch(source, patch)

print(json.dumps(result, ensure_ascii=False, separators=(',', ':'), sort_keys=True))