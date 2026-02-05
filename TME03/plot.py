import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv("SANE_Count.csv", header=None, names=["iteration", "count"])
df2 = pd.read_csv("INFECTED_Count.csv", header=None, names=["iteration", "count"])
df3 = pd.read_csv("RECOVER_Count.csv", header=None, names=["iteration", "count"])

iteration = df1["iteration"]

plt.plot(iteration, df1["count"], label="SANE")
plt.plot(iteration, df2["count"], label="INFECTED")
plt.plot(iteration, df3["count"], label="RECOVER")

plt.xlabel("Iteration")
plt.ylabel("Count")
plt.legend()
plt.show()
