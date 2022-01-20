
import numpy as np
import cv2

from features import Features

class FeatureExtractor(object):
    
    def __init__(self, features : Features):
        self.frame = {}
        self.frame['final']             = None
        self.frame['ROI']               = None
        self.frame['HSV']               = None
        self.frame['HLS']               = None
        self.frame['gray']              = None
        self.frame['mask_L']            = None
        self.frame['Gaussian']          = None
        self.frame['mask_sobel_dx']     = None
        self.frame['mask_Y']            = None
        self.frame['mask_W']            = None
        self.frame['mask_LYW_sobel']    = None
        self.frame['ROI_LYW_sobel']     = None
        self.frame['threshold']         = None
        #self.frame['final']         = None
        #self.frame['HSV']           = None
        #self.frame['gray']          = None
        #self.frame['mask_yellow']   = None
        #self.frame['mask_white']    = None
        #self.frame['mask_yw']       = None
        #self.frame['mask_sobel_x']  = None
        #self.frame['mask_sobel_yw'] = None
        #self.frame['ROI_sobel_yw']  = None
        #self.frame['Gaussian']      = None
        #self.frame['threshold']     = None

        # features
        self.feats = features
        #self.light_lo = 160
        #self.light_hi = 255
        #self.yellow_lo = np.array([10, 100, 100], dtype='uint8')
        #self.yellow_hi = np.array([30, 255, 255], dtype='uint8')
        #self.white_lo = 180

        self.lines_overlay = None
        self.selected_view = 'final'
        
        #self.ROI_polygon = polygon
    
    #------------------------------------------------------------------------------------    
    def set_view(self, view):
        self.selected_view = view
    
    #------------------------------------------------------------------------------------    
    def get_frame(self):
        return self.frame[self.selected_view]

    #------------------------------------------------------------------------------------
    def extract_lane_markers_2(self, frame):
        # create a polygon containing the region of interest (roi)
        stencil = np.zeros_like(frame[:, :, 0])
        cv2.fillConvexPoly(stencil, self.feats['polygon'], 1)
        # crop frame to roi
        self.frame['ROI'] = cv2.bitwise_and(frame, frame, mask=stencil)
        
        # filter on yellow (hsv) and white (gray)
        self.frame['HSV'] = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.frame['HLS'] = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        self.frame['gray'] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # filter on pixels with high lightness (in HLS)
        self.frame['mask_L'] = cv2.inRange(self.frame['HLS'][:,:,1], 
                                           self.feats['light_low'], 
                                           self.feats['light_hi'])
        
        # extract horizontal edges (dx)
        self.frame['Gaussian'] = cv2.GaussianBlur(self.frame['gray'], (1, 1), 1)
        sobel_x = np.absolute(cv2.Sobel(self.frame['Gaussian'], cv2.CV_64F, 1, 0, ksize=3))
        self.frame['mask_sobel_dx'] = np.zeros_like(stencil)
        self.frame['mask_sobel_dx'][sobel_x > self.feats['sobel_threshold']] = 1
        mask = cv2.bitwise_or(self.frame['mask_L'], self.frame['mask_sobel_dx'])
        
        # extract yellow and white from HSV and grayscale, respectively
        self.frame['mask_Y'] = cv2.inRange(self.frame['HSV'], 
                                           self.feats['yellow_low'],
                                           self.feats['yellow_hi'])
        self.frame['mask_W'] = cv2.inRange(self.frame['gray'], self.feats['white_low'], 255)
        
        # update mask
        mask = cv2.bitwise_or(mask, self.frame['mask_Y'])
        mask = cv2.bitwise_or(mask, self.frame['mask_W'])
        self.frame['mask_LYW_sobel'] = mask
        
        # apply mask to ROI
        self.frame['ROI_LYW_sobel'] = cv2.bitwise_and(self.frame['ROI'], 
                                                      self.frame['ROI'],
                                                      mask=mask)

        # threshold only bright pixels in the final mask
        _, self.frame['threshold'] = cv2.threshold(self.frame['ROI_LYW_sobel'], 
                                                   self.feats['threshold'], 255, 
                                                   cv2.THRESH_BINARY)
        
        # get line segments -- extract from the red channel (ie both white and yellow)
        lines = cv2.HoughLinesP(self.frame['threshold'][:,:,2], 2, np.pi/180.0, 20, maxLineGap=400)
        
        if (type(lines) != type(None)):
            self.lines_overlay = np.zeros_like(frame)
            #left_x, left_y, right_x, right_y = [], [], [], []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.circle(self.lines_overlay, (x1, y1), 4, (0, 255, 0))
                cv2.circle(self.lines_overlay, (x2, y2), 4, (0, 255, 0))
                cv2.line(self.lines_overlay, (x1, y1), (x2, y2), (255, 0, 0), 3)
            self.frame['final'] = cv2.addWeighted(frame, 1.0, self.lines_overlay, 1, 1)
        else:
            self.frame['final'] = frame
            
    #------------------------------------------------------------------------------------
    def extract_lane_markers(self, frame):
        # create a polygon containing the region of interest (roi)
        stencil = np.zeros_like(frame[:, :, 0])
                
        cv2.fillConvexPoly(stencil, self.ROI_polygon, 1)
        # crop frame to roi
        self.frame['ROI'] = cv2.bitwise_and(frame, frame, mask=stencil)
        
        # filter on yellow (hsv) and white (gray)
        self.frame['HSV'] = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.frame['HLS'] = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
        self.frame['gray'] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # filter on pixels with high lightness (in HLS)
        self.frame['mask_light'] = cv2.inRange(self.frame['HLS'][:,:,1], 150, 255)

        yellow_lo = np.array([10, 100, 100], dtype='uint8')
        yellow_hi = np.array([30, 255, 255], dtype='uint8')
        self.frame['mask_yellow'] = cv2.inRange(self.frame['HSV'], yellow_lo, yellow_hi)
        self.frame['mask_white'] = cv2.inRange(self.frame['gray'], 190, 255)
        self.frame['mask_yw'] = cv2.bitwise_or(self.frame['mask_yellow'], self.frame['mask_white'])
        
        # perform Sobel edge detection for the x direction
        self.frame['Gaussian'] = cv2.GaussianBlur(self.frame['gray'], (3, 3), 1)
        sobel_x = np.absolute(cv2.Sobel(self.frame['Gaussian'], cv2.CV_64F, 1, 0, ksize=3))
        self.frame['mask_sobel_x'] = np.zeros_like(stencil)
        self.frame['mask_sobel_x'][sobel_x > 100] = 1
        
        # update mask
        self.frame['mask_sobel_yw'] = cv2.bitwise_or(self.frame['mask_yw'], self.frame['mask_sobel_x'])
        
        # apply yellow-white mask to roi
        self.frame['ROI_sobel_yw'] = cv2.bitwise_and(self.frame['ROI'], 
                                                     self.frame['ROI'], 
                                                     mask=self.frame['mask_sobel_yw'])

        # threshold only bright values
        #_, frame_threshold = cv2.threshold(frame_roi_yw, 160, 250, cv2.THRESH_BINARY)
        _, self.frame['threshold'] = cv2.threshold(self.frame['ROI_sobel_yw'], 110, 250, cv2.THRESH_BINARY)
        
        # get line segments -- extract from the red channel (ie both white and yellow)
        lines = cv2.HoughLinesP(self.frame['threshold'][:,:,2], 2, np.pi/180.0, 20, maxLineGap=400)
        
        if (type(lines) != type(None)):
            self.lines_overlay = np.zeros_like(frame)
            #left_x, left_y, right_x, right_y = [], [], [], []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.circle(self.lines_overlay, (x1, y1), 4, (0, 255, 0))
                cv2.circle(self.lines_overlay, (x2, y2), 4, (0, 255, 0))
                cv2.line(self.lines_overlay, (x1, y1), (x2, y2), (255, 0, 0), 3)
                
                #beta1 = np.polyfit((x1, x2), (y1, y2), 1)[0]
                #if beta1 > 0:   
                #    left_x.append([x1, x2])
                #    left_y.append([y1, y2])
                #else:
                #    right_x.append([x1, x2])
                #    right_y.append([y1, y2])
            #if len(left_x) > 0 and len(left_y) > 0 and \
            #   len(right_x) > 0 and len(right_y) > 0:
            #    p0 = (np.min(left_x), np.min(left_y))
            #    p1 = (np.max(left_x), np.max(left_y))
            #    p2 = (np.min(right_x), np.max(right_y))
            #    p3 = (np.max(right_x), np.min(right_y))
                #cv2.line(lines_overlay, p0, p1, (0, 255, 0), 4)
                #cv2.line(lines_overlay, p2, p3, (0, 255, 0), 4)
                #cv2.fillConvexPoly(lines_overlay, 
                #                   np.array([p0, p1, p2, p3]), 
                #                   (0, 63, 0))
            
            self.frame['final'] = cv2.addWeighted(frame, 1.0, self.lines_overlay, 1, 1)
        else:
            self.frame['final'] = frame
  

