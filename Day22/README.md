README.md
OpenCV Video Processing

This project demonstrates video processing using OpenCV. It reads a video file, processes each frame by applying image processing techniques, displays video information, and saves the processed video. It also supports real-time webcam processing.

How OpenCV Reads Videos

OpenCV reads videos using the cv2.VideoCapture() function. The video is opened frame by frame, allowing each frame to be processed individually. The read() method returns the current frame until the end of the video is reached.

What FPS Means

FPS (Frames Per Second) represents the number of video frames displayed or recorded in one second. A higher FPS results in smoother video playback, while a lower FPS produces less smooth motion.

Processing Techniques Applied

The following image processing techniques were applied to each video frame:

Converted each frame to Grayscale.
Applied Gaussian Blur to reduce image noise.
Used Canny Edge Detection to detect object edges.
Displayed video properties including FPS, width, height, total frames, and current frame number.
Saved the processed video as a new output file.
Challenges Faced

Some challenges encountered while working with video frames included:

Maintaining smooth processing speed while processing every frame.
Ensuring the processed video was saved with the correct FPS and resolution.
Handling different video formats and properties.
Adapting the application for deployment on Hugging Face, where desktop functions like cv2.imshow() and webcam access are not supported.