
import numpy as np

class Features(dict):
    def __init__(self, *args, **kwargs):
        super(Features, self).__init__(*args, **kwargs)
        self['polygon']    = np.array([[50, 270], [220, 160], [360, 160], [480, 270]])
        self['yellow_low'] = np.array([10, 100, 100], dtype='uint8')
        self['yellow_hi']  = np.array([30, 255, 255], dtype='uint8')
        self['light_low']  = 170
        self['light_hi']   = 255
        self['white_low']  = 200
        self['sobel_threshold'] = 100
        self['threshold'] = 127

polygon3 = np.array([[30, 270], [240, 160], [450, 270]])                # driving3.mp4
polygon4 = np.array([[20, 270], [190, 175], [290, 175], [460, 270]])    # driving4.mp4

VIDEO_FEATURES_0 = Features()
VIDEO_FEATURES_0['filename']    = '../_RESOURCES/driving0.mp4'
VIDEO_FEATURES_0['start_frame'] = 0
VIDEO_FEATURES_0['polygon']     = np.array([[115, 270], [270, 160], [305, 160], [480, 245], [480, 270]])
VIDEO_FEATURES_0['yellow_low']  = np.array([10, 100, 100], dtype='uint8')
VIDEO_FEATURES_0['yellow_hi']   = np.array([30, 255, 255], dtype='uint8')
VIDEO_FEATURES_0['light_low']   = 200
VIDEO_FEATURES_0['light_hi']    = 255
VIDEO_FEATURES_0['white_low']   = 200
VIDEO_FEATURES_0['sobel_threshold'] = 100
VIDEO_FEATURES_0['threshold'] = 127


VIDEO_FEATURES_1 = Features()
VIDEO_FEATURES_1['filename']    = '../_RESOURCES/driving1.mp4'
VIDEO_FEATURES_1['start_frame'] = 0
VIDEO_FEATURES_1['polygon']     = np.array([[60, 250], [225, 170], [290, 170], [475, 250]])
VIDEO_FEATURES_1['yellow_low']  = np.array([10, 100, 100], dtype='uint8')
VIDEO_FEATURES_1['yellow_hi']   = np.array([30, 255, 255], dtype='uint8')
VIDEO_FEATURES_1['light_low']   = 200
VIDEO_FEATURES_1['light_hi']    = 255
VIDEO_FEATURES_1['white_low']   = 200
VIDEO_FEATURES_1['sobel_threshold'] = 100
VIDEO_FEATURES_0['threshold'] = 127

VIDEO_FEATURES_2 = Features()
VIDEO_FEATURES_2['start_frame'] = 12500
VIDEO_FEATURES_2['filename']    = '../_RESOURCES/driving2.mp4'
VIDEO_FEATURES_2['polygon']     = np.array([[40, 270], [210, 170], [265, 170], [455, 270]])
VIDEO_FEATURES_2['yellow_low']  = np.array([10, 100, 100], dtype='uint8')
VIDEO_FEATURES_2['yellow_hi']   = np.array([30, 255, 255], dtype='uint8')
VIDEO_FEATURES_2['light_low']   = 200
VIDEO_FEATURES_2['light_hi']    = 255
VIDEO_FEATURES_2['white_low']   = 200
VIDEO_FEATURES_2['sobel_threshold'] = 100
VIDEO_FEATURES_0['threshold'] = 100

VIDEO_FEATURES_3 = Features()
VIDEO_FEATURES_3['filename']    = '../_RESOURCES/driving3.mp4'
VIDEO_FEATURES_3['start_frame'] = 0
VIDEO_FEATURES_3['polygon']     = np.array([[40, 270], [210, 170], [265, 170], [455, 270]])
VIDEO_FEATURES_3['yellow_low']  = np.array([10, 100, 100], dtype='uint8')
VIDEO_FEATURES_3['yellow_hi']   = np.array([30, 255, 255], dtype='uint8')
VIDEO_FEATURES_3['light_low']   = 200
VIDEO_FEATURES_3['light_hi']    = 255
VIDEO_FEATURES_3['white_low']   = 200
VIDEO_FEATURES_3['sobel_threshold'] = 100
VIDEO_FEATURES_0['threshold'] = 127






