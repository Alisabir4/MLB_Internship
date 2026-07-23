#  Read a text file and display

with open("Textfile_WriteData.txt","r") as file:
    content=file.read()

print(content)
