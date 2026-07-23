# This program shows how to remove duplicates record 

import pandas as pd

student={
    "Name":["Ali","Ali","Honey"],
    "Marks":[90,90,80]
}

df=pd.DataFrame(student)
df=df.drop_duplicates()

print(df)



