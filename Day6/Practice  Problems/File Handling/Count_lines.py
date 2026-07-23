# Count number of lines

with open("Textfile_WriteData.txt","r") as file:
    lines=file.readlines()
    
print("Toatl Number of lines are :",len(lines))