
import numpy as np
import cv2
import os
from tqdm import tqdm

def assemble_mp4_from_frames(dirname):
    images = [img for img in os.listdir(dirname) if img.endswith('.png')]
    images.sort()
    print(f'found {len(images)} images, creating video stream')
    frame = cv2.imread(os.path.join(dirname, images[0]))
    h, w, c = frame.shape
    print(w, h, c)
    
    video = cv2.VideoWriter(os.path.join(dirname, 'fake_slam.mp4'), 
                            apiPreference=0,
                            fourcc=cv2.VideoWriter_fourcc(*'XVID'),
                            fps=30,
                            frameSize=(w, h))
    
    
    for img in tqdm(images):
        video.write(cv2.imread(os.path.join(dirname, img)))
        
    cv2.destroyAllWindows()
    video.release()