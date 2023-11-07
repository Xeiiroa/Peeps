import logging
from time import sleep

import cv2
import mediapipe as mp
import datetime, time
import sys
from .notifications import send_alert
from database.data import data_commands as Data

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
        
        #! may need self
        self.data = Data()
        self.mp_face_detection = mp.solutions.face_detection(model_selection=1, min_detection_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.cam = self.find_cam()
        self.face_detection = self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.detection = False
        self.get_livefeed()
        self.record_delay= self.data.get_delay()
    
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
                        return int(i) 
            return False
        except cv2.error as e:
            logging.error(f"An error has occured when trying to get webcam: {str(e)}")
        
    
    
    def get_livefeed(self):
        """
        Starts the recording processs and if a face is detected calls the start recording function
        """
        self.detection=False
        
        #set delay before webcam can start to record
        time.sleep(self.data.get_delay()) 
        
        self.cap = cv2.VideoCapture(self.cam)
        if self.cam == False:
            print("No webcam Found")
            sys.exit()
        
        with self.mp_face_detection:
            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("empty frame")
                    continue
        
                #saying not to draw boxes
                image.flags.writeable=False #?
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                #making detections
                results = self.face_detection.process(image)
                
                #if a face is detected start recording
                #! has a risk of causing an infinite loop in the case that the conditional can repeat itself
                if results.detections:
                    time.sleep(2)
                    if results.detections:
                        self.start_recording(results, image)
                        
    def start_recording(self, results, image):
        """
        Starts recording whenever a face is detected and when stopped saves the video into the given savepath
            
            Variables:
                    video_savepath (str): Where the file is to be saved
                    no_detection_time (bool/int): time that a face isnt detected
                    maxtime_without_detection (int): the maximum amount of time in seconds that a face can be undetedcted before the function ends
                    
        """
        video_savepath = ...
        timer_started = False
        no_detection_time = None
        maxtime_without_detection = 5
        
        fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        frame_rate = 20
        
        #?self.cap isnt imported into the function so there may be a need to change it if it doesnt upload
        while self.cap.isOpened():
            if results.detections:
                if self.detection:
                    timer_started = False 
                else:
                    self.detection = True
                    timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")
                    self.out = cv2.VideoWriter(f'{video_savepath}/{timestamp}.mp4', fourcc, frame_rate, frame_size) #! needs testing: make sure it saves in the proper filepath
            elif self.detection:
                if timer_started:
                    if time.time() - no_detection_time >= maxtime_without_detection:
                        detection = False
                        timer_started = False
                        break
                else:
                    timer_started= True
                    no_detection_time = time.time()
            if self.detection:
                self.out.write(image)    
                
        self.out.release()
        return
    
    def stop_feed(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.out is not None:
            self.out.release()
            self.out = None
            
            
            
