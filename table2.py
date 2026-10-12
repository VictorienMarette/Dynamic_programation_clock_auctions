import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

with open("data.pkl", "rb") as f:
    d = pickle.load(f)

df = pd.DataFrame(
    {zmax: [values[0], values[1], values[3]] for zmax, values in d.items()},
    index=["E[U]", "E[Û]", "E[Û]/E[U]"]
)

print(df)

df = pd.DataFrame(
    {zmax: [values[5]] for zmax, values in d.items()},
    index=["P(U =  Û)"]
)

print(df)