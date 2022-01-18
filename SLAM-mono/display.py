

import pygame
import numpy as np


class Display2D(object):
    def __init__(self, W, H, fps_cap):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H), pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.is_running_ = True
        
        self.target_fps = fps_cap
        self.fps = 0.0
        self.frame_count = 0
        self.frame_time = 1000.0 / float(self.target_fps)
        
    #------------------------------------------------------------------------------------
    def render(self, frame):
        t0 = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.is_running_ = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running_ = False
        
        pygame.surfarray.blit_array(self.surface, frame.swapaxes(0, 1)[:, :, [0, 1, 2]])
        self.screen.blit(self.surface, (0, 0))
        
        pygame.display.flip()
        
        # set fps
        t1 = pygame.time.get_ticks()
        sleep_time = int(self.frame_time - (t1 - t0))
        #if sleep_time > 0: pygame.time.wait(sleep_time)
        t2 = pygame.time.get_ticks()
        self.fps = (1000.0 / (t2 - t0))
        self.frame_count += 1
        
        if self.frame_count % int(self.target_fps) == 0:
            print(self.fps)
        
    #------------------------------------------------------------------------------------
    def is_running(self):
        return self.is_running_