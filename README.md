# faceRecognizer with Jetson nano
See also https://wisteriahill.sakura.ne.jp/CMS/WordPress/2020/12/15/jetson-nano-build-dlib-use-gpu-for-face-recognition/ before install of dlib and face_recognition.

# 0. Jetpack version
```
$ sudo apt show nvidia-jetpack -a
Package: nvidia-jetpack
Version: 4.5.1-b17
Priority: standard
Section: metapackages
Maintainer: NVIDIA Corporation
Installed-Size: 199 kB
Depends: nvidia-cuda (= 4.5.1-b17), nvidia-opencv (= 4.5.1-b17), nvidia-cudnn8 (= 4.5.1-b17), nvidia-tensorrt (= 4.5.1-b17), nvidia-visionworks (= 4.5.1-b17), nvidia-container (= 4.5.1-b17), nvidia-vpi (= 4.5.1-b17), nvidia-l4t-jetson-multimedia-api (>> 32.5-0), nvidia-l4t-jetson-multimedia-api (<< 32.6-0)
Homepage: http://developer.nvidia.com/jetson
Download-Size: 29.4 kB
APT-Sources: https://repo.download.nvidia.com/jetson/t210 r32.5/main arm64 Packages
Description: NVIDIA Jetpack Meta Package

Package: nvidia-jetpack
Version: 4.5-b129
Priority: standard
Section: metapackages
Maintainer: NVIDIA Corporation
Installed-Size: 199 kB
Depends: nvidia-cuda (= 4.5-b129), nvidia-opencv (= 4.5-b129), nvidia-cudnn8 (= 4.5-b129), nvidia-tensorrt (= 4.5-b129), nvidia-visionworks (= 4.5-b129), nvidia-container (= 4.5-b129), nvidia-vpi (= 4.5-b129), nvidia-l4t-jetson-multimedia-api (>> 32.5-0), nvidia-l4t-jetson-multimedia-api (<< 32.6-0)
Homepage: http://developer.nvidia.com/jetson
Download-Size: 29.4 kB
APT-Sources: https://repo.download.nvidia.com/jetson/t210 r32.5/main arm64 Packages
Description: NVIDIA Jetpack Meta Package

$ cat /etc/nv_tegra_release
# R32 (release), REVISION: 5.1, GCID: 26202423, BOARD: t210ref, EABI: aarch64, DATE: Fri Feb 19 16:45:52 UTC 2021

$ sudo nvpmodel -q
NVPM WARN: fan mode is not set!
NV Power Mode: MAXN
0
```

# 1. Install face_recognition
```
$ sudo apt-get install python3-opencv
$ sudo apt-get install cmake libopenblas-dev liblapack-dev libjpeg-dev
$ sudo apt-get install python3-pip
$ sudo pip3 install face_recognition
```

# 2. Check if CUDA suppored
This is not used by CUDA lib. Some additional compiles is needed.
```
$ pip3 list |grep dlib
dlib                             19.17.0
launchpadlib                     1.10.6
$ python3
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
False
```

# 3. Install gcc-6 which will be needed by compiling with cuDNN lib
```
$ sudo vi /etc/apt/sources.list
  # Adding below:
  deb http://dk.archive.ubuntu.com/ubuntu/ bionic main universe
$ sudo apt-get update
$ sudo apt-get install gcc-6 g++-6
```

# 4. Install dlib with some compile options
```
$ wget http://dlib.net/files/dlib-19.21.tar.bz2
$ tar jxvf dlib-19.21.tar.bz2 
$ cd dlib-19.21/
$ mkdir build
$ cd build/
$ cmake .. -DDLIB_USE_CUDA=1 -DCUDA_HOST_COMPILER=/usr/bin/gcc-6
$ cd ..
$ sudo python3 setup.py install --set DLIB_USE_CUDA=1 --set CUDA_HOST_COMPILER=/usr/bin/gcc-6
```

# 5. Check if CUDA suppored again!
```
$ python3
Python 3.6.9 (default, Jan 26 2021, 15:33:00) 
[GCC 8.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.DLIB_USE_CUDA
True

$ pip3 list |grep dlib
dlib                             19.21.0
launchpadlib                     1.10.6
```
