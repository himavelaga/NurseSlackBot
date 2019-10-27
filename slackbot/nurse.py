import pymysql.cursors
import sys


# Connect to the database
connection = pymysql.connect(host='52.70.223.35',
                             user='clinicuser',
                             password='sparky19',
                             db='ClinicDB',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


#retreive and store arguments
lastName = sys.argv[1]
month = sys.argv[2]
date = sys.argv[3]

#convert month name to number
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augu\
st', 'September', 'October', 'November', 'December']
monthNo = months.index(month) + 1
monthNo = 04

day = "2019-" + str(monthNo) + "-" + date

try:
   with connection.cursor() as cursor:
      # Read a single record
      sql = "SELECT `id` FROM nurses WHERE `LastName`= %s"
      cursor.execute(sql, (lastName,))
      if cursor.rowcount > 0 :
         result = cursor.fetchone()
         nurseID = result.get("id")
         sql2 = "SELECT `SlotStart` FROM `nurse_schedule` WHERE `NurseID`= %s AND `SlotDate` = %s"
         cursor.execute(sql2,(nurseID, day))
         result = cursor.fetchall()
         if cursor.rowcount > 0 :
            for row in result:
               print row["SlotStart"]
         else:
            print "No times available on specified day for Nurse " + lastName 
      else:
         print "Sorry, but we don't have a Nurse " + lastName + " in this office. Make sure to look up your nurse by last name!"
finally:
   connection.close()
