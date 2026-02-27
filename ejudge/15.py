from datetime import datetime, timedelta
import re
import sys

def parse(s):
    s = s.strip()
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})\s+UTC([+-])(\d{2}):(\d{2})$', s)
    if not m:
        sys.exit(1)

    y, mo, d, sign_str, h, mi = m.groups()
    y, mo, d, h, mi = map(int, [y, mo, d, h, mi])
    sign = 1 if sign_str == '+' else -1
    
    dt_local = datetime(y, mo, d, 0, 0, 0)
    offset = timedelta(hours=sign * h, minutes=sign * mi)
    
    return dt_local - offset


lines = sys.stdin.read().strip().splitlines()
if len(lines) != 2:
    sys.exit(1)

birth_utc = parse(lines[0])
curr_utc  = parse(lines[1])

by, bm, bd = birth_utc.year, birth_utc.month, birth_utc.day

for year in range(curr_utc.year, curr_utc.year + 3):
    try:
        cand = datetime(year, bm, bd, 0, 0, 0)
    except ValueError:
        if bm == 2 and bd == 29:
            cand = datetime(year, 2, 28, 0, 0, 0)
        else:
            raise
    
    cand_utc = cand
    
    if cand_utc >= curr_utc:
        delta = cand_utc - curr_utc
        print(delta.days)
        break
else:
    sys.exit(1)