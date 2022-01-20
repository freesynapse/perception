
from turtle import window_width
import numpy as np
import os
# hide pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"        

import pygame
import pygame.freetype
from pygame.locals import *
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_objects import *
from PIL import Image


# constants
FPS = 30.0
FRAME_TIME = 1000.0 / 30.0


class FakeSLAMScene(object):
    
    #------------------------------------------------------------------------------------
    def __init__(self, window_dim, window_pos=(0, 0)):
        
        # pygame parameters
        self.window_dimensions = window_dim
        self.window_position = window_pos
        self.surface = None
        self.keys = None
        
        # loop variables
        self.is_running = True
        self.fps = None
        self.fpss = []
        self.loop_frame = 0
        self.frame_count = 0
        self.loops_count = 0

        # geometry
        self.objects = []
        self.objects.append(Cube(position=[-2.3, -1.1, -1.1], size=0.7))
        self.objects.append(Cube(position=[ 2.3,  0.0, -3.2], size=0.7))
        self.objects.append(Cube(position=[ 3.4,  0.8, -2.2], size=0.7))
        self.objects.append(Cube(position=[-1.4,  0.1,  1.5], size=0.7))
        
        # rendering
        self.wireframe_mode = False
        self.selected_object = 0
        self.object_selection_mode = False
        self.pixels = None

        # initialize pygame and openGL
        self.setup_openGL_()


    #------------------------------------------------------------------------------------
    def run(self):
        while self.is_running and self.loops_count < 10:
            t0 = pygame.time.get_ticks()
            
            # events including control input
            #self.process_events_()                    
            # fast input
            #self.process_input_()
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            dx = np.sin(self.loop_frame / 100.0 * 2.0 * np.pi)
            if self.loop_frame > 100:
                self.loop_frame = 0
                print(np.mean(np.array(self.fpss)), self.loops_count)
                self.fpss = []
                self.loops_count += 1
            
            ##### BEGIN SCENE #####
            
            for i, object in enumerate(self.objects):
                if self.object_selection_mode:
                    if self.selected_object == i:
                        object.selection_color = np.array([0.0, 0.0, 0.4])
                    else:
                        object.selection_color = np.array([0.0, 0.0, 0.0])
                else:
                    object.selection_color = np.array([0.0, 0.0, 0.0])
                object.render(translation=np.array([dx, 0.0, 0.0]), wireframe=self.wireframe_mode)
            
            ##### END SCENE #####

            self.save_frame(self.frame_count)
            
            pygame.display.flip()
            
            # cap fps to 30ish
            sleep_time = int(FRAME_TIME - (pygame.time.get_ticks() - t0))
            if sleep_time > 0: pygame.time.wait(sleep_time)
            t1 = pygame.time.get_ticks()
            self.fps = 1000.0 / (t1 - t0)
            self.fpss.append(self.fps)
        
            self.frame_count += 1
            self.loop_frame += 1
            
        # exited main loop
        pygame.quit()
    
    #------------------------------------------------------------------------------------
    def save_frame(self, frame_number):
        
        self.pixels = np.empty(self.window_dimensions[0] * self.window_dimensions[1] * 3, np.float32)
        #self.pixels = np.zeros((*self.window_dimensions, 3), np.float32)
        glReadPixels(0, 0,
                     *self.window_dimensions,
                     GL_RGB,
                     GL_FLOAT,
                     array=self.pixels,
                     outputType=None)
        self.pixels = self.pixels.reshape(self.window_dimensions[1], self.window_dimensions[0], 3)[::-1, :]

        filename = str(frame_number)
        leading_zeros = 10 - len(filename)
        filename = '0'*leading_zeros + filename
        img = Image.fromarray(np.uint8(self.pixels * 255.0), mode='RGB')
        img.save(f'../../_RESOURCES/fake-SLAM/{filename}.png')
        
    #------------------------------------------------------------------------------------
    def process_keyboard_events_(self, event):
        if event.key == pygame.K_ESCAPE:
            self.is_running = False
        elif event.key == pygame.K_TAB:
            self.object_selection_mode = not self.object_selection_mode
            print('selection mode : {}'.format('ON' if self.object_selection_mode else 'OFF'))
        elif event.key == pygame.K_F4:
            self.wireframe_mode = not self.wireframe_mode
            print('wireframe mode : {}'.format('ON' if self.wireframe_mode else 'OFF'))
        elif event.key == pygame.K_p:
            for object in self.objects:
                print(object.pos)

        elif event.key == pygame.K_s:
            self.save_frame()

        if self.object_selection_mode:
            if event.key == pygame.K_LEFT:
                self.selected_object = (self.selected_object - 1) % len(self.objects)
                print(f'object {self.selected_object} selected')
            elif event.key == pygame.K_RIGHT:
                self.selected_object = (self.selected_object + 1) % len(self.objects)
                print(f'object {self.selected_object} selected')
                
    #------------------------------------------------------------------------------------
    def process_input_(self):
        self.keys = pygame.key.get_pressed()
        
        if self.object_selection_mode:
            if self.keys[pygame.K_a]:
                self.objects[self.selected_object].pos[0] -= 0.1
            if self.keys[pygame.K_d]:
                self.objects[self.selected_object].pos[0] += 0.1
            if self.keys[pygame.K_SPACE]:
                self.objects[self.selected_object].pos[1] += 0.1
            if self.keys[pygame.K_LSHIFT]:
                self.objects[self.selected_object].pos[1] -= 0.1
            if self.keys[pygame.K_s]:
                self.objects[self.selected_object].pos[2] += 0.1
            if self.keys[pygame.K_w]:
                self.objects[self.selected_object].pos[2] -= 0.1

    #------------------------------------------------------------------------------------
    def process_events_(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self.process_keyboard_events_(event)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                self.process_mouse_events_(event)

    #------------------------------------------------------------------------------------
    def process_mouse_events_(self, event):
        if event.type == pygame.MOUSEMOTION:
            pass
            #print(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print(event.pos)

    #------------------------------------------------------------------------------------
    def setup_openGL_(self):
        
        OpenGL.UNSIGNED_BYTE_IMAGES_AS_STRING = False
        
        # position the window
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (self.window_position[0], 
                                                        self.window_position[1])
        # initialize and create display
        pygame.init()
        self.surface = pygame.display.set_mode(self.window_dimensions, pygame.DOUBLEBUF | pygame.OPENGL)
        
        gluPerspective(45, (self.window_dimensions[0]/self.window_dimensions[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -10.0)
        
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST, GL_LEQUAL)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    
