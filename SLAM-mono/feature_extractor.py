
import cv2
import numpy as np
from queue import Queue


class FeatureExtractor(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.orb = cv2.ORB_create()
        # TODO : replace with self.last_frame?
        self.frames = Queue(maxsize=20)
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
    def process_frame(self, frame):
        """
        Returns the extracted keypoints of a frame.
        """
        # TODO : remove this assertion
        if frame[:,:,0].shape != (self.width, self.height):
            frame_ = cv2.resize(frame, (self.width, self.height))
        else:
            frame_ = frame
        
        if self.frames.full():
            self.frames.get()
        self.frames.put(frame_)
        
        #kps, des = self.orb.detectAndCompute(frame_, None)
        pts = cv2.goodFeaturesToTrack(np.mean(frame_, axis=2).astype(np.uint8), 
                                      maxCorners=3000,
                                      qualityLevel=0.1,
                                      minDistance=5)
        kps = [cv2.KeyPoint(x=p[0][0], y=p[0][1], _size=20) for p in pts]
        kps, des = self.orb.compute(frame_, kps)

        return kps, des, frame_
    
    def match_frames(self, f0, f1):
        """
        Find matching keypoints between frames to track.
        """
        pass        

