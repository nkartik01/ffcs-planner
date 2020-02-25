import pandas as pd
def read(file,n):
    dataset=pd.read_csv(file)
    data=dataset.iloc[0:,0:n].values
    return data
