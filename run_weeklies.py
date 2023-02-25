import pickle

import schedule
import sys


def main():
    with open("jobs.pickle", "rb") as f:
        jobs = pickle.load(f)
    for job in jobs:
        schedule.jobs.append(job)

    while True:
        try:
            schedule.run_pending()
        except EOFError:
            sys.exit(0)


if __name__ == '__main__':
    main()
