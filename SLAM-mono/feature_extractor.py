
import cv2
import numpy as np

from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform

np.set_printoptions(suppress=True)


#----------------------------------------------------------------------------------------
def pose_from_Rt(R, t):
    """
    Concatenates R and t to a camera pose (4x4 matrix).
    """
    M = np.eye(4)
    M[:3, :3] = R
    M[:3, 3] = t
    return M

#----------------------------------------------------------------------------------------
def fundamental_to_Rt(F):
    """
    Calculate the pose (rotation and translation of the camera)
    from the fundamental matrix.
    """
    W = np.mat([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=np.float32)
    U, Sigma, V_T = np.linalg.svd(F)
    if np.linalg.det(U) < 0:
        U *= -1.0
    if np.linalg.det(V_T) < 0:
        V_T *= -1.0
    R = np.dot(np.dot(U, W), V_T)
    t = U[:, 2]
    
    if (t[2] < 0):
        t *= -1.0
        
    return np.linalg.inv(pose_from_Rt(R, t))

#----------------------------------------------------------------------------------------
class FeatureExtractor(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.orb = cv2.ORB_create()
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
        self.this_frame = None
        self.last_frame = None
        
    #------------------------------------------------------------------------------------
    def process_frame(self, frame):
        """
        Returns the extracted keypoints of a frame.
        """
        self.last_frame = self.this_frame
        
        # TODO : remove this assertion?
        if frame[:,:,0].shape != (self.width, self.height):
            frame_ = cv2.resize(frame, (self.width, self.height))
        else:
            frame_ = frame
        
        #kps, des = self.orb.detectAndCompute(frame_, None)
        pts = cv2.goodFeaturesToTrack(np.mean(frame_, axis=2).astype(np.uint8), 
                                      maxCorners=3000,
                                      qualityLevel=0.1,
                                      minDistance=5)
        
        kps, des = None, None
        if pts is not None:
            kps = [cv2.KeyPoint(x=p[0][0], y=p[0][1], _size=20) for p in pts]
            kps, des = self.orb.compute(frame_, kps)
            kps = np.array([(kp.pt[0], kp.pt[1]) for kp in kps])
        self.this_frame = { 'des': des, 'kps': kps }

        return kps, des
    
    #------------------------------------------------------------------------------------
    def match_frames(self):
        """
        Find matching keypoints between frames to track using 
        ORB feature descriptors.
        """
        # TODO : deal with this None crap
        if self.last_frame is not None and \
           self.this_frame['des'] is not None and \
           self.last_frame['des'] is not None:
            
            # match ORB descriptors between frames
            matches = self.BFMatcher.knnMatch(self.this_frame['des'], self.last_frame['des'], k=2)
            
            ret = []
            idx0, idx1 = [], []
            
            # Lowe's ratio test for knn matching
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    p0 = self.this_frame['kps'][m.queryIdx]
                    p1 = self.last_frame['kps'][m.trainIdx]
                    if m.queryIdx not in idx0 and m.trainIdx not in idx1:
                        idx0.append(m.queryIdx)
                        idx1.append(m.trainIdx)
                        ret.append((p0, p1))
            
            ret = np.array(ret)
            idx0 = np.array(idx0)
            idx1 = np.array(idx1)

            
            # Estimate the epipolar geometry between frames using
            # ransac (identifying inliers and outliers in the matches)
            # between frames, and using these inliers to estimate the 
            # fundamental matrix.
            # https://www.robots.ox.ac.uk/~vgg/hzbook/hzbook2/HZepipolar.pdf
            
            assert(ret.shape[0] >= 8)

            # We assume that the focal point is the center of the image
            # (which would be true for all fps videos). Therefore, we subtract
            # by half the image shape, so that the coordinate system essentially
            # becomes (-w/2, -h/2) to (w/2, h/2)
            def focal_point_transform(pt_array, normalize):
                if normalize:
                    pt_array[:, :, 0] -= self.width / 2
                    pt_array[:, :, 1] -= self.height / 2
                else:
                    pt_array[:, :, 0] += self.width / 2
                    pt_array[:, :, 1] += self.height / 2
                return pt_array

            # perform focal point transform (according to above)
            ret = focal_point_transform(ret, normalize=True)
            
            # estimate the fundamental matrix, F, and filter out outlying matches
            model, inliers = ransac(data=(ret[:, 0], ret[:, 1]),
                                    model_class=FundamentalMatrixTransform,
                                    min_samples=8,
                                    residual_threshold=1,
                                    max_trials=100)
            
            print(f"{len(self.this_frame['des'])} -> {len(ret)} -> {len(inliers)} -> {sum(inliers)}")
            print(model.params)
            
            # From the fundamental matrix, we can estimate the instrinsic
            # camera pose (rotation, R, and translation, t)
            

            # Return to original image coordinates for plotting of features and matches
            # TODO : move this somewhere else? More efficient implementation?
            ret = focal_point_transform(ret, normalize=False)
            
            return ret[inliers]
        

