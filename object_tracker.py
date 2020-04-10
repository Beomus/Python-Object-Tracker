from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import time
import imutils

video_path = ''

# type int: this decides the max amount of x, y coordinates that we are tracking 
buffer_size = 64 


# Color range: this will be the color range of the object you are tracking
LOWER = (29, 86, 6)
UPPER = (64, 255, 255)
pos = deque(maxlen=buffer_size)

vs = VideoStream(scr=0).start()

time.sleep(2)
run = True
while run:
	frame = vs.read()

	if frame is None:
		run = False

	# resizing the frame so we can achieve more fps and read easily
	frame = imutils.resize(frame, width=700)
	blur = cv2.GaussianBlur(frame, (5, 5), 0)
	# convert to HSV color
	# [INFO]: https://en.wikipedia.org/wiki/HSL_and_HSV
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

	# masking for the color green
	mask = cv2.inRange(hsv, LOWER, UPPER)
	# erode and dilate to remove all smallers objects or blobs
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# finding the contours and taking the center position of the object
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	center = None
	# making sure if we have any contours in the video
	if len(cnts) > 0:
		# assuming we only track one green object so it should be the biggest object
		c = max(cnts, key=cv2.contourArea)

		# getting the radius of the object
		((x, y), radius) = cv2.minEnclosingCircle(c)

		# getting its coordinate and calculating the centroid
		M = cv2.moments(c)
		center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

		# checking the minimum size of the object
		if radius > 10:
			# draw circle and centroid on the frame
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	# appending the coordinates to deque
	pos.appendleft(center)

	for i in range(1, len(pos)):
		# if there is None the continue, this ensures that we don't break the script
		# when there is no object to track or when the object leave the screen
		if pos[i -1] is None or pos[i] is None:
			continue

		# making a dynamic thickness that disappears over time 
		# and is thicker when it's more recent
		thickness = int(np.sqrt(buffer_size / float(i + 1) * 2.5))
		cv2.line(frame, pos[i - 1], pos[i], (0, 0, 255), thickness)

	# show frame 
	cv2.imshow('Frame', frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		run = False

vs.stop()

cv2.destroyAllWindows()
