import pandas as pd

df = pd.read_csv('../dataset/superstore.csv', encoding='cp1252')
print(df.head())
print(df.columns)