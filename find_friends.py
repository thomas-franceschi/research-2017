from calc_stats import *

curr_date = date(2017, 8, 26)

pair_dict = {}
i = 0

while i < 30:
	print(i)
	csvfile = "BeaconData_Thomas/sortedCSVs/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

	#Read in csv file
	master_dict = load_csv(csvfile, curr_date)

	#Find pairs for the day
	(pairs, count) = find_pairs(master_dict)

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
			


for key in pair_dict.keys():
	if pair_dict[key] > 1:
		print(','.join(key) + " : " + str(pair_dict[key]))

