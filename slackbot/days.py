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
firstName = sys.argv[1]
lastName = sys.argv[2]

try:
   with connection.cursor() as cursor:
      # Read a single record
      sql = "SELECT `id` FROM nurses WHERE `FirstName`= %s AND`LastName`= %s"
      cursor.execute(sql, (firstName,lastName))
      if cursor.rowcount > 0 :
         result = cursor.fetchone()
         nurseID = result.get("id")
         sql2 = "SELECT `SlotDate` FROM `nurse_schedule` WHERE `NurseID`= %s"
         cursor.execute(sql2,(nurseID,))
         result = cursor.fetchall()
         if cursor.rowcount > 0 :
            for row in result:
               print row["SlotDate"]
         else:
            print "No dates currently available for Nurse " + lastName
      else:
         print "Sorry, but we don't have a Nurse " + lastName + " in this office."
finally:
   connection.close()
