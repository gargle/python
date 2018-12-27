#!/usr/bin/python3

from datetime import date
from calendar import isleap

# calculate the number of running days for a year (mondays, wednesday and fridays)

for year in range(2009,2039):
    first_day = date(year,1,1).weekday()
    running_days = sum(list(map(lambda y: 1+((366 if isleap(year) else 365)-y)//7,
                                map(lambda x: 7 if (x==0) else x,
                                    [(8-first_day)%7,  # first monday
                                     (10-first_day)%7, # first wednesday
                                     (12-first_day)%7  # first friday
                                    ]
                                ))))
    print(year, running_days)
