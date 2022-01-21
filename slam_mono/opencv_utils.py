
import cv2
import numpy as np
import matplotlib.pyplot as plt


class Video(object):
    # Opens a video stream
    def __init__(self, filename, starting_frame=0):
        self.video_capture = cv2.VideoCapture(filename)
        # get video parameters
        self.fps = round(self.video_capture.get(cv2.CAP_PROP_FPS))
        self.W = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.H = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # playback options
        self.frame = None
        self.frame_count = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        print('frame_count:', self.frame_count)
        print('starting_frame:', starting_frame)
        self.current_frame = starting_frame
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)
        print('fps:', self.fps)
        print(f'resolution: ({self.W}, {self.H})')

    #------------------------------------------------------------------------------------
    def is_running(self):
        return self.video_capture.isOpened()
    
    #------------------------------------------------------------------------------------
    def get_resolution(self):
        return (self.W, self.H)

    #------------------------------------------------------------------------------------
    def set_resolution(self, W, H):
        self.W, self.H = int(W), int(H)
        print(self.W, self.H)
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.W)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.H)

    #------------------------------------------------------------------------------------
    def release(self):
        self.video_capture.release()

    #------------------------------------------------------------------------------------
    def get_next_frame(self):
        # returns a frame in a format that SDL can handle
        ret, self.frame = self.video_capture.read()
        
        # loop video
        self.current_frame += 1
        if self.current_frame == self.frame_count:
            self.current_frame = 0
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        self.frame = cv2.resize(src=self.frame,
                                dsize=(self.W, self.H), 
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

