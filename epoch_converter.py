import time
from datetime import date

d = date(2020, 10,4)

unixtime = int(time.mktime(d.timetuple()))

print(unixtime)