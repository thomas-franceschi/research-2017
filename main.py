from calc_stats import *
import codecs


i = int(0)
beacon_id = int(51)

curr_date = date(2017, 8, 26)

while i < 5:
	print(curr_date)
	csvfile = "BeaconData_Thomas/ndMobile_" + curr_date.strftime("%Y") + "-" + curr_date.strftime("%m") + "-" + curr_date.strftime("%d") + ".csv"

	#Read in csv file
	master_dict = load_csv(csvfile)

	#plot file
	#plot_gantt_region(master_dict, user)	

	#calc beacon frequency
	freq_dict = calc_beacon_freq(master_dict, beacon_id)

	#plot beacon frequency
	plot_beacon_freq(freq_dict, beacon_id, curr_date)

	curr_date += timedelta(days=1)
	i+=1
	master_dict.clear()
	freq_dict.clear()