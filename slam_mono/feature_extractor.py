
from curses import noraw
import cv2
import numpy as np

from skimage.measure import ransac
from skimage.transform import FundamentalMatrixTransform
from skimage.transform import EssentialMatrixTransform

np.set_printoptions(suppress=True)

#----------------------------------------------------------------------------------------
def add_ones(x):
    # turns [[x, y]] into [[x, y, 1]]
    if len(x.shape) == 1:
        return np.concatenate([x, np.array([1.0])], axis=0)
    # else:
    return np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)

#----------------------------------------------------------------------------------------
def pose_from_Rt(R, t):
    """
    Concatenates R and t to a camera pose (4x4 matrix).
    """
    Rt = np.eye(4)
    Rt[:3, :3] = R
    Rt[:3, 3] = t
    return Rt

#----------------------------------------------------------------------------------------
def E_to_Rt(E):
    """
    Calculate the pose (rotation and translation of the camera)
    from the essential matrix.
    """
        
    # We have now switched to an essential matrix, and trying to get the
    # pose of the camera (i.e. rotation, R, and translation, t)
    W = np.mat([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    U, S, V_T = np.linalg.svd(E)
    
    # There exists 4-way ambiguity which satisfy the decomposition (a-d);
    # Hartley & Zisserman, p 260, fig 9.12

    # a+b: Using the determinants we can take the negative of either U or V_T
    assert(np.linalg.det(U) > 0) # should always be 
    #if np.linalg.det(U) < 0:
    #    U *= -1.0
    if np.linalg.det(V_T) < 0:
        V_T *= -1.0
    # c+d: The diagonal of the correct rotation should be [1, 1, 1]
    R = np.dot(np.dot(U, W), V_T)
    if np.sum(np.diag(R)) < 0:
        R = np.dot(np.dot(U, W.T), V_T)    
    t = U[:, 2].reshape(3, 1)
    Rt = np.concatenate([R, t], axis=1)
    return Rt
    #return np.linalg.inv(pose_from_Rt(R, t))

#----------------------------------------------------------------------------------------
class FeatureExtractor(object):
    def __init__(self, K):
        self.orb = cv2.ORB_create()
        self.BFMatcher = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
        self.this_frame = None
        self.last_frame = None
        
        # camera intrinsics
        self.K = K
        self.K_inv = np.linalg.inv(K)
        self.Rt = None              # pose of camera, i.e. R|t (rotation/translation)
        self.W = int(2 * K[0, 2])   # width
        self.H = int(2 * K[1, 2])   # height
        
    #------------------------------------------------------------------------------------
    def process_frame(self, frame):
        """
        Returns the extracted keypoints of a frame.
        """
        self.last_frame = self.this_frame
        
        # TODO : remove this assertion?
        if frame[:,:,0].shape != (self.W, self.H):
            frame_ = cv2.resize(frame, (self.W, self.H))
        else:
            frame_ = frame
        
        #kps, des = self.orb.detectAndCompute(frame_, None)
        pts = cv2.goodFeaturesToTrack(np.mean(frame_, axis=2).astype(np.uint8), 
                                      maxCorners=3000,
                                      qualityLevel=0.01,
                                      minDistance=7)
        
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
        
        ret = []
        idxs_curr, idxs_prev = [], []

        # TODO : deal with this None crap: perhaps hot start the feature extraction
        if self.last_frame is not None and \
           self.this_frame['des'] is not None and \
           self.last_frame['des'] is not None:
            
            # match ORB descriptors between frames
            matches = self.BFMatcher.knnMatch(self.this_frame['des'], self.last_frame['des'], k=2)
            
            # Lowe's ratio test for knn matching
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    p0 = self.this_frame['kps'][m.queryIdx]
                    p1 = self.last_frame['kps'][m.trainIdx]
                    if m.queryIdx not in idxs_curr and m.trainIdx not in idxs_prev:
                        idxs_curr.append(m.queryIdx)
                        idxs_prev.append(m.trainIdx)
                        ret.append((p0, p1))
            
            ret = np.array(ret)
            idxs_curr = np.array(idxs_curr)
            idxs_prev = np.array(idxs_prev)

            
            # Estimate the epipolar geometry between frames using
            # ransac (identifying inliers and outliers in the matches)
            # between frames, and using resulting inliers to estimate the 
            # fundamental matrix.
            # https://www.robots.ox.ac.uk/~vgg/hzbook/hzbook2/HZepipolar.pdf
            
            # We assume that the focal point is the center of the image
            # (which would be true for all fps videos). Therefore, we subtract
            # by half the image shape, so that the coordinate system essentially
            # becomes (-w/2, -h/2) to (w/2, h/2)

            self.Rt = None
            assert(ret.shape[0] >= 8)
            
            # perform focal point transform (according to above)
            ret[:, 0, :] = np.dot(self.K_inv, add_ones(ret[:, 0, :]).T).T[:, 0:2]
            ret[:, 1, :] = np.dot(self.K_inv, add_ones(ret[:, 1, :]).T).T[:, 0:2]
            #ret = self.focal_point_transform(ret, normalize=True)
            
            # estimate the fundamental matrix, F, and filter out outlying matches
            model, inliers = ransac(data=(ret[:, 0], ret[:, 1]),
                                    #model_class=FundamentalMatrixTransform,
                                    model_class=EssentialMatrixTransform,
                                    min_samples=8,
                                    #residual_threshold=1,
                                    residual_threshold=0.005,
                                    max_trials=100)
            
            print(f"{len(self.this_frame['des'])} -> {len(ret)} -> {sum(inliers)}")
            #print('F:\n', model.params)
            
            # Finding focal length from the fundamental matrix
            #
            #    E = K'.T @ F @ K, 
            #
            # where E is the essential matrix, K is the camera instrinsic matrix and 
            # F is the fundamental matrix. 
            # For E to be correct, there exist a decomposition of U, S, V_T = svd(E)
            # s.t. E = U @ diag(1, 1, 0) @ V_T. Therefore, when searching for the instrisic
            # camera matrix K yielding a good approximation of E (more specifically, the 
            # focal length f [ f=(f_x, f_y), which are assumed to be equal]), we 
            # can search the space of F for a scalar which results in a diagnonal sigma 
            # matrix (1, 1, 0) in the single value decomp of F:
            # > U, S, V_T = np.linalg.svd(model.params)
            # > print(S) # this should be a vector (1, 1, 0)
            #
            # N.B. Although the method above is very crude, since the target values 
            # of the optimization is known (i.e. np.sum(S.diag()) -> 2.0), a form of 
            # auto-calibration could be done through search of the f parameter in an 
            # automated fashion.
            #
            
            # Extract camera pose from the essential matrix
            self.Rt = E_to_Rt(model.params)
            print(self.Rt)


            # Return to original image coordinates for plotting of features and matches
            # TODO : move this somewhere else? More efficient implementation?
            ret[:, 0, :] = np.dot(self.K, add_ones(ret[:, 0, :]).T).T[:, 0:2]
            ret[:, 1, :] = np.dot(self.K, add_ones(ret[:, 1, :]).T).T[:, 0:2]
            #ret = self.focal_point_transform(ret, normalize=False)

            ret = ret[inliers]

        # return the inlying points, the indices of the points in the current frame
        # and the indices to the matching points in the previous frame
        return ret, idxs_curr, idxs_prev
        

