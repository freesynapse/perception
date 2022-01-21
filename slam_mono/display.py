
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"        
import pygame
import numpy as np
import cv2



class Display2D(object):
    def __init__(self, W, H, fps_cap, win_pos=(0, 0)):
        # position the window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos[0], 
                                                        win_pos[1])
        self.W, self.H = int(W), int(H)
        pygame.init()
        self.screen = pygame.display.set_mode((self.W, self.H), pygame.DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()
        self.is_running_ = True
        
        
        self.target_fps = fps_cap
        self.fps = 30.0
        self.frame_count = 0
        self.frame_time = 1000.0 / float(self.target_fps)
        
    #------------------------------------------------------------------------------------
    def render(self, frame):
        
        # TODO : remove this assertion
        if frame[:,:,0].shape != (self.W, self.H):
            frame_ = cv2.resize(frame, (self.W, self.H))
        else:
            frame_ = frame
        
        for event in pygame.event.get():
            if event == pygame.QUIT:
                self.is_running_ = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running_ = False
                elif event.key == pygame.K_SPACE:
                    self.pause_()
        
        frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2RGB)
        pygame.surfarray.blit_array(self.surface, frame_.swapaxes(0, 1)[:, :, [0, 1, 2]])
        self.screen.blit(self.surface, (0, 0))
        
        pygame.display.flip()
                
    #------------------------------------------------------------------------------------
    def pause_(self):
        while (1):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    elif event.key == pygame.K_ESCAPE:
                        self.is_running_ = False
                        return
            pygame.time.wait(33)

    #------------------------------------------------------------------------------------
    def is_running(self):
        return self.is_running_