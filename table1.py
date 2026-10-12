import pickle
import numpy as np
import matplotlib.pyplot as plt

with open("data.pkl", "rb") as f:
    data = pickle.load(f)

d = {key: values[3:5] for key, values in data.items()}
print(d)

keys = list(d.keys())
x = np.arange(len(keys))
width = 0.15

# nom
nom = ["SB", "Bellman"]

values1 = [100*d[k][0]-80 for k in keys]
values2 = [100*d[k][1]-80 for k in keys]

plt.bar(x - width/2, values1, width, label="Bellman", bottom=80)
plt.bar(x + width/2, values2, width, label="SB", bottom=80)


plt.xticks(x, keys)
plt.xlabel("Zmax")
plt.ylabel("% of perfectly informed play")
plt.legend()
plt.savefig("graphique.pdf", format="pdf", bbox_inches="tight")