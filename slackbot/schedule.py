import pymysql.cursors
import sys

# Connect to the database
connection = pymysql.connect(host='52.70.223.35',
                             user='clinicuser',
                             password='sparky19',
                             db='ClinicDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
#retrieve and store arguments
time = sys.argv[1] #time 
meridian =  sys.argv[2] #am or pm
month = sys.argv[3]
date = sys.argv[4]

#convert month name to number
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
monthNo = months.index(month) + 1

#convert time to military time
time = int(time)
if (meridian == "pm" and time >= 1 and time < 12) or (meridian == "am" and time == 12):
   time = 12 + time

#start database query if time is within 9am-5pm range
if (meridian== "am" and time >= 9 and time <=11 ) or (meridian == "pm" and time >= 12 and time <= 16) :
   time = str(time)
   time = time + ":00:00"
   day = "2019-" + str(monthNo) + "-" + date

   try:
       with connection.cursor() as cursor:
           # Read a single record
           sql = "SELECT `NurseID` FROM nurse_schedule WHERE `SlotDate`= %s AND `SlotStart`= %s"
           cursor.execute(sql, (day,time))
           if cursor.rowcount > 0:
              result = cursor.fetchall()
              nurseID = result[0].get("NurseID")
              sql2 = "SELECT `FirstName`, `LastName` FROM `nurses` WHERE `id`= %s"
              cursor.execute(sql2,(nurseID,))
              result = cursor.fetchone()
              print result.get("FirstName") + " " + result.get("LastName")
           else: 
              print "No one is available at the specified date and time"
   finally:
      connection.close()
else:
   print "Sorry, the clinic is only open from 9am-5pm Mon-Fri."
