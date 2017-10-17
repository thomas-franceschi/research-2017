from calc_stats import *

#Read in csv file
master_dict = load_csv(csvfile)

#plot file
plot_gantt_region(master_dict, user)	

#calc beacon frequency
freq_dict = calc_beacon_freq(master_dict, int(52))

#plot beacon frequency
plot_beacon_freq(freq_dict)