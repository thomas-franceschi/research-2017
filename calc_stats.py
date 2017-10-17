import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import plotly.figure_factory as ff
import csv
from datetime import *
from params import *
from global_vars import *

#csv to read in
csvfile = "ndMobile_" + str(year) + "-" + str(month) + "-" + str(day) + ".csv"

#beacon groups
locations = {
	"entrance" 		: [58, 27, 51, 110],
	"r_beverages" 	: [100, 21, 97],
	"l_beverages" 	: [46, 43, 44],
	"home_style" 	: [4, 10],
	"grill" 		: [97, 21, 10, 46, 83],
	"pasta" 		: [13, 16, 40, 23, 9],
	"mexican" 		: [23, 40, 3, 99, 114],
	"salad" 		: [54, 26, 12, 9, 40, 16, 13],
	"stir_fry" 		: [78, 54, 26, 10],
	"sandwich" 		: [46, 83, 44, 43, 13],
	"pizza" 		: [101, 49, 44],
	"bread" 		: [57, 35, 3, 99, 26, 12, 54],
	"cereal" 		: [78, 54, 26, 110, 57],
	"left_dining" 	: [51, 47, 67, 102, 41],
	"right_dining" 	: [27, 53, 104, 64, 55] 
	}

#authenticate to plotly
plotly.tools.set_credentials_file(username=USERNAME, api_key=KEY)

def load_csv( filename ):
	
	users_dict = {}
	single_user_dict = {}

	with open(filename) as file:
		#Begin reading file
		infile = csv.reader(file)

		#skip header
		next(infile)

		#Iterate through lines of csv file
		for entry in infile:

			user_id 		= entry[0]
			beacon_id 		= entry[9]
			dwell_time 		= entry[13]
			entry[5] 		= entry[5][:18]
			entry[6] 		= entry[6][:18]

			#Skip non-dining hall beacons
			if entry[3] != '7':
				continue
				
			#Skip less than 1 minute dwell
			if int(dwell_time) < 1:
				continue
			
			#Skip absurd length dwells
			if int(dwell_time) >= 60:
				continue

			time_entered 	= datetime.strptime(entry[5], "%Y-%m-%d %H:%M:%S")
			time_exited 	= datetime.strptime(entry[6], "%Y-%m-%d %H:%M:%S")

			#skip off-hours
			if time_entered < start_time or time_entered > end_time:
				continue

			#if no user sub-dict, create
			if user_id not in users_dict.keys():
				users_dict[user_id] = {}

			#insert into dicts
			#single_user_dict[(beacon_id,time_entered)] = [ time_entered, time_exited, dwell_time ]
			users_dict[user_id][(beacon_id,time_entered)] = [ time_entered, time_exited, dwell_time ]

			single_user_dict.clear

	return (users_dict)

#calculate frequency of users over time for a beacon
###IN PROGRESS###
def calc_beacon_freq( users_dict, beacon_id ):

	num = int(beacon_id)
	freq_dict = {} #(time_of_day,num_hits)
	min = timedelta(minute=1)

	#iterate through all users
	for user in user_dict:
		#iterate through each session for a given user
		for touple, beacons in user_dict[user].items():
			#filter for current beacon only
			if int(touple[0]) != num:
				continue
			
			curr_time 	= beacons[0]
			end 		= beacons[1]
			dwell 		= beacons[2]

			#increment value for each minute user was in range
			while curr_time <= end:
				if curr_time.strftime("%H:%M:%S") not in freq_dict.keys():
					freq_dict[curr_time.strftime("%H:%M:%S")] = int(1)
				else:
					freq_dict[curr_time.strftime("%H:%M:%S")] += 1

				curr_time = curr_time + min

	return freq_dict

