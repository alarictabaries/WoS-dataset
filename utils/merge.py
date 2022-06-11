import pandas as pd

f1 = pd.read_excel("../data/tg/1.xls")
f2 = pd.read_excel("../data/tg/2.xls")
f3 = pd.read_excel("../data/tg/3.xls")

f = pd.concat([f1, f2, f3])
f.drop_duplicates()

f.to_csv("../data/tg/full.csv",index=False)