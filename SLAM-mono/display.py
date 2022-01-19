
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"        
import pygame
import numpy as np
import cv2


class Display2D(object):
    def __init__(self, W, H, fps_cap):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H), pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.is_running_ = True
        
        self.width, self.height = W, H
        
        self.target_fps = fps_cap
        self.fps = 30.0
        self.frame_count = 0
        self.frame_time = 1000.0 / float(self.target_fps)
        
    #------------------------------------------------------------------------------------
    def render(self, frame):
        
        # TODO : remove this assertion
        if frame[:,:,0].shape != (self.width, self.height):
            frame_ = cv2.resize(frame, (self.width, self.height))
        else:
            frame_ = frame
        
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.is_running_ = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running_ = False
        
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        pygame.surfarray.blit_array(self.surface, frame_.swapaxes(0, 1)[:, :, [0, 1, 2]])
        self.screen.blit(self.surface, (0, 0))
        
        pygame.display.flip()
                
    #------------------------------------------------------------------------------------
    def is_running(self):
        return self.is_running_