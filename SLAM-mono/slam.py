#!/usr/bin/python3

from nis import match
import cv2
import numpy as np

from opencv_utils import Video
from feature_extractor import FeatureExtractor
from display import Display2D
from timer import Timer


if __name__ == '__main__':
    render_size = 960, 540
    cap_size = 480, 270
    
    #filename = '../_resources/fake-SLAM/fake_slam.mp4'
    filename = '../_resources/driving0.mp4'
    
    video = Video(filename, *cap_size)
    print(video)
    
    extractor = FeatureExtractor(*cap_size)
    display = Display2D(*render_size, video.fps)
    
    while (video.is_running() and display.is_running()):
        timer = Timer(False)

        ret, frame = video.get_next_frame()

        if ret:
            kps, des = extractor.process_frame(frame)
            matched_pts = extractor.match_frames()
            if matched_pts is not None:
                for pt0, pt1 in matched_pts:
                    u0, v0 = int(pt0.pt[0]), int(pt0.pt[1])
                    u1, v1 = int(pt1.pt[0]), int(pt1.pt[1])
                    cv2.circle(img=frame, center=(u0, v0), radius=3, color=(0, 255, 0))
                    cv2.line(img=frame, pt1=(u0, v0), pt2=(u1, v1), color=(255, 0, 0))

            # blit to SDL surface
            display.render(frame)

        else:
            break
        
        timer.get()
    
    video.release()
    
    