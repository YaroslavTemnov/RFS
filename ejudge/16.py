from datetime import datetime, timezone, timedelta

def parse_with_offset(s: str):

    dt_part, tz_part = s.split(" UTC")
    dt = datetime.strptime(dt_part, "%Y-%m-%d %H:%M:%S")
    

    sign = 1 if tz_part[0] == "+" else -1
    h, m = map(int, tz_part[1:].split(":"))
    offset_sec = sign * (h * 3600 + m * 60)
    
    return dt - timedelta(seconds=offset_sec)


start_str = input().strip()
end_str   = input().strip()

start_utc = parse_with_offset(start_str)
end_utc   = parse_with_offset(end_str)

duration = int((end_utc - start_utc).total_seconds())
print(duration)