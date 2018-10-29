import glob
import psycopg2
import face_recognition
import cv2
import requests
import time


video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
known_face_names_pre = glob.glob('dataset/*.jpg')
known_image = []
known_face_encodings = []
known_face_names = []
for i in range(len(known_face_names_pre)):
    image_for_append = face_recognition.load_image_file(known_face_names_pre[i])
    known_image.append(image_for_append)
    known_face_encodings.append(face_recognition.face_encodings(image_for_append)[0])
    known_face_names.append(known_face_names_pre[i][8:-4])

	
connection = psycopg2.connect(user = "dpcwdmmygwvxqe",
                                  password = "d113638b455977377844724fea4f9e7aac7ff8dbc4685516ecbdd25d5b52a39b",
                                  host = "ec2-54-246-86-167.eu-west-1.compute.amazonaws.com",
                                  port = "5432",
                                  database = "darsad67es2t64")
cursor = connection.cursor()    
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


count = 0
while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"#; 
            
			
			
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame
    

	
    if len(face_names) > 0:
        rec = face_names[0]
        #print(type(face_names[0][8:-4]))
        query = "UPDATE people SET status = 'yes' WHERE name = '" + str(rec) + "'"
		
        cursor.execute(query)
        connection.commit()

        #req = requests.request('GET', 'https://facevision27.herokuapp.com/refresh')

    for (top, right, bottom, left), name in zip(face_locations, face_names):

        if name == "Unknown":
            time.sleep(5)
            count += 1
            print('Не авторизованный пользователь')
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        query_count = "UPDATE people SET count = " + str(count) + " WHERE id = '4' "
		
		
		
        cursor.execute(query_count)
        connection.commit()
		
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        query_count = "'UPDATE people SET count = '" + str(count) + "'WHERE id = 1'"
        cursor.execute(query)
        connection.commit()
		
		
    # Display the resulting image
    cv2.imshow('LifeBug', frame)
    
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
cursor.close()