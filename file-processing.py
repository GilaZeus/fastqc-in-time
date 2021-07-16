#!/usr/bin/env python3
import datetime
import accnums


def main():
    start_date = datetime.date(2021, 6, 30)
    end_date = datetime.date(2020, 1, 1)
    delta = datetime.timedelta(days=1)

    while start_date >= end_date:
        date_str = "{0}/{1:02d}/{2:02d}".format(start_date.year,
                                        start_date.month,
                                        start_date.day)
        
        with open("tmpdata/" + str(start_date), "w") as data:
            data.write(accnums.get_accnums_body(date_str))
        
        start_date -= delta


if __name__ == "__main__":
    main()
