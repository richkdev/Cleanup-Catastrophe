import cv2
import os

print(cv2.getBuildInformation())
print("ffmpeg accessable?", os.system("cd /; ffmpeg.exe"))

vid = cv2.VideoCapture()
print("VideoCapture opened successfully?", vid.open("http://127.0.0.1:5500/tests/opencv_web_test/video.mp4"))
