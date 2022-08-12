# gauge-vision

Several video feeds of similar pressure gauges in operation will be available, the goal is to write software capable of turing that video stream into a stream of values representing the pressure reading of the gauge. 

## High Level Implementation Concerns

Ultimately the work in this repo will update a variable in the EPICS/DRAMA systems representing some compressor. 
Thus the run time of the algorithm should be reduced as much as possible and can be used as a measure of success when comparing algorithms or implementations.

## Image Processing

With some level of detail I describe the steps required to process a single frame (image) containing a pressure gauge and read it's current value.

### Image Acquisition (Pre Step)

Currently I have ~15 seconds of cell phone camera video of each dial in operation, they look equivalent (values ranges are the same and the ticks seem to be positioned at the same angle, i.e. 350 occurs at angle theta on both dials) despite their markings differing superficially.

these files are  in carbon:~/Project/gauge-vision/example/\*.mp4

### Blur

I believe this step is necessary for the performance of the circle Hough Transform (CHT).
The image is blurred using cv2.GaussianBlur.

### CHT

The dial's spatial position (center and radius) in the image is computed using a CHT.
I am using the cv2.HoughCircles implementation.


### Edge Detection

Edge detection is being done as a preprocessing step for the line detection step.
Currently using cv2.Canny for this.

### Line Detection

Line detection is being done specifically to detect the angle (in Q1) and  orientation.

Currently using cv2.HoughLines with some results, more parameter tuning needs to be done.


