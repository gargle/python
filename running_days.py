#!/usr/bin/python3

from calendar import isleap, monthrange

# calculate the number of running days for a year (mondays, wednesday and fridays)

print("year  total  ja fe ma ap ma ju ju au se oc no de")
for year in range(2009,2039):
    running_days = []
    for month in range(1,13):
        (first_day, total_days) = monthrange(year,month)
        running_days.append(sum(list(map(lambda y: 1+(total_days-y)//7,
                                      map(lambda x: 7 if (x==0) else x,
                                          [(8-first_day)%7,  # first monday
                                           (10-first_day)%7, # first wednesday
                                           (12-first_day)%7  # first friday
                                          ]
                                      )))))
    print("%4d   %3d  " % (year, sum(running_days)),end='')
    for month in range(0,12):
        print(" %2d" % running_days[month], end='')
    print("")
