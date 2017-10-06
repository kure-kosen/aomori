aomori
====

Overview

## Description
H29年度E科B研のソースコードです。

## Demo

## Requirement
- HomeBrew
- pip

## Usage

## Install

### OpenCV

```
$ brew tap homebrew/science
$ brew install opencv3 --with-python3
$ brew link opencv3 --force
```

### python3

```
$ brew install python3
$ pip install virtualenv
$ virtualenv aomori_env -p python3
$ pip install -r requirement.txt
```

### symbolic link

```
$ python3 -c "import cv2; print(cv2.__file__)"
{OPENCV_PATH}
# Example: /usr/local/lib/python3.6/site-packages/cv2.cpython-36m-darwin.so
$ ln -s {OPENCV_PATH} aomori_env/lib/python3.6/site-packages/
```

### check

```
$ source aomori_env/bin/activate
(aomori_env) $ python -V
python3.6.x
(aomori_env) $ python
>>> import cv2
>>> cv2
<module 'cv2' from ...>
```

## Licence

## Author
[chanyou0311](https://github.com/chanyou0311)

