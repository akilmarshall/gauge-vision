# gauge-vision

Several video feeds of similar pressure gauges in operation will be available, the goal is to write software capable of turing that video stream into a stream of values representing the pressure reading of the gauge. 

## Todo

- write an object for training, (requires detections param) computes look up table
- write an object that uses the look up table (requires detections param) and computes pressures from images
- turn notebook block diagram into a dot(graphviz) diagram

## High Level Implementation Concerns

Ultimately the work in this repo will update a variable in the EPICS/DRAMA systems representing some compressor. 
Thus the run time of the algorithm should be reduced as much as possible and can be used as a measure of success when comparing algorithms or implementations.

## Operation Description

Instead of processing a video stream instead consider processing a single image as quickly as possible even if video data is available.

## Detect (object)

This object encapsulates the environmentally sensitive parameters related to image pre processing steps as well as the Hough transform applied.

Allows a set of _good_ parameters to be reused/communicated. 

## Training

The goal of training is to produce a look up table (theta -> pressure), I believe more information is necessary since theta is in (0, pi) Hough space.
Perhaps the look up table (r, theta) -> pressure is ok?
Currently it is (\_, theta) -> pressure.

### look up table

- Implemented as a dict?

## Operation

With a Detection object and pressure look up table, real time usage is simply applying the known good parameters to *quickly* compute the current pressure from an image with the look up table.

## Image Processing

With some level of detail I describe the steps required to process a single frame (image) containing a pressure gauge and read it's current value.

![image processing diagram](https://imgur.com/JNz5G4I.png)

- Compute the spatial position of the gauge (x, y, r)
- Crop the image to the gauge using (x, y, r)
- Apply blur
- Apply edge finding (emphasizing)
- Compute the spatial position of the needle

### Image Acquisition (Pre Step)

Currently I have ~15 seconds of cell phone camera video of each dial in operation, they look equivalent (values ranges are the same and the ticks seem to be positioned at the same angle, i.e. 350 occurs at angle theta on both dials) despite their markings differing superficially.

Some examples can be found [here](https://imgur.com/a/AmQpacS)

### Blur

cv2.GaussianBlur

- [tutorial\_py\_filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [cv2.GaussianBlur()](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1)

### CHT

The dial's spatial position (center and radius) in the image is computed using a CHT.
I am using the cv2.HoughCircles implementation.

- [tutorial\_py\_houghcircles](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)
- [cv2.HoughCircles()](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)

### Edge Detection

Edge detection is being done as a preprocessing step for the line detection step.
Currently using cv2.Canny for this.

Results in a binary image.

- [tutorial\_py\_canny](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [cv2.Canny()](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de)

### Line Detection (needle detection)

Line detection is being done specifically to detect the angle (in Q1) and  orientation.

Currently using cv2.HoughLines with some results, more parameter tuning needs to be done.

- [tutorial\_hough\_lines](https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html)
- [cv2.HoughLines()](https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga46b4e588934f6c8dfd509cc6e0e4545a)
