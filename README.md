## perception
Toy implementations of lane marker detection and SLAM.

## execution
SLAM depends on Pangolin. Building Pangolin on Ubuntu 20.04 proved somewhat difficult. For recent versions of Pangolin, Eigen is a required dependency. To make Eigen visible to cmake, I edited pangolin/src/CMakeLists.txt. The variable EIGEN_INCLUDE_DIR was pointed to the system location of the un-tar:ed Eigen lib:
> set(EIGEN_INCLUDE_DIR, "/usr/local/lib/eigen-3.4.0)

In addition, a soft link to the Eigen include directory was added to /usr/include with:
> ln -s /usr/local/lib/eigen-3.4.0/Eigen/ /usr/include/Eigen
	
After this, building was successful.

