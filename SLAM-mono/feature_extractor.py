
import cv2
import numpy as np
from queue import Queue


class FeatureExtractor(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.orb = cv2.ORB_create()
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
        self.this_frame = None
        self.last_frame = None
        
    def process_frame(self, frame):
        """
        Returns the extracted keypoints of a frame.
        """
        self.last_frame = self.this_frame
        
        # TODO : remove this assertion?
        if frame[:,:,0].shape != (self.width, self.height):
            frame_ = cv2.resize(frame, (self.width, self.height))
        else:
            frame_ = frame
        
        #kps, des = self.orb.detectAndCompute(frame_, None)
        pts = cv2.goodFeaturesToTrack(np.mean(frame_, axis=2).astype(np.uint8), 
                                      maxCorners=3000,
                                      qualityLevel=0.1,
                                      minDistance=5)
        kps = [cv2.KeyPoint(x=p[0][0], y=p[0][1], _size=20) for p in pts]
        kps, des = self.orb.compute(frame_, kps)

        self.this_frame = { 'des': des, 'kps': kps }

        return kps, des
    
    def match_frames(self):
        """
        Find matching keypoints between frames to track using 
        ORB feature descriptors.
        """
        if self.last_frame is not None:
            
            # match ORB descriptors between frames
            matches = self.BFMatcher.knnMatch(self.this_frame['des'], self.last_frame['des'], k=2)
            
            matched_pts = []
            idx0, idx1 = [], []
            
            # Lowe's ratio test for knn matching
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    p0 = self.this_frame['kps'][m.queryIdx]
                    p1 = self.last_frame['kps'][m.trainIdx]
                    if m.queryIdx not in idx0 and m.trainIdx not in idx1:
                        idx0.append(m.queryIdx)
                        idx1.append(m.trainIdx)
                        matched_pts.append((p0, p1))
            
            return matched_pts
        

