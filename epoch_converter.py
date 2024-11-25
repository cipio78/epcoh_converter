import time
from datetime import date
import argparse
import re
import sys


parser = argparse.ArgumentParser(description="""A python script to turn two dates into earliest and latest epoch timestamps, maily for Splunk usage.""")
parser.add_argument('-e', '--earliest', help='The beginning date for your search')
parser.add_argument('-l', '--latest', help='The end date for you search.')
parser.add_argument('-d', '--delimiter', default='/',help='The delimiter for the date.  Deafult is "/"')
parser.add_argument('-r', '--reverse', nargs=1, help='convert epoch timestamp ')
parser.add_argument('-f', '--format', default='MM/DD/YYYY', help='The order used for the date.  Currently there are not other optoins than MM/DD/YYYY format and this arugumetn is not currently used.')


args = parser.parse_args()
split_character= args.delimiter

def delimiter_check(date):
    if args.delimiter not in date:
        print(f'The delimiter {args.delimiter} was not found in {date}.  Stopping script')
        sys.exit(0)

def year_check(year):
    if len(year) != 4 or not 1970 <= int(year) <= 4000 :
        print(f'{year} is not a valid year.  Stopping script')
        sys.exit(0)

def month_check(month):
    if len(month) > 2 or not 1 <= int(month) <= 12:
        print(f'{month} is not a valid month.  Stopping script')
        sys.exit(0)

def day_check(day):
    if len(day) > 2 or not 1 <= int(day) <= 31:
        print(f'{day} is not a valid day.  Stopping script')
        sys.exit(0)

def main():
        if args.earliest and args.latest and not args.reverse:
                delimiter_check(args.earliest)
                delimiter_check(args.latest)

                early = re.split(split_character, args.earliest) 
                late = re.split(split_character, args.latest)


                year_check(early[2])
                year_check(late[2])

                month_check(early[0])
                month_check(late[0])

                day_check(early[1])
                day_check(late[1])

                tuple_early = date(int(early[2]), int(early[0]), int(early[1]))
                tuple_late = date(int(late[2]), int(late[0]), int(late[1]))

                ut_earliest = int(time.mktime(tuple_early.timetuple()))
                ut_latest = int(time.mktime(tuple_late.timetuple()))

                if ut_latest >=  ut_earliest:
                        print(f'\r\nHere is your Splunk time entries.\r\nearliest={ut_earliest} latest={ut_latest}')
                else:
                        print(f'\r\nYour latest time comes before the earliest.  Stopping Script')
                        sys.exit(0)
        elif args.reverse and not (args.earliest or args.latest):
                reg_time = time.strftime('%m/%d/%Y', time.localtime(int(args.reverse[0])))
                print(f'\r\nEpoch timestamp {args.reverse[0]} is {reg_time}')
        elif args.reverse and (args.earliest or args.latest):
                print(f'\r\nYou cannot convert a date into epoch time stamp while trying to convert a epoch timestampt to date.  Existing script')
                sys.exit(0)
        elif args.earliest or args.latest:
                print(f'\r\nYou must enter both the earliest date and latest date.  Exiting script')
                sys.exit(0)
        
if __name__ == "__main__":
    main()