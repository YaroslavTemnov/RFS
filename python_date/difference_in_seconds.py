from datetime import datetime
today = datetime.now()
some_date = datetime(2006, 1, 7, 11, 42, 11)
result = today - some_date
print(result.seconds)