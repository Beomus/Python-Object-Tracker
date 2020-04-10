# Object Tracker 
Simple object tracker using Python and OpenCV

## Installation 

`$ pip install opencv-python imutils`

## TODO(Improvements)
- Specify read from Video or capture Webcam: 
		`import argparse
		
		ap = argparse.ArgumentParser()
		
		ap.add_argument('-v', '--video', help='Path to the video / [DEFAULT]: Webcam')
		
		ap.add_argument('-b', '--buffer', type=int, default=64, help='Change buffer size')
		
		ap.add_argument('-c', '--color', type=tuple, help='Input color range (lower, upper) in RGB')
		
		args = vars(ap.parse_args())
		`
