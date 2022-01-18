#!/usr/bin/python3

import cv2
import numpy as np

from opencv_utils import Video
from feature_extractor import FeatureExtractor
from display import Display2D
from timer import Timer


if __name__ == '__main__':
    render_size = 960, 540
    cap_size = 480, 270
    
    #filename = '../_RESOURCES/fake-SLAM/fake_slam.mp4'
    filename = '../_RESOURCES/driving0.mp4'
    
    video = Video(filename, *cap_size)
    
    extractor = FeatureExtractor(*cap_size)
    display = Display2D(*render_size, video.fps)
    
    while (video.is_running() and display.is_running()):
        timer = Timer()
                
        ret, frame = video.get_next_frame()
        if ret:
            kps, des, frame_ = extractor.process_frame(frame)
            print(len(kps))
            for kp in kps:
                cv2.circle(img=frame_, center=(int(kp.pt[0]), int(kp.pt[1])), radius=6, color=(0, 255, 0))
            frame = cv2.resize(frame_, render_size)

            display.render(frame)

        else:
            break
        
        timer.get()
    
    video.release()
    
    