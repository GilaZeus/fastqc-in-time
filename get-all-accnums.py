#!/usr/bin/env python3
import datetime
import accnums


def main():
    start_date = datetime.date(2020, 11, 30)
    end_date = datetime.date(2020, 10, 1)
    delta = datetime.timedelta(days=1)

    while start_date >= end_date:
        month = start_date.month

        with open("tmp/" + str(start_date)[: -3], "w") as data:
            while month == start_date.month:
                date_str = "{0}/{1:02d}/{2:02d}".format(start_date.year,
                                                        start_date.month,
                                                        start_date.day)

                for acc_num in accnums.accnum_iter(date_str):
                    if acc_num != "":
                        data.write(acc_num + "\n")
        
                start_date -= delta


if __name__ == "__main__":
    main()
