from datetime import datetime, timedelta
today = datetime.now()
result = today - timedelta(days = 5)
print(result.strftime("%Y-%m-%d"))