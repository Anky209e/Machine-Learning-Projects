import pandas as pd

def find_data(numbers):
    df = pd.read_csv("data.csv")
    for i in range(0,len(df)-1):
        for num in numbers:
            if df["NUMBER PLATE"][i] == num:
                name = df["REGISTERED NAME"][i]
                address = df["ADDRESS"][i]
                mob_no = df["MOBILE NUMBER"][i]

                return {"name":name,"address":address,"mob":mob_no}
    return None
                


