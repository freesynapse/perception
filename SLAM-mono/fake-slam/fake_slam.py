#!/usr/bin/python3

from fake_slam_scene import FakeSLAMScene
from assemble_mp4 import assemble_mp4_from_frames


if __name__ == '__main__':
    
    WIN_WIDTH, WIN_HEIGHT = 940, 540
    #WIN_WIDTH, WIN_HEIGHT = 20, 10
    #scene = FakeSLAMScene((WIN_WIDTH, WIN_HEIGHT))
    #scene.run()
    
    assemble_mp4_from_frames('../../_RESOURCES/fake-SLAM/')
    
    exit(0)
