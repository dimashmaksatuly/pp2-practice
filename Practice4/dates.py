from datetime import datetime, timedelta

# current date
now = datetime.now()
print(now)

# create specific date
d = datetime(2025, 1, 1)
print(d)

# formatting
print(now.strftime("%Y-%m-%d"))

# difference
diff = now - d
print(diff.days)

# add time
future = now + timedelta(days=5)
print(future)