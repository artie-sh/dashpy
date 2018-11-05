import pandas as pd

df = pd.read_csv('./xrp.csv')

for row in df:
    print row