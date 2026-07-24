# Day-24: Optical Character Recognition (OCR) with EasyOCR

## Overview

This project demonstrates Optical Character Recognition (OCR) using the EasyOCR library. The application extracts text from images and displays the recognized text. It also enhances the image before OCR to improve recognition accuracy.

---
## Explanation

### What is OCR?

Optical Character Recognition (OCR) is a technology that enables computers to detect and extract text from images, scanned documents, receipts, invoices, books, and other visual sources. It converts printed or handwritten text into editable and searchable digital text.

---

### Which OCR Library Did I Use and Why?

This project uses **EasyOCR** because it is easy to set up, supports multiple languages, and provides good accuracy for recognizing text from various types of images. It works well with Python and performs effectively on printed documents, signboards, receipts, and book pages without requiring complex configuration.

---

### What Preprocessing Techniques Improved the Results?

The following image preprocessing techniques were applied before OCR to improve text recognition:

- **Grayscale Conversion:** Simplified the image by removing color information.
- **Histogram Equalization:** Enhanced image contrast, making text more visible.
- **Image Enhancement:** Improved the clarity of characters, especially in low-contrast images.

These preprocessing steps increased OCR accuracy, particularly for images with poor lighting or faint text.

---

### Challenges Faced While Extracting Text

Some challenges encountered during the project included:

- Low-quality or blurry images reduced OCR accuracy.
- Handwritten text was more difficult to recognize than printed text.
- Small or stylized fonts were sometimes recognized incorrectly.
- Images with uneven lighting or shadows affected text extraction.
- Initial setup required downloading EasyOCR models, and incorrect image file paths caused loading errors during testing.

## Topics Covered

- Introduction to OCR
- EasyOCR Installation and Setup
- Image Preprocessing
- Text Extraction
- OCR Comparison
- Streamlit Deployment

---

## Coding Practice

Completed the following tasks:

- Installed and configured EasyOCR
- Extracted text from 15 different images
- Tested OCR on:
  - Printed documents
  - Receipts
  - Invoices
  - Signboards
  - Book pages
  - Handwritten notes
- Applied grayscale conversion
- Applied image enhancement (Histogram Equalization)
- Compared OCR results before and after preprocessing

---

## Mini Project

### Simple OCR Document Reader

### Features

- Upload an image
- Display the original image
- Convert image to grayscale
- Enhance the image
- Extract text using EasyOCR
- Display extracted text
- Download extracted text as a `.txt` file

---

## Dataset

The project was tested on at least **15 images** containing text, including:

- Printed Documents
- Books
- Receipts
- Invoices
- Forms
- Signboards
- Handwritten Notes

The images contain different lighting conditions, backgrounds, and text sizes.

---

## OCR Comparison

| Image Type | Original OCR | Enhanced OCR | Observation |
|------------|--------------|--------------|-------------|
| Printed Document | Excellent | Excellent | Very accurate |
| Receipt | Moderate | Better | Numbers became clearer |
| Invoice | Good | Better | Small text improved |
| Signboard | Good | Excellent | Better edge detection |
| Book Page | Good | Excellent | Improved readability |
| Handwritten Note | Poor | Moderate | Some words recognized |

---

## Technologies Used

- Python
- EasyOCR
- OpenCV
- NumPy
- Pillow
- Streamlit

---

## Project Structure

```
Day-24/
│
├── Coding Practice/
│   ├── ocr_easyocr.py
│   ├── Input Images/
│   ├── Original OCR/
│   ├── Enhanced OCR/
│   └── Comparison/
│
├── Mini Project/
│   ├── simple_ocr_reader.py
│   └── Output/
│
├── app.py
├── requirements.txt
├── README.md
├── Sample Input Images/
├── Extracted Text Files/
└── Demo.mp4
```

---

## How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
streamlit run app.py
```

---

## Streamlit Features

- Upload an image
- View the original image
- View the enhanced image
- Extract text using EasyOCR
- Display extracted text
- Download extracted text as a text file

---

## Deployment

### GitHub Repository

Add your GitHub repository link here:

```
https://github.com/YourUsername/MLB_Internship/tree/main/Day24
```

### Streamlit Community Cloud

Add your deployed Streamlit app link here:

```
https://your-app-name.streamlit.app/
```

---

## Deliverables

- ✅ OCR Practice Scripts
- ✅ Mini Project Source Code
- ✅ Streamlit Application (`app.py`)
- ✅ `requirements.txt`
- ✅ Sample Input Images
- ✅ Extracted Text Files
- ✅ `README.md`
- ✅ GitHub Repository Link
- ✅ Streamlit App Link
- ✅ Screen Recording Demonstration

---

## Conclusion

This project demonstrates how EasyOCR can be used to extract text from different types of images. Image preprocessing techniques such as grayscale conversion and histogram equalization improve OCR accuracy, especially for low-quality images. The application was successfully deployed using Streamlit Community Cloud, making it accessible through a web interface.