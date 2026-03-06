import re

s = input()

email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{1,}\b'
email = re.search(email_pattern,s )
if email:
    print(email.group())
else:
    print("No email")