import pandas as pd
import numpy as np

data = pd.read_csv('/Users/giuliano/code/Slik300/forecasting-website/data/state_names_IND.csv')
data.head()
STATES = data['NAME_1,C,22'].tolist()
