import sys
from calc_stats import *

curr_date = date(2017, 8, 26)
pairs_per_day = []
pair_dict = {}
i = 0

while i < 35:
	sys.stdout.write('.')
	sys.stdout.flush()
	#print(i)
	csvfile = "BeaconData_Thomas/sortedCSVs/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

	#Read in csv file
	master_dict = load_csv(csvfile, curr_date)

	#Find pairs for the day
	(pairs, count) = find_pairs(master_dict)
	pairs_per_day.append(count)

	#Increment pair counts
	for pair in pairs:
		pair = sorted(pair)
		pair = tuple(pair)
		if pair not in pair_dict:
			pair_dict[pair] = int(1)
		else:
			pair_dict[pair] += 1

	curr_date += timedelta(days=1)
	i+=1

	master_dict.clear()
			


#print pairs per day
print('')
print(pairs_per_day)

frequencies_dict = {}

#print pairs of notable frequency and build frequencies dict
for key in pair_dict.keys():

	#if val not present create new entry
	if str(pair_dict[key]) not in frequencies_dict:
		frequencies_dict[str(pair_dict[key])] = int(1)
	else:
		frequencies_dict[str(pair_dict[key])] += 1

	#print pairs >= 12.5% frequency
	#if pair_dict[key] >= i/10:
	#	print(','.join(key) + " : " + str(pair_dict[key]))

#
print(frequencies_dict)