def plot_gantt_region( master_dict, user ):
	#build user dict
	df = []
	for touple, beacons in master_dict[user].items():
		beacon_id = str(touple[0])
		print(beacon_id)
		start = beacons[0].strftime("%Y-%m-%d %H:%M:%S")
		finish = beacons[1].strftime("%Y-%m-%d %H:%M:%S")

		#find region
		for region in locations.keys():
			if int(beacon_id) in locations[region]:
					beacon_dict = dict(Task=region, Start=start, Finish=finish, Resource='Complete')
					df.append(beacon_dict)

	#			beacon_dict = dict(Task=beacon_id, Start=start, Finish=finish, Resource='Complete')
	#			df.append(beacon_dict)

	colors = {'Not Started': 'rgb(220, 0, 0)','Incomplete': (1, 0.9, 0.16), 'Complete': 'rgb(0, 255, 100)'}

	fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=False, group_tasks=True)
	py.iplot(fig, filename='gantt-group-6', world_readable=True)

	return

def print_dict( users_dict ):
	for user, beacon in users_dict.items():
		print (user)
	return

def print_user( users_dict, user ):
	for touple, beacons in users_dict[user].items():
		print (str(touple) + ": " + str(beacons))
	return

if __name__ == "__main__":
	
	#init dicts
	beacon_dwell 	= {}
	beacon_count 	= {}
	beacon_avg 		= {}

	user_beacon_dwell 	= {}
	user_beacon_count 	= {}
	user_beacon_avg 	= {}

	#Read in csv file
	master_dict = load_csv(csvfile)

	with open(csvfile) as file:
		dwell_sum 	= 0
		dwell_avg 	= 0
		count 		= 0
		incsv 		= csv.reader(file)

		user_num_beacons = 0

		#Skip Header
		next(incsv)

		#Iterate through csv
		for entry in incsv:

			#Sum total dwell times
			dwell_sum += int(entry[13])
			count += 1

			#Sum per beacon dwell times
			if(str(entry[7]) not in beacon_count):
				beacon_count[str(entry[9])] = int(1)
				beacon_dwell[str(entry[9])] = int(entry[13])
			else:
				beacon_count[str(entry[9])] += int(1)
				beacon_dwell[str(entry[9])] += int(entry[13])

			#Track user statistics
			if entry[0] == user:
				user_num_beacons += 1
				if(str(entry[7]) not in user_beacon_count):
					user_beacon_count[str(entry[9])] = int(1)
					user_beacon_dwell[str(entry[9])] = int(entry[13])
				else:
					user_beacon_count[str(entry[9])] += int(1)
					user_beacon_dwell[str(entry[9])] += int(entry[13])


		#Calc avg results
		dwell_avg = dwell_sum / count
		titles = []
		values = []

		user_titles = []
		user_values = []

		#Calculate averages per beacon
		for beacon, tot in sorted(beacon_dwell.items()):
			beacon_avg[beacon] = tot/beacon_count[beacon]
			if beacon_avg[beacon] != 0:
				#print("beacon " + beacon + " avg: " + str(beacon_avg[beacon]))
				titles.append(str(beacon))
				values.append(beacon_avg[beacon])

		#calculate user statistics
		for beacon, tot in sorted(user_beacon_dwell.items()):
			user_beacon_avg[beacon] = tot/user_beacon_count[beacon]
			if beacon_avg[beacon] != 0:
				#print("beacon " + beacon + " avg: " + str(user_beacon_avg[beacon]))
				user_titles.append(str(beacon))
				user_values.append(beacon_avg[beacon])

		print('Dwell sum: ' + str(dwell_sum) + '\n' + 'Dwell_avg: ' + str(dwell_avg))
		print("user: " + str(user))
		print("beacon count: " + str(user_beacon_count))

		#Plot to plotly
		data = [go.Bar(
				x=titles,
				y=values
		)]

		#py.iplot(data, filename='avg_dwell_bar')

		user_data = [go.Bar(
				x=user_titles,
				y=user_values
		)]

		#py.iplot(user_data, filename='user_avg_dwell_bar')

		#Plot single user gantt
		plot_gantt_region(master_dict, user)	