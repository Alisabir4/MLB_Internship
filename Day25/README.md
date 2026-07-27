# Day-25: Document OCR Web Application

## Overview

This project is a **Document OCR Web Application** developed using **Streamlit** and **EasyOCR**. It allows users to upload document images, preprocess them to improve readability, extract text using Optical Character Recognition (OCR), and download the extracted text as a `.txt` file.

---

## Features

* Upload document images
* Image preprocessing for better OCR accuracy
* Text extraction using EasyOCR
* Display original and processed images
* Display extracted text
* Download extracted text as a `.txt` file
* Simple and user-friendly Streamlit interface

---

## Technologies Used

* Python
* Streamlit
* EasyOCR
* OpenCV
* NumPy
* Pillow

---

## OCR Library Used

**EasyOCR**

EasyOCR is an open-source OCR library that supports multiple languages and provides accurate text recognition for printed documents without requiring model training.

---

## Preprocessing Techniques Applied

To improve OCR accuracy, the following preprocessing techniques were used:

* Grayscale Conversion
* Otsu Thresholding
* Median Blur (Denoising)

These preprocessing steps help reduce image noise and improve text visibility before OCR.

---

## Project Structure

```text
Day-25/
│
├── OCR Source Code/
│   ├── app.py
│   ├── preprocessing.py
│   ├── ocr.py
│   └── utils.py
│
├── requirements.txt
├── README.md
├── Sample Input Images/
├── Sample Output Results/
└── Screenshots/
```

---

## How to Run the Application

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your web browser.

---

## Testing

The application was tested on at least **15 different images**, including:

* Printed Documents
* Receipts
* Invoices
* Forms
* Utility Bills
* Bank Statements
* Certificates
* ID Cards
* Letters
* Book Pages

---

## Challenges Faced

* OCR accuracy decreases on blurry or low-quality images.
* Handwritten text is more difficult to recognize than printed text.
* Skewed or rotated documents may reduce recognition accuracy.
* Complex document layouts can affect the reading order of extracted text.

---

## Possible Improvements

* Support multiple OCR languages.
* Add document deskewing and perspective correction.
* Improve handwritten text recognition.
* Export extracted text to PDF or Microsoft Word.
* Enable batch processing for multiple document images.
* Preserve document layout during text extraction.

---

## GitHub Repository

**Repository Link:**
(Add your GitHub repository link here)

---

## ngrok Public URL

**Public URL:**
(Add your active ngrok URL here)


