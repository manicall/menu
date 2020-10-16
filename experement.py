import pandas as pd


df = pd.read_excel(r'C:\Users\max\Desktop\example.xlsx',index_col=None,header=None)
print(df)
#df.to_excel('ToWrite.xlsx',index=False,header=False)
