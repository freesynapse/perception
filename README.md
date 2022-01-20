# Perception
Toy implementations of lane marker detection and SLAM (for now).

# Building

## slam_mono
slam_mono uses Pangolin for rendering of poses. Building Pangolin on Ubuntu 20.04 proved somewhat difficult. For recent versions of Pangolin, Eigen is a required dependency. To make Eigen visible to cmake, I edited pangolin/src/CMakeLists.txt. The variable EIGEN_INCLUDE_DIR was pointed to the system location of the un-tar:ed Eigen lib:
> set(EIGEN_INCLUDE_DIR, "/usr/local/lib/eigen-3.4.0)

In addition, a soft link to the Eigen include directory was added to /usr/include with:
> ln -s /usr/local/lib/eigen-3.4.0/Eigen/ /usr/include/Eigen
	
After this, building was successful.

For building of g2opy, a number of adjustments was needed. g2opy depends on (to name a few):

* QGLViewer --> built according to instructions at http://libqglviewer.com/installUnix.html
* libcholmod --> this was already installed, but by installing libsuitesparse-dev, this was resolved (as mentioned [here](https://github.com/jingpang/LearnVIORB/issues/13)).
* Eigen3; similar issues as with Pangolin: resolved in much of the same manner. I edited ./g2opy/cmake_modules/FindEigen3.cmake to point cmake to the correct libraries for Eigen. The modified file is included in the repo.
* In Eigen3 the return type of some quternion-related functions (Eigen::Quaterniond::x() / ::y() / ::z() and ::w()) were changed to const double & (sometimes before eigen-3.4.0, which is what I have). In the pybind references to these functions the return type is expected to be double &. To fix this issue, the eigen_types.h was changed (the updated file is included in this repo under g2opy).
 

