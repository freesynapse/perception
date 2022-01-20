
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Video(object):
    # Opens a video stream
    def __init__(self, filename, width, height, starting_frame=0):
        self.width = width
        self.height = height        
        self.video_capture = cv2.VideoCapture(filename)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.fps = round(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.frame = None
        self.frame_count = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print('frame_count:', self.frame_count)
        print('starting_frame:', starting_frame)
        self.current_frame = starting_frame
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)
        print('fps:', self.fps)
    #------------------------------------------------------------------------------------
    def get_next_frame(self):
        # returns a frame in a format that SDL can handle
        ret, self.frame = self.video_capture.read()
        
        # loop video
        self.current_frame += 1
        if self.current_frame == self.frame_count:
            self.current_frame = 0
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
        self.frame = cv2.resize(self.frame,
                                (self.width, self.height), 
                                interpolation=cv2.INTER_AREA)
            
        return ret, self.frame
        # self.add_alpha_to_frame()
    #------------------------------------------------------------------------------------
    def add_alpha_to_frame(self, frame):
        self.frame = np.insert(frame, 3, 255, axis=2)
        return self.frame
    #------------------------------------------------------------------------------------
    def save_current_frame(self, filename):
        cv2.imwrite(filename, self.image)

