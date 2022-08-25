import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import copy
import pytz
import statistics
import numpy as np


def clean_data_rewrite( audio_or_activity ):
    user_data = []
    users = []

    start_date = None
    end_date = None

    for user in range (61):
        username  = str (user)
        if int(user/10) == 0:
            username = "0"+username

        #print(username)
        try:
            file_name  = '/Users/gagesh/Documents/dataset/dataset/sensing/{}/{}_u{}.csv'.format(audio_or_activity, audio_or_activity, username)
            print(file_name)
            csv_activity = open(file_name, mode='r')
        except Exception as e :
            print(e)
            continue
        csv_activity_reader = csv.DictReader(csv_activity)

        users.append(username)
        timestamps = []
        activities = []

        for row in csv_activity_reader:
            #dartmouth_timezone = 'America/New_York'
            #NY = pytz.timezone(dartmouth_timezone)

            dt_obj = datetime.fromtimestamp(int(list(row.values())[0]))  # row['timestamp']))
            activity = int(int(list(row.values())[1]))  # row[' activity inference'])

            timestamps.append(dt_obj)
            activities.append(activity)

        #user_datetime_list = []
        user_activity_list = []
        last_hour_activity = []

        last_date = 0

        quarters = []
        activity_sum = []

        last_dt_obj = 0

        #print(type(csv_activity_reader))
        i = 0
        while i < len(timestamps):
            #dt_obj = datetime.fromtimestamp(int(list(row.values())[0]))  # row['timestamp']))
            #activity = int(int(list(row.values())[1]))  # row[' activity inference'])

            dt_obj = timestamps[i]
            activity = activities[i]

            hour = dt_obj.hour
            date = dt_obj.date()

            if(i == 0):
                last_hour = hour
                last_date = date
                last_dt_obj = dt_obj



            diff = dt_obj - last_dt_obj

            diff_seconds = diff.days*(24*60*60)  + diff.seconds

            if diff_seconds > 60*15:
                print(dt_obj,last_dt_obj,diff_seconds)
                k = i-1

                # lets check for last week's same slot data, if its not there we will take previous days data
                num_weeks_behind = int(diff.days/7)
                go_back = timedelta(hours=(num_weeks_behind+1)*7*24)

                last_day_dt_object = last_dt_obj - go_back

                if last_day_dt_object < timestamps[0]:
                    go_back = timedelta(hours=(diff.days+1)*24)
                    last_day_dt_object = last_dt_obj - go_back
                    if last_day_dt_object < timestamps[0]:
                        print("Intial data cut")
                        last_dt_obj = dt_obj
                        timestamps = timestamps[i:]
                        activities = activities[i:]
                        i = 1
                        continue


                print(last_day_dt_object)
                #last_day_dt_object = last_dt_obj - go_back
                #print("last_day: ", last_day_dt_object)
                missed_timestamps = []
                missed_activities = []

                start_time_stamp_idx = -1
                end_time_stamp_idx = -1

                for j in range(0, 60*15):
                    last_day_second = last_day_dt_object + timedelta(seconds = j)
                    if last_day_second in timestamps:
                        start_time_stamp_idx = timestamps.index(last_day_second)
                        break

                if start_time_stamp_idx != -1:
                    for j in range(diff_seconds, diff_seconds-15*60, -1):
                        last_day_second = last_day_dt_object + timedelta(seconds=j)
                        if last_day_second in timestamps:
                            end_time_stamp_idx = timestamps.index(last_day_second)
                            break

                if start_time_stamp_idx != -1 and end_time_stamp_idx != -1:
                    count = end_time_stamp_idx - start_time_stamp_idx + 1
                    #print(timestamps[ start_time_stamp_idx:start_time_stamp_idx+count])
                    missed_activities = activities[start_time_stamp_idx: start_time_stamp_idx + count]
                    missed_timestamps = timestamps[ start_time_stamp_idx: start_time_stamp_idx+count ]

                    for ts_idx in range(len(missed_timestamps)):
                        missed_timestamps[ts_idx] = missed_timestamps[ts_idx] + go_back


                else:
                    # the code can't come here according to the above logic, but if it comes there can be a bug
                    print("some code bug")

                #print(missed_timestamps)

                timestamps = timestamps[:i] + missed_timestamps + timestamps[i:]
                activities = activities[:i] + missed_activities + activities[i:]

                continue

            if last_date != date:

                #print(last_date, date)
                last_date = date

            i += 1
            last_dt_obj = dt_obj

        i = 0

        while i < len(timestamps):
            # dt_obj = datetime.fromtimestamp(int(list(row.values())[0]))  # row['timestamp']))
            # activity = int(int(list(row.values())[1]))  # row[' activity inference'])

            dt_obj = timestamps[i]
            activity = activities[i]

            hour = dt_obj.hour
            date = dt_obj.date()


            if (i == 0):
                last_hour = hour
                last_date = date
                last_dt_obj = dt_obj
                user_start_date = date

            # print(dt_obj)

            diff = dt_obj - last_dt_obj
            diff_seconds = diff.seconds

            if diff_seconds > 15*60:
                print(dt_obj, last_dt_obj, diff_seconds)

            last_hour_activity.append(activity)

            if last_hour != hour:

                if last_hour < 10 or last_hour > 22:
                    last_hour_activity = []
                    last_hour = hour
                    continue

                count = len(last_hour_activity)
                q = count / 4
                q = int(q)
                # print(q, count)
                # print("hello")
                # print(len(last_hour_activity[0:q]))

                quarter_activities = [sum(last_hour_activity[0:q]) / len(last_hour_activity[0:q]),
                                      sum(last_hour_activity[q:2 * q]) / len(last_hour_activity[q:2 * q]),
                                      sum(last_hour_activity[2 * q:3 * q]) / len(last_hour_activity[2 * q:3 * q]),
                                      sum(last_hour_activity[3 * q:]) / len(last_hour_activity[3 * q:])]

                last_hour_str = str(last_hour)
                if last_hour / 10 == 0:
                    last_hour_str = "0" + last_hour_str

                date_time_str = "{} {}:{}:{}".format(last_date, last_hour_str, "00", "00")
                # print(date_time_str)
                date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")

                diff = hour - last_hour
                if diff < 0:
                    diff = diff + 24

                if diff != 1:
                    print(diff, last_hour, dt_obj)

                # print(quarter_activities)

                for h in range(0, diff):
                    for k in range(0, 60, 15):
                        quarter_activity = quarter_activities[int(k / 15)]
                        date_time_obj_plus = date_time_obj + timedelta(hours=h, minutes=k)
                        quarters.append(date_time_obj_plus)
                        activity_sum.append(quarter_activity)

                last_hour_activity = []
                last_hour = hour

            if last_date != date:

                # print(user_dict)

                # print(quarters)
                print(len(quarters), last_date)
                if (len(quarters) != 52):
                    for x in quarters:
                        print(x)

                user_activity_list.append((last_date, sum(activity_sum)))

                '''
                #plt.plot([], [])
                plt.title(str(last_date) + "({})".format(last_date.weekday()))
                plt.plot(quarters, activity_sum)
    
                # beautify the x-labels
                plt.gcf().autofmt_xdate()
                myFmt = mdates.DateFormatter('%H:%M')
                plt.gca().xaxis.set_major_formatter(myFmt)
    
                plt.show()
                '''
                quarters = []
                activity_sum = []

                last_date = date

            i += 1
            last_dt_obj = dt_obj

        print(username)
        print(user_activity_list)

        with open('{}/compiled_{}_{}.csv'.format(audio_or_activity, audio_or_activity, username), 'w') as out:
            csv_out = csv.writer(out)
            for row in user_activity_list:
                csv_out.writerow([i for i in row])


        user_data.append(user_activity_list)

    return user_data


