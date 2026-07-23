import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)

image = None
filename = ""

while True:

    print("\n========== Image Processing Toolkit ==========")
    print("1. Load Image")
    print("2. Convert to Grayscale")
    print("3. Resize Image")
    print("4. Rotate Image")
    print("5. Flip Image")
    print("6. Crop Image")
    print("7. Draw Shapes")
    print("8. Add Custom Text")
    print("9. Save Image")
    print("10. Display Image")
    print("0. Exit")

    choice = input("\nEnter your choice: ")

    # Load Image
    if choice == "1":

        filename = input("Enter image name (example: person.jpg): ")

        path = os.path.join("input", filename)

        image = cv2.imread(path)

        if image is None:
            print("Image not found!")
        else:
            print("Image Loaded Successfully.")

    elif choice == "2":

        if image is None:
            print("Load an image first.")
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print("Converted to Grayscale.")

    elif choice == "3":

        if image is None:
            print("Load an image first.")
        else:
            width = int(input("Enter Width: "))
            height = int(input("Enter Height: "))
            image = cv2.resize(image, (width, height))
            print("Image Resized.")

    elif choice == "4":

        if image is None:
            print("Load an image first.")
        else:

            print("1. Rotate 90°")
            print("2. Rotate 180°")
            print("3. Rotate 270°")

            rotate = input("Choose: ")

            if rotate == "1":
                image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

            elif rotate == "2":
                image = cv2.rotate(image, cv2.ROTATE_180)

            elif rotate == "3":
                image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

            print("Rotation Completed.")

    elif choice == "5":

        if image is None:
            print("Load an image first.")
        else:

            print("1. Horizontal Flip")
            print("2. Vertical Flip")

            flip = input("Choose: ")

            if flip == "1":
                image = cv2.flip(image, 1)
            else:
                image = cv2.flip(image, 0)

            print("Image Flipped.")

    elif choice == "6":

        if image is None:
            print("Load an image first.")
        else:

            x = int(input("Start X: "))
            y = int(input("Start Y: "))
            w = int(input("Width: "))
            h = int(input("Height: "))

            image = image[y:y+h, x:x+w]

            print("Image Cropped.")

    elif choice == "7":

        if image is None:
            print("Load an image first.")
        else:

            draw = image.copy()

            # Rectangle
            cv2.rectangle(draw, (20,20), (180,180), (0,255,0), 2)

            # Circle
            cv2.circle(draw, (300,100), 50, (255,0,0), 2)

            # Line
            cv2.line(draw, (0,0), (400,300), (0,0,255), 2)

            # Polygon
            points = np.array([[250,250],[320,200],[400,250],[370,330],[270,330]], np.int32)
            points = points.reshape((-1,1,2))

            cv2.polylines(draw,[points],True,(255,255,0),2)

            image = draw

            print("Shapes Added.")

    elif choice == "8":

        if image is None:
            print("Load an image first.")
        else:

            text = input("Enter Text: ")

            cv2.putText(
                image,
                text,
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2
            )

            print("Text Added.")

    elif choice == "9":

        if image is None:
            print("Load an image first.")
        else:

            save_name = input("Enter output file name (example: result.jpg): ")

            save_path = os.path.join("output", save_name)

            cv2.imwrite(save_path, image)

            print("Image Saved Successfully.")

    elif choice == "10":

        if image is None:
            print("Load an image first.")
        else:

            cv2.imshow("Image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    elif choice == "0":

        print("Program Closed.")
        break

    else:
        print("Invalid Choice!")