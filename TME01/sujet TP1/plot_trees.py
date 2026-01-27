import csv
import matplotlib.pyplot as plt

iterations = []
fractions = []

# Read CSV
with open("trees.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        iterations.append(int(row[0]))
        fractions.append(float(row[1]))

# Plot
plt.plot(iterations, fractions, color='green')
plt.xlabel("Iterations")
plt.ylabel("Fraction of Healthy Trees")
plt.title("Healthy Trees Over Time")
plt.grid(True)
plt.show()
