import pandas as pd
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
print("dir_path:", dir_path)

data = pd.read_csv(os.path.join(dir_path, 'state_names_IND.csv'))
STATES = data['NAME_1,C,22'].tolist()
