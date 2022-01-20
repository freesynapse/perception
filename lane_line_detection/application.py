
import sdl2, sdl2.ext
import sdl_timer

import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys

from feature_extractor import FeatureExtractor
from features import VIDEO_FEATURES_0, VIDEO_FEATURES_1, VIDEO_FEATURES_2, VIDEO_FEATURES_3
from opencv_utils import Video

#----------------------------------------------------------------------------------------
def add_alpha_to_image(img):
    return np.insert(img, 3, 255, axis=2)

#----------------------------------------------------------------------------------------
# constants
CAM_WIDTH, CAM_HEIGHT = 480, 270

class Application(object):
    """ 
        Encapsulation class for the application.
        * The class is itself a wrapper for SDL, for displaying video and handling events.
        * Video : class encapsulator for a cv2.VideoCapture object.
        * Extractor : class for extracting features from frames using open-cv.
    """
    def __init__(self, window_width, window_height):

        # initialize sdl and create window
        self.window_width = window_width
        self.window_height = window_height
        self.win_to_cam_ar = (window_width / CAM_WIDTH, window_height / CAM_HEIGHT)
            
        # initalize SDL and create a surface to draw opencv images to
        sdl2.ext.init()
        self.window = sdl2.ext.Window("SDL2", size=(self.window_width, self.window_height),
                                      position=(0, 0))
        self.window.show()
        self.surface = sdl2.SDL_GetWindowSurface(self.window.window)
        self.surface_array = sdl2.ext.pixels3d(self.surface.contents)
        
        # input
        self.key_states = sdl2.SDL_GetKeyboardState(None)
        self.key_down = False
        
        # loop
        self.is_running = True
        self.is_paused = False
        self.is_in_console_mode = False
        self.frame = None
        self.clock = sdl_timer.Clock()
        
        # get features and setup feature extractor
        self.features = VIDEO_FEATURES_3
        
        self.extractor = FeatureExtractor(self.features)
        self.selected_view = 'final'
        self.extractor.set_view(self.selected_view)

        # load video file
        self.video = Video(self.features['filename'], 
                           CAM_WIDTH, CAM_HEIGHT, 
                           self.features['start_frame'])
        self.time_per_frame = 1000.0 / self.video.fps

        # hack to be able to switch between viewing modes
        view_keys = [sdl2.SDLK_q, # -- this will always be the first key, the 'final' view
                     sdl2.SDLK_w, sdl2.SDLK_e, sdl2.SDLK_r, sdl2.SDLK_t, sdl2.SDLK_y, sdl2.SDLK_u, 
                     sdl2.SDLK_i, sdl2.SDLK_o, sdl2.SDLK_p, sdl2.SDLK_a, sdl2.SDLK_s, sdl2.SDLK_d, 
                     sdl2.SDLK_f, sdl2.SDLK_g, sdl2.SDLK_h, sdl2.SDLK_j, sdl2.SDLK_k, sdl2.SDLK_l, 
                     sdl2.SDLK_z, sdl2.SDLK_x, sdl2.SDLK_c, sdl2.SDLK_v, sdl2.SDLK_b, sdl2.SDLK_n,
                     sdl2.SDLK_m
                     ]
        self.views_dict = {}
        for keycode, view in zip(view_keys, self.extractor.frame.keys()):
            self.views_dict[keycode] = view

    #------------------------------------------------------------------------------------
    def is_key_pressed(self, sdl_key_code):
        # handles repeating keys (i.e. for first-person controls)
        if self.key_states[sdl_key_code] and not self.key_down:
            self.key_down = True
            return True
        elif not self.key_states[sdl_key_code] and self.key_down:
            self.key_down = False
            return False
        
    #------------------------------------------------------------------------------------
    def process_keyboard_events(self, keycode):
        
        # quit
        if keycode == sdl2.SDLK_ESCAPE:
            self.is_running = False
            return

        if self.is_in_console_mode:
            return
        
        # pauses playback
        if keycode == sdl2.SDLK_SPACE:
            self.is_paused = not self.is_paused
            if self.is_paused:
                print('paused at frame', self.video.current_frame)
        # pauses and plots the current view with mpl
        elif keycode == sdl2.SDLK_TAB:
            print('exporting view to matplotlib')
            fig, ax = plt.subplots(1, 1, figsize=(10, 10))
            ax.imshow(self.extractor.get_frame())
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(self.selected_view)
            plt.show()
        # start console
        elif keycode == sdl2.SDLK_RETURN:
            self.is_paused = True
            self.is_in_console_mode = True
            print('paused at frame', self.video.current_frame)
            for k in self.features.keys():
                if k != 'filename' and k != 'start_frame': 
                    print(f"{k}: {self.features[k]}")
            command = input('> ')
            self.parse_input_string_(command)

        if keycode in self.views_dict.keys():
            self.selected_view = self.views_dict[keycode]
            self.extractor.set_view(self.selected_view)
    
    #------------------------------------------------------------------------------------
    def process_mouse_events(self, event):
        print(f'[{int(event.button.x / self.win_to_cam_ar[0])},'
              f' {int(event.button.y / self.win_to_cam_ar[1])}]')
        
    #------------------------------------------------------------------------------------
    def main_loop(self):
        """
        Enters SDL main loop, with a callback each frame.
        Each frame, self.frame is copied to the surface, 
        the callback_fnc may alter this.
        """
        
        while (self.is_running):
            
            self.clock.tick()
            t0 = sdl_timer.get_time()
            
            # get frame from video
            if self.is_paused == False:
                _, self.frame = self.video.get_next_frame()

            #self.extractor.extract_lane_markers(self.frame)
            self.extractor.extract_lane_markers_2(self.frame)
            frame = self.extractor.get_frame()

            # convert to format compatible with blitting
            frame = self.cv2_to_sdl2_(frame)
            
            if frame.shape[0] != self.window_width or frame.shape[1] != self.window_height:
                frame = cv2.resize(frame, 
                                (self.window_height, self.window_width), 
                                interpolation=cv2.INTER_AREA)
            
            # copy to SDL surface
            np.copyto(self.surface_array, frame)

            # SDL events and exit conditions
            sdl_events = sdl2.ext.get_events()
            for event in sdl_events:
                if event == sdl2.SDL_QUIT:
                    return False
                # the event type == sdl2.SDL_KeyboardEvent --> SDL_KEYDOWN or SDL_KEYUP
                # event.state is SDL_PRESSED or SDL_RELEASED
                # event.key.keysym.sym is the keycode
                elif event.type == sdl2.SDL_KEYDOWN:
                    self.process_keyboard_events(event.key.keysym.sym)
                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    self.process_mouse_events(event)
                #elif event.type == sdl2.SDL_MOUSEMOTION:
                #    print(dir(event))

            render_time = sdl_timer.get_delta(t0)
            sleep_time = self.time_per_frame - render_time
            if sleep_time > 1:
                sdl_timer.wait(int(sleep_time))

            # flip surfaces
            self.window.refresh()

    #----------------------------------------------------------------------------------------
    def parse_input_string_(self, cmd):
        args = cmd.split(' ')
        if len(args) < 2:
            print('invalid command.')
        elif len(args) == 2:
            feature = args[0]
            arg = args[1]
            self.features[feature] = int(arg)
            print(f"Setting feature '{feature}' to {int(arg)}.")
        print(self.video.current_frame)
        self.is_in_console_mode = False

    #----------------------------------------------------------------------------------------
    def to_rgba_(self, frame):
        if (frame.ndim == 2):
            frame = frame.reshape(frame.shape[0], frame.shape[1], 1)
            frame = np.repeat(frame, 3, axis=2)
        # show view
        cv2.putText(img=frame,
                    text='view: ' + self.selected_view, 
                    org=(3, 10), 
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX,
                    color=(255, 0, 255),
                    fontScale=0.4)
        # add alpha
        frame = np.insert(frame, 3, 255, axis=2)
        
        return frame

    #----------------------------------------------------------------------------------------
    def cv2_to_sdl2_(self, frame):
        frame = self.to_rgba_(frame)
        frame = frame.swapaxes(0, 1)
        return frame
    

