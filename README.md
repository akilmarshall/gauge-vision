# gauge-vision

Several video feeds of similar pressure gauges in operation will be available, the goal is to write software capable of turing that video stream into a stream of values representing the pressure readings of the gauge. 

Ultimately the work in this repo will update a variable in the EPICS/DRAMA systems representing some compressor. 
Thus the run time of the algorithm should be reduced as much as possible and can be used as a measure of success when comparing algorithms or implementations.

<p align="center">
<img src=https://imgur.com/qmYCjDS.png alt="" width="250"/>
<img src=https://imgur.com/k0YyhoU.png alt="" width="250"/>
</p>
<p align="center">
<img src=https://imgur.com/McrgEL7.png alt="" width="250"/>
<img src=https://imgur.com/Ijun0Cu.png alt="" width="250"/>
</p>

## Todo

- write an object for training, (requires detections param) computes look up table
- write an object that uses the look up table (requires detections param) and computes pressures from images

## Operation

With a Detection object and pressure look up table, real time usage is simply applying the known good parameters to *quickly* compute the current pressure from an image with the look up table.

## Image Processing

With some level of detail I describe the steps required to process a single frame (image) containing a pressure gauge and read it's current value.

<p align="center">
	<img src=https://imgur.com/JNz5G4I.png />
</p>
<p align = "center">Image processing pipeline.</p>

### Image Acquisition (Pre Step)

Currently I have ~15 seconds of cell phone camera video of each dial in operation, they look equivalent (values ranges are the same and the ticks seem to be positioned at the same angle, i.e. 350 occurs at angle theta on both dials) despite their markings differing superficially.

They can be found [here](https://imgur.com/a/AmQpacS).

### Blur

Necessary to obscure incidental lines and other edges that are not the needle.

Using cv2.GaussianBlur

- [tutorial\_py\_filtering](https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html)
- [cv2.GaussianBlur()](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gaabe8c836e97159a9193fb0b11ac52cf1)

### CHT

The dial's spatial position (center and radius) in the image is computed using a CHT.
Using the cv2.HoughCircles implementation.

- [tutorial\_py\_houghcircles](https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html)
- [cv2.HoughCircles()](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga47849c3be0d0406ad3ca45db65a25d2d)

[stack overflow thread](https://dsp.stackexchange.com/questions/22648/in-opecv-function-hough-circles-how-does-parameter-1-and-2-affect-circle-detecti) describing CHT parameters intuitively.

### Crop

Using the spatial data acquired in the previous step the image is cropped (simplifying the line detection problem and reducing the load on subsequent image processing steps).

Using [pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=crop#PIL.Image.Image.crop) for this.

(does cv2 offer a crop method?)

### Edge Detection

Edge detection is being done as a preprocessing step for the line detection step.
Currently using cv2.Canny for this.
Results in a binary image (2 color).

- [tutorial\_py\_canny](https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html)
- [cv2.Canny()](https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de)

### Linear Hough Transform (needle detection)

Line detection is being done specifically to detect the angle (in Q1) and  orientation.

Currently using cv2.HoughLines, although the open cv docs claim HoughLinesP is more efficient I did not observe significant time savings when switching to 
the probabilistic version of the transform, in fact run time increased on average.

- [tutorial\_hough\_lines](https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html)
- [cv2.HoughLines()](https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga46b4e588934f6c8dfd509cc6e0e4545a)
- [cv2.HoughLinesP](https://docs.opencv.org/3.4/dd/d1a/group__imgproc__feature.html#ga8618180a5948286384e3b7ca02f6feeb)
