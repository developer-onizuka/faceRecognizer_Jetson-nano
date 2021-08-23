# faceRecognizer with Jetson nano
See also https://wisteriahill.sakura.ne.jp/CMS/WordPress/2020/12/15/jetson-nano-build-dlib-use-gpu-for-face-recognition/ before install of dlib and face_recognition.

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
