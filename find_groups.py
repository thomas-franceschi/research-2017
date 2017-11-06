from calc_stats import *

curr_date = date(2017, 8, 29)

csvfile = "BeaconData_Thomas/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

#Read in csv file
master_dict = load_csv(csvfile, curr_date)

group_counts = find_groups(master_dict)

print(group_counts)

print(find_pairs(master_dict))