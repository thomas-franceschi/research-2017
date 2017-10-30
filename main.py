from calc_stats import *
import codecs


i = int(0)
beacon_id = int(51)

curr_date = date(2017, 8, 26)

num_pairs = []
dates = []

while i < 7:
	print(curr_date)
	dates.append(curr_date)
	csvfile = "BeaconData_Thomas/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

	#Read in csv file
	master_dict = load_csv(csvfile, curr_date)

	#plot file
	#plot_gantt_region(master_dict, user)	

	#calc beacon frequency
	#freq_dict = calc_beacon_freq(master_dict, beacon_id)

	#plot beacon frequency
	#plot_beacon_freq(freq_dict, beacon_id, curr_date)

	num = find_pairs(master_dict)

	print(num)
	num_pairs.append(num)

	curr_date += timedelta(days=1)
	i+=1
	master_dict.clear()
	#freq_dict.clear()

trace = go.Scatter(
		x = dates,
		y = num_pairs
	)

data = [trace]

py.iplot(data, filename=curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + "pairs")