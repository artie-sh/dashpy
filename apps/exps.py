import pandas as pd
import dateparser

df = pd.read_csv('./xrp1.csv')

# def avg(values):
#     return sum(values)/len(values)

def getData(df):
    coords = dict()
    for row in df.iterrows():
        r = list(row[1])

        coords[dateparser.parse(r[0])] = r[2]

    for item in sorted(coords.keys()):
        print(f"{item} - {coords[item]}")


getData(df)
