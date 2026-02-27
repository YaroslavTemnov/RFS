from datetime import datetime, timedelta
import re
import sys


def parse_datetime_with_offset(s: str) -> datetime:
 
    s = s.strip()

    match = re.match(r'(\d{4}-\d{2}-\d{2})\s*UTC([+-]\d{1,2}):(\d{2})', s)
    if not match:
        raise ValueError("")

    date_part = match.group(1)
    sign = match.group(2)[0]
    hours = int(match.group(2)[1:])
    minutes = int(match.group(3))

    dt = datetime.strptime(date_part, "%Y-%m-%d")

    offset_seconds = hours * 3600 + minutes * 60
    if sign == '-':
        offset_seconds = -offset_seconds

    utc_dt = dt - timedelta(seconds=offset_seconds)

    return utc_dt

lines = sys.stdin.read().strip().splitlines()

if len(lines) != 2:
    sys.exit(1)

try:
    dt1 = parse_datetime_with_offset(lines[0])
    dt2 = parse_datetime_with_offset(lines[1])
except Exception as e:
    sys.exit(1)


delta_seconds = abs((dt1 - dt2).total_seconds())

days = int(delta_seconds // 86400)

print(days)