def calculate_relative_graphs (user_data, users):
    mean_data = []
    stdev_data = []

    relative_compare = []
    for user in user_data:
        relative_compare.append([])


    start_date = datetime(2013, 3, 28).date()
    end_date = datetime(2013,5,26).date()


    current_date = start_date
    while current_date <= end_date:
        values = []
        for useridx in range(len(user_data)):
            user_list = user_data[useridx]
            dates_list = [x for x, y in user_list]
            values_list = [y for x, y in user_list]

            #print(dates_list)
            #print(current_date)
            #print(current_date in dates_list)
            if current_date in dates_list:
                index = dates_list.index(current_date)
                values.append( values_list[index] )

        mean_data.append((current_date, sum(values)/len(values)))
        stdev_data.append((current_date , statistics.pstdev(values)))

        for useridx in range(len(user_data)):
            user_list = user_data[useridx]
            dates_list = [ x for x,y in user_list]
            values_list = [ y for x,y in user_list]
            if current_date in dates_list:
                index = dates_list.index(current_date)
                value = values_list[index]
                if value < mean_data[-1][1] + stdev_data[-1][1] and value > mean_data[-1][1] - stdev_data[-1][1]:
                    relative_compare[useridx].append((current_date , 0))
                else:
                    relative_compare[useridx].append((current_date , 1))

        current_date = current_date + timedelta(hours =24)

    print(mean_data)
    print(stdev_data)

    for useridx in range(len(relative_compare)):

        compare_dates = [x for x,y in relative_compare[useridx]]
        compare_values = [y for x, y in relative_compare[useridx]]
        user_dates = [x for x, y in user_data[useridx]]
        user_values= [y for x,y in user_data[useridx]]


        plt.bar(user_dates, user_values, color= "red")
        plt.bar(compare_dates, compare_values, compare_values, color="blue")

        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%M-%D')
        plt.gca().xaxis.set_major_formatter(myFmt)

        plt.title("user-{}-{}".format(users[useridx], type), fontsize=10)
        plt.show()


def compare_self(user_data, users):
    spreads = {}
    for useridx in range(len(user_data)):
        user_list = user_data[useridx]
        user = users[useridx]
        dates_list = [x for x, y in user_list]
        values_list = [y for x, y in user_list]

        maximum = max(values_list)

        normalised = [x/maximum for x in values_list]

        stdev = statistics.pstdev(normalised)
        variance = stdev * stdev

        spreads[user] = variance

    users = spreads.keys()
    spreads = spreads.values()

    plt.bar(users, spreads, color="green" )
    plt.title("spreads")
    plt.show()


def load_compiled_data (audio_or_activity):
    user_data = []
    users = []

    for user in range (61):
        username  = str (user)
        if int(user/10) == 0:
            username = "0"+username

        #print(username)
        try:
            file_name  = '{}/compiled_{}_{}.csv'.format(audio_or_activity, audio_or_activity, username)
            print(file_name)
            csv_activity = open(file_name, mode='r')
        except Exception as e :
            print(e)
            continue
        csv_activity_reader = csv.DictReader(csv_activity)

        users.append(username)
        user_activity = []

        for row in csv_activity_reader:
            #dartmouth_timezone = 'America/New_York'
            #NY = pytz.timezone(dartmouth_timezone)
            dt_obj = datetime.strptime(str(list(row.values())[0]), "%Y-%m-%d")

            activity = float(list(row.values())[1])

            user_activity.append( (dt_obj.date(), activity) )

        #print(user_activity)
        user_data.append(user_activity)
    return user_data, users


type = "activity"

#user_data = clean_data_rewrite( type )
user_data, users = load_compiled_data(type)
calculate_relative_graphs(user_data, users)
#compare_self( user_data, users )














