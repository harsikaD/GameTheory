import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import copy
import pytz

type = "phonelock"

users = []
users_dark_data = []
for i in range (60):
    username  = str (i)
    if int(i/10) == 0:
        username = "0"+username


    #print(username)
    try:
        file_name  = '/Users/Priya/Desktop/IITK/Game Theory/dataset/sensing/conversation/conversation_u{}.csv'.format(type, type, username)
        print(file_name)
        csv_activity = open(file_name, mode='r')
    except Exception as e :
        print(e)
        continue


    user_dark_data = []
    csv_activity_reader = csv.DictReader(csv_activity)

    last_dt2 = None
    for row in csv_activity_reader:

        dt_obj1 = datetime.fromtimestamp(int(list(row.values())[0]))  # row['timestamp']))
        dt_obj2 = datetime.fromtimestamp(int(list(row.values())[1]))

        #print(dt_obj2, dt_obj1, dt_obj2 - dt_obj1)
        #print(dt_obj1.hour)
        if dt_obj1.hour >= 10 and dt_obj2.hour <= 21 and dt_obj1.date() == dt_obj2.date():

            if last_dt2 is None:
                #print("changed from None", dt_obj2)
                last_dt2 = dt_obj2

            diff = dt_obj2 - dt_obj1
            #print(last_dt2)
            #print(dt_obj2, dt_obj1, diff)
            secs = diff.days*(24*60*60)  + diff.seconds
            hours = float(secs)/(3600.0)

            if dt_obj1 > last_dt2 and dt_obj1.date() == last_dt2.date() :
                #print("added")
                updated_hours = user_dark_data[-1][1] + hours
                user_dark_data[-1] = (dt_obj1.date(), updated_hours)
                #print(user_dark_data[-1])
            else:
                #print("appended")
                missed_diff = dt_obj1.date() - last_dt2.date()
                #print(missed_diff)

                if (missed_diff.days > 1 ):
                    for i in range(missed_diff.days -1 ):
                        user_dark_data.append((last_dt2.date() + timedelta(hours = 24*(i+1)), 0))
                user_dark_data.append((dt_obj1.date(), hours))
                #print(user_dark_data[-1])

            last_dt2 = dt_obj2

    #print(user_dark_data)
    #print(len(user_dark_data))
    if (len(user_dark_data) == 0):
        start_date = datetime(2013, 3, 28).date()
        for j in range(60):
            user_dark_data.append(( start_date + timedelta(hours=24*j) ,0))

    for dark_data in user_dark_data:
        print(dark_data[0], dark_data[1] )
    users.append(username)
    users_dark_data.append( user_dark_data )
    with open('{}/compiled_{}_{}.csv'.format(type, type, username), 'w') as out:
        csv_out = csv.writer(out)
        for row in user_dark_data:
            csv_out.writerow([i for i in row])

