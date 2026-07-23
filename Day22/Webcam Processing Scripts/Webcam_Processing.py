import cv2
import os

# Input and Output Paths


input_video = r"D:\python\MLB_Internship\Day22\Input Videos\Park.mp4"
output_folder = r"D:\python\MLB_Internship\Day22\Output Videos"

os.makedirs(output_folder, exist_ok=True)

output_video = os.path.join(output_folder, "processed_video.mp4")


# Read Video


cap = cv2.VideoCapture(input_video)

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()

# Video Properties

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("Video Properties")
print("-------------------------")
print("FPS:", fps)
print("Width:", width)
print("Height:", height)
print("Total Frames:", total_frames)

# Video Writer


fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    output_video,
    fourcc,
    fps,
    (width, height)
)

# Process Recorded Video


while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Current Frame Number
    frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    # Convert to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny Edge Detection
    edges = cv2.Canny(blur, 50, 150)

    # Convert to BGR for writing text
    processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

   
    # Display Video Information

    cv2.putText(processed, f"FPS: {fps}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Width: {width}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Height: {height}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Total Frames: {total_frames}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Current Frame: {frame_no}", (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    
    # Display Videos
    

    cv2.imshow("Original Video", frame)
    cv2.imshow("Processed Video", processed)

    # Save Processed Video
    out.write(processed)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print("Processed video saved successfully!")


# Webcam Processing


webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Error: Cannot access webcam.")
    exit()

print("Webcam Started")
print("Press 'Q' to Quit")

while True:

    ret, frame = webcam.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Webcam Properties
    webcam_width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
    webcam_height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    webcam_fps = webcam.get(cv2.CAP_PROP_FPS)

    cv2.putText(processed, f"FPS: {webcam_fps:.2f}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Width: {webcam_width}", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(processed, f"Height: {webcam_height}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Webcam Original", frame)
    cv2.imshow("Webcam Processed", processed)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

print("Webcam processing finished.")