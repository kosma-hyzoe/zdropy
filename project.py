import argparse
from datetime import datetime

import schedule as schedule
from croniter import croniter


def main():
    parser_args = get_parser_args()

    if parser_args.schedule:
        schedule_registration(parser_args.schedule)


def register(class_name, day_of_week, hour):
    pass

    # if registration fails, it should automatically schedule a retry (i.e. after 10 minutes)


def schedule_registration(class_time):
    cron = croniter(class_time, datetime.now())
    next_registration_time = cron.get_next()

    schedule.every().week.at(next_registration_time).do(register)


def retry(after=10):
    pass

def get_parser_args():
    pass

if __name__ == '__main__':
    main()
