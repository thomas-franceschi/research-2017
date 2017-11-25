from calc_stats import *

curr_date = date(2017, 8, 26)

count_freq = {}
i = 0

while i < 9:
	print(i)
	csvfile = "BeaconData_Thomas/sortedCSVs/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

	#Read in csv file
	master_dict = load_csv(csvfile, curr_date)

	group_counts = find_groups(master_dict)



	for group in group_counts:
		if group not in count_freq:
			count_freq[group] = 1
		else:
			count_freq[group] += 1

	curr_date += timedelta(days=1)
	i+=1
	master_dict.clear()
			
print(count_freq)

counts = []
nums = []

for x, y in count_freq.items():
	counts.append(y)
	nums.append(x)

#print(find_pairs(master_dict))


trace = go.Bar(
		x = nums,
		y = counts
	)

data = [trace]

py.iplot(data, filename=curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + "groups")