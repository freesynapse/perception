#!/usr/bin/python3

import cv2
import numpy as np

from opencv_utils import Video
from feature_extractor import FeatureExtractor
from display import Display2D
from timer import Timer


if __name__ == '__main__':
    W, H = 960, 540
    
    # focal length; number of pixels per radian the camera rotates
    f = 270
    # the camera matrix
    K = np.array([[f, 0.0, W/2], [0, f, H/2], [0, 0, 1]])
    
    #filename = '../_resources/fake-SLAM/fake_slam.mp4'
    filename = '../_resources/driving0.mp4'
    
    video = Video(filename, W, H)
    print(video)
    
    fe = FeatureExtractor(K)
    display = Display2D(W, H, video.fps)
    
    while (video.is_running() and display.is_running()):
        timer = Timer(False)

        ret, frame = video.get_next_frame()

        if ret:
            kps, des = fe.process_frame(frame)
            matches = fe.match_frames()
            if matches is not None:
                for pt0, pt1 in matches:
                    u0, v0 = int(pt0[0]), int(pt0[1])
                    u1, v1 = int(pt1[0]), int(pt1[1])
                    cv2.circle(img=frame, center=(u0, v0), radius=3, color=(0, 255, 0))
                    cv2.line(img=frame, pt1=(u0, v0), pt2=(u1, v1), color=(255, 0, 0))

            # blit to SDL surface
            display.render(frame)

        else:
            break
        
        timer.update()


    video.release()
    
    