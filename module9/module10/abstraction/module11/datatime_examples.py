import datetime

current_datetime = datetime.datetime.now()

print("Year:",current_datetime.year)
print("Month:",current_datetime.month)
print("Day:",current_datetime.day)

current_date = datetime.datetime.now().date()
print(current_date)

current_date = datetime.datetime.now().time()
print(current_date)