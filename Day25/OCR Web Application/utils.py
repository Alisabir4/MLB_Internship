def save_text(text):

    filename = "OCR_Result.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    return filename