# This Program shows how to rename column 

import pandas as pd

student={
    "Name":["Ali","Honey"],
    "Marks":[90,80]
}

df=pd.DataFrame(student)
df=df.rename(columns={
    "Name":"Student Name",
    "Marks":"Student Marks"
    
})
print(df)

# in this way we are renaming the columns

