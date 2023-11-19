import logging
from time import sleep

import cv2
import mediapipe as mp #type: ignore
import datetime, time
import sys
from .notifications import send_alert
from database.data import data_commands as Data
from .notifications import send_alert



class Feed():
    """
    All functions related to camera functionality 
    """
    def __init__(self):
        """
        Parameters:
                data: Calls the data functions class to let me grab data saved in my database
                mp_face_detection: mediapipes face detection
                mp_drawing: mediapipes box drawing (not in use just there if i choose to do something with it)
                cam (int): webcam port number for opencv
                detection (bool): checking if a face is detected while webcam is running
                record_delay(int): the delay before livefeed has the ability to start recording (to try to combat instant recording so it doesnt alert if the person that turned the webcam is leaving view of the camera)
                
        """
        
        self.data = Data()
        
        self.face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")
        
        self.mp_face_detection = mp.solutions.face_detection    
        self.mp_drawing = mp.solutions.drawing_utils
        self.cam = self.find_cam()
        print(self.cam) #? test
        self.detection = False
    
    # if a cam isnt found return false so that livefeed cant take place      
    def find_cam(self):
        """
        goes through a reasonable amount of ports in a computer and checks if any of them can produce a video frame, if no luck returns false so that get_livefeed can exit safely
        
        """
        try:
            for i in range (10):
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if frame is not None:
                        cap.release()
                        return int(i)
                    cap.release() 
            return False
        except cv2.error as e:
            logging.error(f"An error has occured when trying to get webcam: {str(e)}")
        
    
    
    def get_livefeed(self):
        """
        Starts the recording processs and if a face is detected calls the start recording function
        """
        #! may not be needed self.detection=False
        
        #set delay before webcam can start to record
        #time.sleep(self.data.get_delay()) #! add this back when testing is done
        
        self.cap = cv2.VideoCapture(self.cam)
        if not (0 <= self.cam <= 10):
            print("Webcam not found")
            sys.exit()
        
        
        
        while self.cap.isOpened():
            _, self.image = self.cap.read()
            
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            self.bodies = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if not _:
                print("empty frame")
                continue
    
            if len(self.faces) + len(self.bodies) > 0:
                time.sleep(2)
                if len(self.faces) + len(self.bodies) > 0:
                    self.start_recording()
            
                        
    def start_recording(self):
        """
        Starts recording whenever a face is detected and when stopped saves the video into the given savepath
            
            Variables:
                    video_savepath (str): Where the file is to be saved
                    no_detection_time (bool/int): time that a face isnt detected
                    maxtime_without_detection (int): the maximum amount of time in seconds that a face can be undetedcted before the function ends
                    
        """
        
        
        
        send_alert()
        print("alert sent")
        video_savepath = self.data.get_video_save_path() 
        timer_started = False
        no_detection_time = None
        maxtime_without_detection = 5
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        frame_rate = 20
        out = None
        
        while True:
            if len(self.faces) + len(self.bodies) > 0:
                if self.detection:
                    timer_started = False
                else:
                    self.detection = True
                    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
                    out = cv2.VideoWriter(f'{video_savepath}/{timestamp}.mp4', fourcc, frame_rate, frame_size)
                    print("recording...")
            elif self.detection:
                if timer_started:
                    if time.time() - no_detection_time >= maxtime_without_detection:
                        self.detection = False
                        timer_started= False
                        print("stopping recording...")
                        out.release()
                        return
                else:
                    timer_started = True
                    no_detection_time = time.time()        
            if self.detection:
               out.write(self.image)
            
            
                
             
            
            

        
        
        """while True:
            if self.results.detections:
                if self.detection:
                    timer_started = False
                else:
                    self.detection = True
                    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
                    out = cv2.VideoWriter(f'{video_savepath}/{timestamp}.mp4', fourcc, frame_rate, frame_size) #! needs testing: make sure it saves in the proper filepath
                    #out.write(self.image)
                    print("recording...")
            elif self.detection:
                if timer_started:
                    if time.time() - no_detection_time >= maxtime_without_detection:
                        self.detection = False
                        timer_started = False
                        out.release()
                        print("recording stopped")
                        break
                else: timer_started = True
                no_detection_time = time.time()
            
        out.write(self.image)
        return"""
                
        
        
        
    def stop_feed(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.out is not None:
            self.out.release()
            self.out = None
            
            
            
