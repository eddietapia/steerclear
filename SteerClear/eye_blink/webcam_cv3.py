import cv2
from twilio.rest import Client
import json
import sys
import io
import random
from PIL import Image
import logging as log
import datetime as dt
from emotion import detectEmotion 
from time import sleep
#from analyze import is_celebrity

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

# Twilio account and token
account_sid = 'ACeac27a33a1be3b756861ddaa85947de2'
auth_token = '5ab180dea9ae21caee01c6e47869575f'

def get_emotion(emotions):
    """
    Finds the emotion that has the max score
    :param emotions: dictionary that contains the emotions
    and their scores
    :return maxEmotion: the emotion that has the highest match
    """
    maxScore = 0
    maxEmotion = None
    # Loop through the emotions to find the highest match
    for key in emotions.keys():
        if (maxScore < emotions[key]):
            maxScore = emotions[key]
            maxEmotion = key
    return maxEmotion


def send_text(emotion):
    """
    Will send the user a text message depending on their emotion
    :param emotion: the emotion that was detected in the current frame
    :return: None
    """
    # Create the messages that we will send
    happy = ["Nice to see you smiling! Don't get used to it. Life is full of dissapointments",
    "Whoah! You scared me! Don't ever smile again", 
    "Are you happy because you almost broke my mirror with your smile?",
    "Idk why you're so happy, you look horrible..." ]
    sad = ["Why so sad? Wanna hear a joke? What did Jay-Z call his gf before they got married?...   Feyonce!!!"
    "You know what's more sad? I got caught taking a pee in the swimming pool. The lifeguard yelled at me \
    so loud, I nearly fell in.", "Idk why you're so sad. You're not completely useless, you can always serve as a bad example.",
    "I know something that will cheer you up. What's green, fuzzy, and if it fell out of a tree it would kill you?.. A pool table."]
    anger = ["Whoah! Calm down Hulk. You don't scare anyone :P", "You look even worse when you're angry.", 
    "Eat a snickers. You're not you when you're hangry", 
    "Chill. I'm the one who should be angry at you. Do you know how scary it is to look at you in the morning?"]
    surprise = ["I told my friend she was drawing her eyebrows too high. She looked surprised.",
    "Surprise surprise! It's me!", "Don't be so surprised. I always look this flawless...",
    "I know you're not really surprised by my talents. You're just exaggerating. Typical human..."]
    
    index = random.randrange(0,4)

    # The numbers that we will use to send/receive SMS 
    to_num = '+18184817822'
    from_num = '+18184234513'
    # Establish the Twilio client 
    client = Client(account_sid, auth_token)
    if emotion != 'neutral':
        if emotion == 'happiness':
            message = client.messages.create(to= to_num, from_= from_num, body=(happy[index]))
        elif emotion == 'sadness':
            message = client.messages.create(to= to_num, from_= from_num, body=(sad[index]))
        elif emotion == 'anger':
            message = client.messages.create(to= to_num, from_= from_num, body=(anger[index]))
        elif emotion == 'surprise':
            message = client.messages.create(to= to_num, from_= from_num, body=(surprise[index]))
        else:
            message = client.messages.create(to= to_num, from_= from_num, body=("I see you're feeling some form of", emotion))


# Open the camera so we can capture video and image sequences
video_capture = cv2.VideoCapture(0)
anterior = 0
counter = 0

while True:
    # Check if the video camera was opened succesfully
    if not video_capture.isOpened():
        print('Unable to load camera. Will attempt to load in 5 seconds')
        sleep(5)
        video_capture = cv2.VideoCapture(0)
        continue

    # Capture frame-by-frame
    ret, frame = video_capture.read()
    # The counter resets to 0 every 90 seconds
    if (counter == 0):
	# Grab the image from the frames we read and save it
        image = Image.fromarray(frame)
        image.save('file.jpg')
        with open('file.jpg', mode='rb') as file: # b is important -> binary
            fileContent = file.read()
        #print is_celebrity(fileContent)
        # Use Microsoft Emotion API to detect the emotions in the frame
        faceEmotions = json.loads(detectEmotion(fileContent))
        for face in faceEmotions:
            emotion = get_emotion(face['scores'])
            face_position = face['faceRectangle']
            #print "Face at:", face_position['height'], face_position['left'], face_position['top'], \
            #    face_position['width'], "Emotion:", emotion
            print "Emotion", emotion
            # Send the text message to the user
            #send_text(emotion)            
            
        # Use opencv to detect the faces in the frames
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        if anterior != len(faces):
            anterior = len(faces)
            log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))
    
    elif (counter == 30):
        counter = -1   
    
    counter = counter + 1
    
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
