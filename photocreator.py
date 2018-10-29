
import glob
import psycopg2
import face_recognition
import cv2
import requests
import cv2
import os

connection = psycopg2.connect(user = "dpcwdmmygwvxqe",
                                  password = "d113638b455977377844724fea4f9e7aac7ff8dbc4685516ecbdd25d5b52a39b",
                                  host = "ec2-54-246-86-167.eu-west-1.compute.amazonaws.com",
                                  port = "5432",
                                  database = "darsad67es2t64")
cursor = connection.cursor()
sql= "SELECT id FROM people"
cursor.execute(sql)
r = cursor.fetchall()
count = (len(r)+1)

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = input('\n enter name ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count

while(True):

    ret, img = cam.read()
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     

        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/" + str(face_id) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)

        #query = "UPDATE people SET status = 'yes' WHERE name = '" + str(rec) + "'"
		

        cursor.execute("INSERT INTO people (id, name, status, photo, count) VALUES (%s, %s, %s, %s, %s);", (count, face_id, 'no', 'photo', 0))

        connection.commit()

        
    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 1: # Take 30 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
cursor.close()

